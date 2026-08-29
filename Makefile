PYTHON ?= python3

.PHONY: help test check all clean

help:
	@echo "Targets:"
	@echo "  make test   - run the offline unit test suite (schema, redaction-safe checker, no-controlled-data guard)"
	@echo "  make check  - alias for 'test'; run before every commit"
	@echo "  make all    - re-run the full pipeline (requires local data/ downloaded per README.md; NOT run in CI)"
	@echo "  make clean  - remove generated intermediate files under data/"

test:
	$(PYTHON) -m unittest discover -s tests -v

check: test

all:
	@echo "This target requires the controlled-access dataset in ./data (see README.md)."
	@echo "It is intentionally not run automatically (no controlled data in this repo)."
	$(PYTHON) scripts/filter_candidate_genes.py > data/candidate_variants.tsv
	$(PYTHON) scripts/annotate_candidates.py data/candidate_variants.tsv
	$(PYTHON) scripts/build_submission.py

clean:
	rm -f data/candidate_variants.tsv data/candidate_variants_annotated.tsv
	rm -rf data/snpeff_out
