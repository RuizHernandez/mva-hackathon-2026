"""
Frequency-filters the genome-wide HIGH-impact PASS variant list produced by
SnpEff (data/snpeff_out/high_impact_filtered.tsv) using Ensembl VEP REST to
pull gnomAD AF + ClinVar status. This is the unbiased, genome-wide analog of
scripts/annotate_candidates.py, which only covered a 13-gene candidate panel.

Usage:
    python annotate_genomewide_highimpact.py
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
IN_TSV = Path(__file__).resolve().parent.parent / "data" / "snpeff_out" / "high_impact_filtered.tsv"
OUT_TSV = IN_TSV.with_name("high_impact_genomewide_annotated.tsv")


def load_variants():
    variants = []
    with open(IN_TSV, newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            alt = row["alt"].split(",")[0]
            variants.append({
                "chrom": row["chrom"], "pos": int(row["pos"]), "ref": row["ref"],
                "alt": alt, "gene": row["gene"], "snpeff_consequence": row["consequence"],
                "hgvsp": row["hgvsp"],
            })
    return variants


def to_vep_str(v):
    return f"{v['chrom']} {v['pos']} . {v['ref']} {v['alt']} . . ."


def chunked(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def main():
    variants = load_variants()
    print(f"Annotating {len(variants)} genome-wide HIGH-impact variants via VEP REST...", file=sys.stderr)

    results = []
    for i, batch in enumerate(chunked(variants, BATCH_SIZE)):
        payload = {"variants": [to_vep_str(v) for v in batch]}
        resp = requests.post(VEP_URL, headers=HEADERS, data=json.dumps(payload),
                              params={"canonical": 1}, timeout=90)
        if resp.status_code != 200:
            print(f"batch {i}: error {resp.status_code}", file=sys.stderr)
            time.sleep(3)
            continue
        data = resp.json()
        for v, entry in zip(batch, data):
            colocated = entry.get("colocated_variants", [])
            freqs, clin = {}, []
            for cv in colocated:
                for allele, fdict in cv.get("frequencies", {}).items():
                    freqs.update(fdict)
                clin.extend(cv.get("clin_sig", []))
            gnomad_af = freqs.get("gnomad", freqs.get("gnomade", freqs.get("gnomadg", "")))
            results.append({**v, "gnomad_af": gnomad_af, "clin_sig": ";".join(sorted(set(clin)))})
        print(f"  batch {i+1}/{(len(variants)-1)//BATCH_SIZE + 1} done", file=sys.stderr)
        time.sleep(1)

    with open(OUT_TSV, "w", newline="") as f:
        cols = ["chrom", "pos", "ref", "alt", "gene", "snpeff_consequence", "hgvsp", "gnomad_af", "clin_sig"]
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t")
        w.writeheader()
        for r in results:
            w.writerow({k: r.get(k, "") for k in cols})
    print(f"Written: {OUT_TSV} ({len(results)} rows)", file=sys.stderr)

    print("\n=== Rare (AF<0.0001 or absent) or ClinVar path/likely-path, genome-wide ===")
    for r in results:
        af = r["gnomad_af"]
        try:
            af_val = float(af) if af != "" else None
        except ValueError:
            af_val = None
        is_pathogenic = any(k in r["clin_sig"].lower() for k in ["pathogenic"])
        is_rare = af_val is None or af_val < 0.0001
        if is_rare or is_pathogenic:
            print(f"{r['gene']}\t{r['chrom']}:{r['pos']}{r['ref']}>{r['alt']}\t{r['snpeff_consequence']}\t"
                  f"{r['hgvsp']}\tgnomAD_AF={af}\tClinVar={r['clin_sig']}")


if __name__ == "__main__":
    main()
