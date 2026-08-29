"""
Redaction-safe genotype check for the two nominated BUB1B loci.

Confirms the proband's genotype at exactly the two candidate positions
without emitting anything else from the VCF: no sample name, no depth, no
allelic depth, no quality scores, no other variant calls. Intended to let a
reviewer (or a future collaborator) re-verify the nominated calls against
the controlled-access VCF without re-exposing broader patient genomic data.

Usage:
    python check_target_calls.py --vcf data/WGS_EX2312012_HGWCNDSX7.vcf.gz
"""

import argparse
import gzip
import json
import sys
from pathlib import Path

TARGET_LOCI = [
    {"chrom": "15", "pos": 40209701, "ref": "T", "alt": "G", "label": "BUB1B c.2210T>G (p.Leu737Ter)"},
    {"chrom": "15", "pos": 40220612, "ref": "T", "alt": "G", "label": "BUB1B c.3006T>G (p.Asn1002Lys)"},
]


def classify(gt: str) -> str:
    alleles = gt.replace("|", "/").split("/")
    if len(alleles) != 2:
        return "unknown"
    if alleles[0] == alleles[1] == "0":
        return "hom_ref"
    if alleles[0] == alleles[1] and alleles[0] not in ("0", "."):
        return "hom_alt"
    if "." in alleles:
        return "unknown"
    return "het"


def check(vcf_path: Path):
    results = {loc["label"]: {"found": False, "genotype_class": None} for loc in TARGET_LOCI}
    remaining = {(loc["chrom"], loc["pos"]): loc for loc in TARGET_LOCI}

    with gzip.open(vcf_path, "rt") as f:
        for line in f:
            if not remaining:
                break
            if line[0] == "#":
                continue
            fields = line.rstrip("\n").split("\t")
            key = (fields[0], int(fields[1]))
            loc = remaining.get(key)
            if loc is None:
                continue
            ref, alt = fields[3], fields[4].split(",")[0]
            if ref != loc["ref"] or alt != loc["alt"]:
                continue
            gt = fields[9].split(":")[0]
            results[loc["label"]] = {"found": True, "genotype_class": classify(gt)}
            del remaining[key]

    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vcf", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=None,
                         help="Optional path to write JSON result (default: stdout only)")
    args = parser.parse_args()

    results = check(args.vcf)
    output = json.dumps(results, indent=2)
    print(output)
    if args.output:
        args.output.write_text(output)


if __name__ == "__main__":
    main()
