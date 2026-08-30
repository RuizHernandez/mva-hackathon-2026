"""
Maps the two BUB1B compound-het variant positions (p.Leu737Ter, p.Asn1002Lys)
onto the full-length AlphaFold model of BUBR1 (UniProt O60566), colored by
per-residue pLDDT confidence, with the two mutated residues highlighted.

Uses the AlphaFold model rather than an experimental PDB structure because no
deposited crystal/cryo-EM structure of BUBR1 covers both positions (checked:
2WVI residues 57-220, 4GGD 165-476, 5JJA 29-375, 5KHU chain Q 18-308, 3SI5
67-220 — all cover only the N-terminal TPR/central region, none reach the
C-terminal pseudokinase domain where both variants sit).

Usage:
    python visualize_structure.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from Bio.PDB import PDBParser

PDB_PATH = Path(__file__).resolve().parent.parent / "data" / "AF-O60566-F1-model_v6.pdb"
OUT_PATH = Path(__file__).resolve().parent.parent / "Track 2" / "figures" / "bubr1_variants_structure.png"

VARIANTS = [
    {"resnum": 737, "marker": "1", "label": "1 — p.Leu737Ter (stop-gained, ClinVar pathogenic)"},
    {"resnum": 1002, "marker": "2", "label": "2 — p.Asn1002Lys (missense, novel, SIFT/PolyPhen deleterious)"},
]


def main():
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("BUB1B_AF", str(PDB_PATH))
    chain = structure[0]["A"]

    coords, plddt, resnums = [], [], []
    for res in chain:
        if res.id[0] != " " or "CA" not in res:
            continue
        ca = res["CA"]
        coords.append(ca.get_coord())
        plddt.append(ca.get_bfactor())  # AlphaFold stores pLDDT in the B-factor column
        resnums.append(res.id[1])
    coords = np.array(coords)
    resnums = np.array(resnums)
    plddt = np.array(plddt)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    sc = ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], c=plddt, cmap="viridis",
                     s=8, alpha=0.65, vmin=0, vmax=100)
    ax.plot(coords[:, 0], coords[:, 1], coords[:, 2], color="gray", linewidth=0.4, alpha=0.3)

    for v in VARIANTS:
        idx = np.where(resnums == v["resnum"])[0]
        if len(idx) == 0:
            continue
        x, y, z = coords[idx[0]]
        ax.scatter([x], [y], [z], color="red", s=160, edgecolor="black", linewidth=1.2, zorder=10)
        ax.text(x, y, z, "  " + v["marker"], fontsize=13, fontweight="bold", color="black", zorder=11)

    cbar = fig.colorbar(sc, ax=ax, shrink=0.6, pad=0.1)
    cbar.set_label("AlphaFold pLDDT (per-residue confidence)")

    plddt_737 = plddt[np.where(resnums == 737)[0][0]]
    plddt_1002 = plddt[np.where(resnums == 1002)[0][0]]

    ax.set_title(
        "BUBR1 (BUB1B, UniProt O60566) — AlphaFold model\n"
        "Proband compound-het variant positions\n"
        f"pLDDT at 737 = {plddt_737:.1f} | pLDDT at 1002 = {plddt_1002:.1f}",
        fontsize=11,
    )
    ax.set_xlabel("X (Å)")
    ax.set_ylabel("Y (Å)")
    ax.set_zlabel("Z (Å)")

    legend_text = "\n".join(v["label"] for v in VARIANTS)
    fig.text(0.02, 0.02, legend_text, fontsize=9, va="bottom", ha="left")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=200, bbox_inches="tight")
    print(f"Saved: {OUT_PATH}")
    print(f"pLDDT at Leu737: {plddt_737:.1f}")
    print(f"pLDDT at Asn1002: {plddt_1002:.1f}")


if __name__ == "__main__":
    main()
