# Track 1 Methods Report — MVA Hackathon 2026

**Team / participant:** ihruizh (verify against actual Hugging Face username before submitting)
**Proband:** WGS_EX2312012 (singleton WGS, GRCh38, no parental samples provided)

## 1. Clinical phenotype summary

From `Challenge_Clinical_Phenotype_1.docx`:

| Feature | HPO ID |
|---|---|
| Rhabdomyosarcoma | HP:0002859 |
| Nephrocalcinosis | HP:0000121 |
| Short stature | HP:0004322 |
| Failure to thrive / skeletal muscle atrophy | HP:0001508 / HP:0003202 |
| Premature birth (32 weeks) | HP:0001622 |
| Small for gestational age / IUGR (~1kg birth weight) | HP:0001518 |
| Parental recurrent miscarriages | HP:0200067 |

The combination of an embryonal malignancy (rhabdomyosarcoma) with severe intrauterine
growth restriction, failure to thrive, and a parental history of recurrent pregnancy
loss is the classic constellation associated with **Mosaic Variegated Aneuploidy (MVA)
/ Premature Chromatid Separation (PCS) syndrome**, a chromosomal instability disorder.

## 2. Approach

1. **Candidate gene panel, phenotype-driven, then genome-wide confirmation.**
   `cyvcf2`/`pysam` require a compiled htslib not buildable on this Windows
   workstation without a WSL toolchain, so we first prioritized a targeted
   panel: the three established MVA genes (**BUB1B**, **CEP57**, **TRIP13**),
   then expanded to mitotic-checkpoint / kinetochore genes and other recessive
   chromosomal-instability-with-cancer-predisposition genes that overlap the
   phenotype differentially (**BUB1**, **BUB3**, **MAD1L1**, **MAD2L1**,
   **CENPE**, **CEP57L1**, **BLM**, **NBN**, **ATM**, **ATR**). We then closed
   the gap to a true unbiased scan using a portable Java runtime + **SnpEff
   4.3t (GRCh38.86)**, which installs natively on Windows without a compiled
   htslib: the entire genome (~5.01M variant records) was annotated, filtered
   to `FILTER=PASS` + HIGH impact (frameshift/stop-gained/stop-lost/start-lost/
   splice donor-acceptor) + non-reference genotype (1,250 variants
   genome-wide), then cross-checked against gnomAD frequency and ClinVar via
   Ensembl VEP REST. See Section 4 for the result of that genome-wide pass.
2. **Coordinate resolution.** GRCh38 gene coordinates pulled from Ensembl
   (release 116) via `gget`.
3. **Region extraction.** Linear parse of the proband's GATK-called germline
   VCF (`WGS_EX2312012_HGWCNDSX7.vcf.gz`), pulling all records within each
   gene ± 20kb, restricted to `FILTER=PASS`. ~2,500 variants across the 13-gene
   panel.
4. **Functional annotation.** Ensembl VEP REST API (GRCh38), batched, pulling
   consequence, impact, SIFT/PolyPhen, gnomAD allele frequency, and ClinVar
   clinical significance for colocated known variants.
5. **Triage.** Filtered to variants with a protein-altering consequence
   (missense/LoF/splice) AND rare or absent from gnomAD (AF < 0.001) or with a
   pathogenic ClinVar classification.

## 3. Primary finding

**Compound heterozygous candidate in *BUB1B* (ENSG00000156970, canonical
transcript ENST00000287598):**

| | Variant 1 | Variant 2 |
|---|---|---|
| GRCh38 | chr15:40,209,701 T>G | chr15:40,220,612 T>G |
| HGVSc | c.2210T>G | c.3006T>G |
| HGVSp | p.Leu737Ter | p.Asn1002Lys |
| Consequence | stop_gained (HIGH) | missense_variant (MODERATE) |
| In silico | — | SIFT: deleterious (0.01); PolyPhen: probably_damaging (0.997) |
| gnomAD AF | 7.867e-05 | absent (not in gnomAD) |
| ClinVar | Pathogenic / Likely pathogenic (VCV000533901, rs759242053) | not previously reported |
| Literature | Cited in Hanks et al. 2004, *Nat Genet*, PMID 15475955 — the original report establishing biallelic BUB1B mutations as the cause of MVA/PCS syndrome | — |
| Genotype (proband) | 0/1 | 0/1 |

**Structural context:** both residues were mapped onto the full-length
AlphaFold model of BUBR1 (UniProt O60566; no deposited experimental
structure covers both positions — the available crystal/cryo-EM structures
of BUB1B, e.g. 2WVI, 3SI5, 4GGD, 5JJA, 5KHU, only resolve the N-terminal
TPR/central region, residues ≤476). Leu737 falls in a moderate-to-high
confidence region (pLDDT 73.6) and Asn1002 in a very-high-confidence region
(pLDDT 91.1) of the C-terminal pseudokinase domain, supporting that the
missense variant sits in a well-folded, likely functionally important part
of the protein rather than a disordered region. See
[../../Track 2/figures/bubr1_variants_structure.png](../../Track%202/figures/bubr1_variants_structure.png)
(generated with `scripts/visualize_structure.py`).

**Interpretation:** biallelic (compound heterozygous) loss of BUB1B function
causes **Mosaic Variegated Aneuploidy type 1** (OMIM #257300; autosomal
recessive), a mitotic
spindle-assembly-checkpoint disorder causing chromosomal instability, childhood
cancer predisposition (Wilms tumor, rhabdomyosarcoma), growth restriction, and
is compatible with recurrent early pregnancy loss in carrier couples (consistent
with the family history reported here). This matches the proband's phenotype
closely.

BUB1B encodes BUBR1, a core mitotic spindle-assembly-checkpoint kinase. The
literature establishes a **dosage-dependent mechanism**: residual BUBR1 below
~50% of normal is sufficient to cause premature chromatid separation, and
further reduction produces overt aneuploidy (Bohers et al. 2008, *Hum Genet*,
PMID 18932004; Matsuura et al. 2006, *AJMG*, PMID 16411201). This explains why
MVA1 is typically caused by a **null allele in trans with a hypomorphic
allele** rather than two fully null alleles (which would likely be embryonic
lethal) — directly consistent with our finding of one clear loss-of-function
allele (stop-gained, ClinVar pathogenic) paired with a missense allele
predicted damaging but not fully null.

Multiple independent case reports describe the same architecture — one
truncating/frameshift BUB1B allele plus one missense/hypomorphic allele,
each inherited from a different parent — in children presenting with MVA1 and
malignancy or severe growth restriction, closely mirroring this proband:
- He et al. 2018 (PMID 30512160): compound heterozygous BUB1B
  (frameshift + p.Arg814His missense), growth retardation, renal
  involvement.
- Qu et al. 2025 (PMID 40555658): compound heterozygous BUB1B
  (frameshift + missense, one paternal/one maternal), confirmed by parental
  Sanger sequencing and parental PCS karyotyping — the kind of segregation
  study that would be the natural confirmatory next step for this case if
  parental samples become available.
- Pavone et al. 2022 (PMID 35804254): genotype–phenotype reappraisal
  reviewing ~31 published MVA1 cases, reinforcing IUGR/growth restriction and
  malignancy as core, recurrent features.
- Hanks et al. 2006 (PMID 16182441, *Cancer Letters*): BUB1B mutation
  analysis specifically in childhood cancers arising in MVA syndrome,
  directly supporting the rhabdomyosarcoma link in this proband.

**Limitation / assumption to flag for the judging panel:** this is a singleton
WGS (no parental samples), and the VCF does not carry read-backed phasing
(`PID`/`PGT`) at either position, so *trans* configuration (one variant per
allele) is inferred, not directly confirmed. Two independent rare/novel
deleterious variants co-occurring on the same single allele by chance is
unlikely, and one of the two is an established pathogenic allele, which
supports the compound-het interpretation — but formal confirmation would
require parental Sanger/segregation testing or long-read phasing.

## 4. Ruled-out candidates and genome-wide confirmation

The expanded 13-gene panel scan (~2,500 PASS variants annotated) returned no
other rare, protein-altering, or pathogenic-classified variant of comparable
strength. Two borderline hits were reviewed and excluded:
- *ATM* p.Ser978Pro — heterozygous only, ClinVar conflicting
  (benign/likely-benign/VUS), gnomAD AF ~8×10⁻⁴ (too common for this
  presentation).
- A variant near *MRM2* — picked up only due to padding overlap with the
  *MAD1L1* region; gene/phenotype unrelated to MVA.

We then went beyond the candidate-gene panel and ran a genuine **genome-wide**
pass (SnpEff GRCh38.86, all ~5.01M variant records; see Section 1) to check
whether anything anywhere in the genome scores higher than BUB1B. Restricting
to `FILTER=PASS`, HIGH impact (frameshift / stop-gained / stop-lost /
start-lost / splice donor-acceptor), and a non-reference genotype yielded
1,250 variants. Cross-referencing all 1,250 against gnomAD frequency and
ClinVar (Ensembl VEP REST) shows that **BUB1B c.2210T>G is the only
genome-wide HIGH-impact variant that is simultaneously (a) rare
(gnomAD AF < 10⁻⁴), (b) ClinVar pathogenic/likely-pathogenic, and (c)
consistent with the proband's phenotype.** No other candidate combines all
three properties — this is the strongest evidence in this report that BUB1B
is correct, independent of the phenotype-first reasoning in Sections 1–3.

As a third, independent cross-check, we additionally ran **`bcftools csq`**
(v1.22, htslib 1.22.1) with the Ensembl GRCh38.116 reference FASTA + GFF3 —
a completely different annotation engine/database pairing from both the
Ensembl VEP REST API and SnpEff used above. On the canonical transcripts, it
reproduces, independently, exactly the same gene, consequence, and
amino-acid change for all findings in this report:
`BUB1B|ENST00000287598|stop_gained|737L>737*`,
`BUB1B|ENST00000287598|missense|1002N>1002K`,
`LZTR1|...|stop_gained|748Y>748*`, and `MAGI2|ENST00000522342|stop_gained|180Q>180*`.
Three independent tool/database combinations now agree exactly on all four
variants reported here.

## 5. Secondary / incidental findings

Two heterozygous findings from the genome-wide HIGH-impact scan are reported
as secondary/incidental (not proposed as the primary cause; included per the
submission format, which welcomes these and does not penalize the automated
score):

- ***LZTR1* p.Tyr748Ter** (chr22:20996720 C>G), gnomAD AF ≈ 1.4×10⁻⁶
  (ultra-rare), ClinVar includes pathogenic/likely-pathogenic entries.
  Biallelic or monoallelic LZTR1 loss-of-function causes LZTR1-related Noonan
  syndrome (a RASopathy) and schwannomatosis. Flagged specifically because
  RASopathies (Noonan, Costello syndrome) are a recognized differential for
  rhabdomyosarcoma predisposition — worth keeping in mind if BUB1B were ever
  reconsidered, though it is a clearly weaker candidate (no phenotype
  overlap beyond the cancer risk, no second hit, and BUB1B has direct
  ClinVar + literature support this variant lacks).
- ***MAGI2* p.Gln180Ter** (chr7:78158312 G>A), absent from gnomAD. MAGI2
  biallelic loss-of-function causes autosomal recessive nephrotic
  syndrome/FSGS. Only one damaged allele was found genome-wide (no
  compound-het partner), so this cannot be causal on its own under a
  recessive model — flagged only because the proband has nephrocalcinosis,
  in case a second hit (e.g. structural or deep intronic, outside this
  scan's scope) is found later.

A formal ACMG SF v3.2 actionable-secondary-findings screen was not run
separately; the two findings above emerged naturally from the genome-wide
HIGH-impact pass described in Section 4.

## 6. Tools & environment

- Python 3.12, `gget` (Ensembl gene coordinates), Ensembl VEP REST API
  (GRCh38, public endpoint) for variant annotation and gnomAD/ClinVar
  cross-referencing.
- **SnpEff 4.3t (database GRCh38.86)** for genome-wide consequence
  annotation, run under a portable Eclipse Temurin JRE 17 — installs
  natively on Windows without a compiled htslib, unlike `bcftools`/
  `cyvcf2`/`pysam`.
- Redaction-safe check: `scripts/check_target_calls.py` re-verifies the
  genotype at exactly the two nominated BUB1B positions without emitting
  sample name, depth, quality, or any other variant from the VCF.
- `bcftools csq` (1.22, installed via WSL Ubuntu `apt`, no admin/root needed
  beyond the one-time package install) with Ensembl GRCh38.116 FASTA+GFF3,
  as a third independent annotation cross-check. Note: a genome-wide run
  crashed (exit 255) under the default `--phase r` (require-phased) mode on
  this unphased singleton VCF instead of erroring cleanly; re-running with
  `--phase a` on the relevant regions resolved it — flagging this in case it
  helps another team hit the same issue.
- **AI assistance disclosure:** Claude Code (Anthropic API, Claude Sonnet
  model, commercial/API terms — no training on customer content) was used as
  an interactive coding and analysis assistant throughout: writing the VCF
  filtering/annotation scripts, querying Ensembl/VEP, and drafting this
  report. All genomic interpretation claims above (ClinVar status, gnomAD
  frequencies, literature citation) were pulled from live API responses, not
  generated from the model's internal knowledge.

## 7. Reproducibility

Code: `scripts/filter_candidate_genes.py`, `scripts/annotate_candidates.py`,
`scripts/build_submission.py` in the accompanying GitHub repository
(add repo URL before submitting).

## 8. References

1. Hanks S, et al. Constitutional aneuploidy and cancer predisposition caused
   by biallelic mutations in BUB1B. *Nat Genet.* 2004. PMID: 15475955.
2. Matsuura S, et al. Monoallelic BUB1B mutations and defective
   mitotic-spindle checkpoint in seven families with premature chromatid
   separation (PCS) syndrome. *Am J Med Genet A.* 2006. PMID: 16411201.
3. Bohers É, et al. Gradual reduction of BUBR1 protein levels results in
   premature sister-chromatid separation then in aneuploidy. *Hum Genet.*
   2008. PMID: 18932004.
4. Hanks S, et al. Comparative genomic hybridization and BUB1B mutation
   analyses in childhood cancers associated with mosaic variegated aneuploidy
   syndrome. *Cancer Lett.* 2006. PMID: 16182441.
5. He T, et al. [Clinical features and genetic analysis of a child with
   mosaic variegated aneuploidy syndrome]. *Zhonghua Yi Xue Yi Chuan Xue Za
   Zhi.* 2018. PMID: 30512160.
6. Qu J, et al. [Genetic analysis of two fetuses with Mosaic variegated
   aneuploidy syndrome caused by compound heterozygous variants in BUB1B].
   *Zhonghua Yi Xue Yi Chuan Xue Za Zhi.* 2025. PMID: 40555658.
7. Pavone P, et al. Pathogenic correlation between mosaic variegated
   aneuploidy 1 (MVA1) and a novel BUB1B variant: a reappraisal of a severe
   syndrome. *Neurol Sci.* 2022. PMID: 35804254.
8. Hanks S, Rahman N. Aneuploidy-cancer predisposition syndromes: a new link
   between the mitotic spindle checkpoint and cancer. *Cell Cycle.* 2005.
   PMID: 15655355.
9. OMIM #257300 — Mosaic Variegated Aneuploidy Syndrome 1; MVA1.
   https://omim.org/entry/257300

*Literature identified via the Elicit academic search API (semantic search
over its indexed corpus), cross-checked against ClinVar/PubMed identifiers
returned by Ensembl VEP.*
