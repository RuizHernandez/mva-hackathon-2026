"""
Visualizes the experimentally solved co-crystal structure of bosutinib bound
to human Src kinase (PDB 4MXO) -- direct structural evidence supporting the
Track 2 repurposing rationale (Schukken et al. 2020: Src-kinase inhibition is
synergistically toxic to spindle-checkpoint-deficient cells), stronger than
a computational docking prediction since this is a solved X-ray structure.

Usage:
    python visualize_bosutinib_src.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from Bio.PDB import PDBParser

PDB_PATH = Path(__file__).resolve().parent.parent / "data" / "4MXO.pdb"
OUT_PATH = Path(__file__).resolve().parent.parent / "Track 2" / "figures" / "bosutinib_src_cocrystal.png"

LIGAND_CODE = "DB8"  # bosutinib, as deposited in PDB 4MXO


def main():
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("SRC_BOSUTINIB", str(PDB_PATH))
    chain = structure[0]["A"]

    ca_coords = []
    ligand_atoms = []
    for res in chain:
        if res.id[0] == " " and "CA" in res:
            ca_coords.append(res["CA"].get_coord())
        elif res.resname == LIGAND_CODE:
            for atom in res:
                ligand_atoms.append(atom.get_coord())

    ca_coords = np.array(ca_coords)
    ligand_atoms = np.array(ligand_atoms)

    fig = plt.figure(figsize=(9, 8))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot(ca_coords[:, 0], ca_coords[:, 1], ca_coords[:, 2],
            color="#9CB8B5", linewidth=1.2, alpha=0.85, zorder=1)
    ax.scatter(ca_coords[:, 0], ca_coords[:, 1], ca_coords[:, 2],
               color="#028090", s=6, alpha=0.5, zorder=1)

    ax.scatter(ligand_atoms[:, 0], ligand_atoms[:, 1], ligand_atoms[:, 2],
               color="#D62828", s=60, edgecolor="black", linewidth=0.4, zorder=10,
               label="Bosutinib (bound, PDB 4MXO)")

    ax.set_title(
        "Bosutinib bound to human Src kinase\n"
        "Experimentally solved co-crystal structure (PDB 4MXO, Src chain A)\n"
        "Direct structural evidence for the proposed mechanism (Schukken et al. 2020)",
        fontsize=10.5,
    )
    ax.set_xlabel("X (Å)")
    ax.set_ylabel("Y (Å)")
    ax.set_zlabel("Z (Å)")
    ax.legend(loc="upper left", fontsize=9)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=200, bbox_inches="tight")
    print(f"Saved: {OUT_PATH}")
    print(f"Src chain A residues (CA): {len(ca_coords)}")
    print(f"Bosutinib (DB8) atoms: {len(ligand_atoms)}")


if __name__ == "__main__":
    main()
