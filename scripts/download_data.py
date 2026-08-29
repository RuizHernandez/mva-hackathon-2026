"""
Descarga el dataset del MVA Hackathon 2026 desde Hugging Face.

Requiere estar logueado en Hugging Face (`hf auth login`) o tener la variable
de entorno HF_TOKEN definida, con acceso ya concedido al dataset gated
SageBio/mva-hackathon-2026-data.

Uso:
    python download_data.py            # descarga todo (~85GB)
    python download_data.py --list     # solo lista los archivos disponibles
    python download_data.py --file WGS_EX2312012_HGWCNDSX7.vcf.gz
"""

import argparse
import sys
from pathlib import Path

from huggingface_hub import HfApi, hf_hub_download, snapshot_download

REPO_ID = "SageBio/mva-hackathon-2026-data"
REPO_TYPE = "dataset"
LOCAL_DIR = Path(__file__).resolve().parent.parent / "data"


def list_files():
    api = HfApi()
    files = api.list_repo_files(repo_id=REPO_ID, repo_type=REPO_TYPE)
    for f in files:
        print(f)
    return files


def download_file(filename: str):
    path = hf_hub_download(
        repo_id=REPO_ID,
        filename=filename,
        repo_type=REPO_TYPE,
        local_dir=str(LOCAL_DIR),
    )
    print(f"Descargado: {path}")


def download_all():
    path = snapshot_download(
        repo_id=REPO_ID,
        repo_type=REPO_TYPE,
        local_dir=str(LOCAL_DIR),
        ignore_patterns=["README.md", ".gitattributes"],
    )
    print(f"Dataset descargado en: {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="Solo listar archivos del dataset")
    parser.add_argument("--file", type=str, default=None, help="Descargar un solo archivo por nombre")
    args = parser.parse_args()

    try:
        if args.list:
            list_files()
        elif args.file:
            download_file(args.file)
        else:
            download_all()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        print(
            "\nAsegúrate de haber iniciado sesión con `hf auth login` y de "
            "tener acceso concedido al dataset en "
            "https://huggingface.co/datasets/SageBio/mva-hackathon-2026-data",
            file=sys.stderr,
        )
        sys.exit(1)
