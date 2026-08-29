# Reproducibility & data boundary

## What never leaves the local machine

Per the Hackathon Rules and Data Transfer Agreement (WCG IRB protocol
#20252010), the following are **never** committed to this repository and
must be deleted from local compute once the hackathon concludes:

- `data/*.vcf.gz`, `data/*.vcf.gz.tbi` — the proband's raw variant calls
- `data/*fastq.gz` — raw sequencing reads (not downloaded in this project;
  not needed since a pre-called VCF was provided)
- `data/Challenge_Clinical_Phenotype_1.docx` — the clinical phenotype
  document, marked "Confidential — Do not redistribute" in its own text
- `data/snpeff_out/` — SnpEff's genome-wide annotated VCF (derived
  directly from the controlled VCF; same restriction applies)
- `.env` — local secrets (API keys)

All of the above are excluded via `.gitignore`. `tests/test_no_controlled_data_tracked.py`
enforces this automatically: it runs `git ls-files` and fails if any tracked
file matches a controlled-data or secret-file pattern. Run `make test`
before every commit.

## What is safe to share (and is committed here)

- All scripts (`scripts/*.py`) — they take a local file path as input and
  contain no patient data themselves.
- The submission CSV (`submissions/track1/*.csv`) and both reports — these
  only contain the specific variant coordinates and clinical summary the
  hackathon organizers already require in the public submission format and
  the released phenotype summary; nothing beyond what the challenge itself
  asks participants to report.
- The BUBR1 structure figure (`Track 2/figures/*.png`) — derived from a
  public AlphaFold model (UniProt O60566), not from patient data.

## How to reproduce

1. Request and download the dataset yourself (gated; requires accepting the
   Hackathon Rules) — see `scripts/download_data.py` and the main
   `README.md`.
2. Install dependencies: `pip install -r requirements.txt`. A Java runtime
   is additionally required for the genome-wide SnpEff step (any JRE 11+;
   a portable one works, no admin/install needed).
3. Run `make all` — this re-runs candidate-gene filtering, VEP REST
   annotation, and CSV generation. The genome-wide SnpEff pass and the
   3D structure figure are separate one-off scripts
   (`scripts/annotate_genomewide_highimpact.py`,
   `scripts/visualize_structure.py`) not wired into `make all` because they
   need the SnpEff/JRE toolchain and the downloaded AlphaFold PDB file
   respectively — see each script's docstring for exact steps.
4. Run `make test` (or `make check`) — offline, no controlled data needed —
   to validate the submission schema, the redaction-safe checker logic
   (against synthetic fixtures only), and the no-controlled-data guard.
