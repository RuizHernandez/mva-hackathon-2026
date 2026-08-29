"""
Anota con Ensembl VEP REST (GRCh38) las variantes del panel de genes
candidatos, leyendo el TSV generado por filter_candidate_genes.py.

Uso:
    python annotate_candidates.py data/candidate_variants.tsv
"""

import csv
import json
import sys
import time
from pathlib import Path

import requests

VEP_URL = "https://rest.ensembl.org/vep/human/region"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}
BATCH_SIZE = 100

COMMON_HGNC_ALIASES = {
    # a veces VEP resuelve el símbolo con el gen canónico solapado distinto
}


def load_variants(tsv_path):
    variants = []
    with open(tsv_path, newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            if row["filter"] != "PASS":
                continue
            alt = row["alt"].split(",")[0]  # sitios multialélicos: primer ALT
            variants.append({
                "gene": row["gene"],
                "chrom": row["chrom"],
                "pos": int(row["pos"]),
                "ref": row["ref"],
                "alt": alt,
                "gt": row["gt"],
            })
    return variants


def to_vep_region_string(v):
    return f"{v['chrom']} {v['pos']} . {v['ref']} {v['alt']} . . ."


def chunked(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


def annotate(variants):
    results = []
    for batch in chunked(variants, BATCH_SIZE):
        payload = {"variants": [to_vep_region_string(v) for v in batch]}
        resp = requests.post(
            VEP_URL, headers=HEADERS, data=json.dumps(payload),
            params={"canonical": 1, "hgvs": 1}, timeout=90,
        )
        if resp.status_code != 200:
            print(f"Error {resp.status_code} en batch: {resp.text[:300]}", file=sys.stderr)
            time.sleep(3)
            continue
        data = resp.json()
        for v, entry in zip(batch, data):
            most_severe = entry.get("most_severe_consequence")
            tcs = entry.get("transcript_consequences", [])
            canonical_tc = next((t for t in tcs if t.get("canonical") == 1), tcs[0] if tcs else {})
            colocated = entry.get("colocated_variants", [])
            freqs = {}
            clin_sig = []
            for cv in colocated:
                for allele, fdict in cv.get("frequencies", {}).items():
                    freqs.update(fdict)
                clin_sig.extend(cv.get("clin_sig", []))
            results.append({
                **v,
                "gene_symbol": canonical_tc.get("gene_symbol", v["gene"]),
                "consequence": most_severe,
                "impact": canonical_tc.get("impact", ""),
                "hgvsc": canonical_tc.get("hgvsc", ""),
                "hgvsp": canonical_tc.get("hgvsp", ""),
                "sift": canonical_tc.get("sift_prediction", ""),
                "polyphen": canonical_tc.get("polyphen_prediction", ""),
                "gnomad_af": freqs.get("gnomad", freqs.get("gnomade", freqs.get("gnomadg", ""))),
                "clin_sig": ";".join(sorted(set(clin_sig))),
            })
        time.sleep(1)
    return results


IMPACTFUL = {
    "stop_gained", "stop_lost", "start_lost", "frameshift_variant",
    "splice_acceptor_variant", "splice_donor_variant", "missense_variant",
    "inframe_deletion", "inframe_insertion", "splice_region_variant",
    "protein_altering_variant",
}


def main():
    tsv_path = sys.argv[1] if len(sys.argv) > 1 else "data/candidate_variants.tsv"
    variants = load_variants(tsv_path)
    print(f"Anotando {len(variants)} variantes PASS (VEP REST, GRCh38)...", file=sys.stderr)
    results = annotate(variants)

    out_path = Path(tsv_path).with_name("candidate_variants_annotated.tsv")
    with open(out_path, "w", newline="") as f:
        cols = ["gene_symbol", "chrom", "pos", "ref", "alt", "gt", "consequence",
                "impact", "hgvsc", "hgvsp", "sift", "polyphen", "gnomad_af", "clin_sig"]
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t")
        w.writeheader()
        for r in results:
            w.writerow({k: r.get(k, "") for k in cols})
    print(f"Escrito: {out_path} ({len(results)} filas)", file=sys.stderr)

    print("\n=== Candidatos de interés (impacto funcional + AF baja/ausente/patogénica) ===")
    for r in results:
        af = r["gnomad_af"]
        try:
            af_val = float(af) if af != "" else None
        except ValueError:
            af_val = None
        rare = af_val is None or af_val < 0.001
        if r["consequence"] in IMPACTFUL and rare:
            print(
                f"{r['gene_symbol']}\t{r['chrom']}:{r['pos']}{r['ref']}>{r['alt']}\t"
                f"GT={r['gt']}\t{r['consequence']}\t{r['impact']}\t{r['hgvsp']}\t"
                f"SIFT={r['sift']}\tPolyPhen={r['polyphen']}\tgnomAD_AF={af}\tClinVar={r['clin_sig']}"
            )


if __name__ == "__main__":
    main()
