"""Genera el CSV de submission de Track 1 en el formato exacto requerido."""

import csv
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "submissions" / "track1" / "ihruizh_bub1b-compound-het.csv"

ROWS = [
    {
        "proband_id": "WGS_EX2312012",
        "chrom_1": "chr15",
        "pos_1": 40209701,
        "ref_1": "T",
        "alt_1": "G",
        "chrom_2": "chr15",
        "pos_2": 40220612,
        "ref_2": "T",
        "alt_2": "G",
        "epcr": 0.9,
        "finding_type": "primary",
        "notes": (
            "BUB1B compound heterozygote. Variant 1 (c.2210T>G, p.Leu737Ter) is a "
            "known stop-gained variant classified Pathogenic/Likely pathogenic in "
            "ClinVar (VCV000533901, rs759242053), gnomAD AF ~7.9e-5, cited in the "
            "founding BUB1B-MVA paper (Hanks et al. 2004, PMID 15475955). Variant 2 "
            "(c.3006T>G, p.Asn1002Lys) is a novel missense absent from gnomAD, "
            "predicted deleterious (SIFT 0.01) and probably damaging (PolyPhen "
            "0.997). Both are heterozygous in the proband; trans configuration is "
            "assumed (singleton WGS, no parental samples, no read-backed phasing "
            "at these positions) but not directly confirmed. BUB1B biallelic "
            "loss-of-function causes Mosaic Variegated Aneuploidy type 1 / PCS "
            "syndrome (autosomal recessive), matching the proband's phenotype "
            "(rhabdomyosarcoma, IUGR/short stature, failure to thrive) and the "
            "reported parental recurrent miscarriages consistent with carrier "
            "parents."
        ),
    },
]

FIELDS = ["proband_id", "chrom_1", "pos_1", "ref_1", "alt_1", "chrom_2", "pos_2",
          "ref_2", "alt_2", "epcr", "finding_type", "notes"]


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for row in ROWS:
            w.writerow(row)
    print(f"Escrito: {OUT}")


if __name__ == "__main__":
    main()
