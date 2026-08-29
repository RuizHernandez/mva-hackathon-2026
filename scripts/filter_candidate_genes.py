"""
Extrae variantes del VCF del proband dentro de coordenadas de un panel de
genes candidatos (GRCh38, Ensembl), y las escribe a un TSV para anotación
posterior. Parsing lineal con gzip (cyvcf2/pysam/tabix no disponibles en
este entorno Windows).

Uso:
    python filter_candidate_genes.py > data/candidate_variants.tsv
"""

import gzip
import sys
from pathlib import Path

VCF = Path(__file__).resolve().parent.parent / "data" / "WGS_EX2312012_HGWCNDSX7.vcf.gz"
PADDING = 20_000  # bp de margen para variantes reguladoras/splice cercanas

# Coordenadas GRCh38 (Ensembl release 116), sin prefijo "chr" (el VCF usa
# notación numérica 1..22,X,Y según su ##reference).
CANDIDATE_GENES = {
    # Genes causales establecidos de Mosaic Variegated Aneuploidy (MVA1-3)
    "BUB1B": ("15", 40_160_984, 40_221_137),
    "CEP57": ("11", 95_789_965, 95_837_070),
    "TRIP13": ("5", 892_849, 919_357),
    # Panel ampliado: checkpoint mitótico / cinetocoro / inestabilidad
    # cromosómica con predisposición a cáncer + restricción de crecimiento
    # (diagnóstico diferencial de la constelación fenotípica del caso)
    "CEP57L1": ("6", 109_095_105, 109_174_418),
    "BUB1": ("2", 110_635_468, 110_678_098),
    "BUB3": ("10", 123_154_365, 123_313_144),
    "MAD1L1": ("7", 1_815_787, 2_233_243),
    "MAD2L1": ("4", 120_055_623, 120_067_192),
    "CENPE": ("4", 103_105_349, 103_198_463),
    "BLM": ("15", 90_717_340, 90_816_166),
    "NBN": ("8", 89_924_515, 90_003_228),
    "ATM": ("11", 108_222_788, 108_369_102),
    "ATR": ("8", 17_496_975, 17_570_573),
}


def main():
    regions = {
        g: (c, max(0, s - PADDING), e + PADDING)
        for g, (c, s, e) in CANDIDATE_GENES.items()
    }
    by_chrom = {}
    for g, (c, s, e) in regions.items():
        by_chrom.setdefault(c, []).append((s, e, g))

    print("gene\tchrom\tpos\tid\tref\talt\tqual\tfilter\tinfo\tgt")

    with gzip.open(VCF, "rt") as f:
        for line in f:
            if line[0] == "#":
                continue
            fields = line.rstrip("\n").split("\t")
            chrom = fields[0]
            if chrom not in by_chrom:
                continue
            pos = int(fields[1])
            for s, e, gene in by_chrom[chrom]:
                if s <= pos <= e:
                    ref, alt = fields[3], fields[4]
                    gt = fields[9].split(":")[0] if len(fields) > 9 else ""
                    print(f"{gene}\t{chrom}\t{pos}\t{fields[2]}\t{ref}\t{alt}\t{fields[5]}\t{fields[6]}\t{fields[7]}\t{gt}")
                    break


if __name__ == "__main__":
    main()
