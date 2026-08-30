# Track 2 Pitch Video Script (~3 minutes)

Target: ~420-450 spoken words at a natural pace (~145 wpm). Timestamps are
guides, not hard cuts — adjust to your own delivery. Bracketed lines are
stage/visual directions, not spoken.

---

**[0:00–0:20] Hook**
[Visual: title card — "BUB1B-MVA: from a diagnosis to a drug repurposing hypothesis"]

> This project starts with a real child living with Mosaic Variegated
> Aneuploidy — an ultra-rare disease with no approved treatment. In Track 1,
> we found a likely causal genetic diagnosis. This pitch is about what we can
> do with that diagnosis: two already-approved drugs worth investigating,
> chosen because of exactly how this disease breaks a cell, not by guessing.

**[0:20–0:50] The diagnosis, briefly**
[Visual: the two-variant table from the Track 1 report]

> The proband carries two damaged copies of BUB1B — one is a known
> pathogenic stop-gained variant already in ClinVar, the other a novel
> missense variant predicted deleterious by SIFT and PolyPhen. BUB1B encodes
> BUBR1, a core protein of the mitotic spindle checkpoint — the quality
> control system that stops a cell from dividing until every chromosome is
> properly attached.

**[0:50–1:30] The mechanism**
[Visual: the causal-chain diagram: LOF → reduced BUBR1 → weakened checkpoint → premature chromatid separation → aneuploidy → CIN → cancer risk]

> When BUBR1 drops below a functional threshold, cells can no longer reliably
> hold the checkpoint. Chromosomes separate too early, cells end up with the
> wrong chromosome number, and that instability — repeated across a
> lifetime of cell divisions — is what predisposes these children to cancers
> like rhabdomyosarcoma. We confirmed this isn't just one paper's claim: we
> pulled the interaction network from STRING and the pathway data from
> Reactome, and BUB1B sits at the center of exactly this checkpoint module,
> independently, in both databases.

**[1:30–2:20] The repurposing candidates**
[Visual: two drug cards, side by side — Bosutinib / Metformin]

> So the question for Track 2 isn't "how do we fix the checkpoint" — it's
> "given a cell that already has a weak checkpoint, what already-approved
> drug exploits that weakness?" We found two candidates, each backed by a
> specific mechanistic study, not a hunch. Bosutinib, an approved leukemia
> drug, was shown in an independent screen to be selectively toxic to cells
> with a defective spindle checkpoint — exactly this cell's biology.
> Metformin, one of the most widely used and safest drugs in the world, was
> shown in a separate screen to selectively stress aneuploid cells through
> the AMPK energy-sensing pathway. Both are cheap, generic, and already
> deeply characterized in humans — which matters enormously for an
> ultra-rare disease with no dedicated drug pipeline. And just as
> important: we explicitly ruled out a whole class of drugs — checkpoint
> inhibitors already in cancer development — because in this patient they'd
> push in exactly the wrong direction.

**[2:20–2:35] Structural confirmation (new slide 5)**
[Visual: PDB 4MXO — bosutinib bound to Src kinase]

> We didn't stop at a mechanistic argument — we checked whether bosutinib
> actually engages its target. PDB entry 4MXO is a solved co-crystal
> structure of bosutinib bound to human Src kinase, the exact mechanism
> Schukken et al. showed to be selectively toxic in checkpoint-deficient
> cells. A separate solved structure confirms it also binds Abl kinase.
> That's stronger evidence than a docking prediction — it's a structure
> someone has actually solved.

**[2:35–2:50] Why this matters beyond one child**
[Visual: "1 child → 3 MVA genes → CIN+ tumors broadly"]

> This mechanism isn't unique to this one mutation. It generalizes to the
> other two known MVA genes, and to chromosomally unstable tumors more
> broadly — the same vulnerability has independently shown up in
> glioblastoma and prostate cancer research. The pipeline we used —
> phenotype, to mechanism, to literature-mined approved drugs — is reusable
> for the next undiagnosed case, not just this one.

**[2:50–3:00] Close**
[Visual: contact / repo link]

> These are hypotheses for follow-up, not proven treatments — validating
> them in this child's own cells is the obvious next step. But for a family
> that had no genetic answer six weeks ago, we think this is a real,
> testable place to start.

---

## Production notes

- Keep the two visuals (variant table, mechanism diagram) on screen long
  enough to read — don't rely on narration alone for the technical claims.
- If recording in Spanish instead of English, keep the same structure;
  I can produce a Spanish version on request — just ask.
- Every specific claim above (ClinVar status, SIFT/PolyPhen, STRING/Reactome
  results, the two drugs' approval status and mechanism papers) is already
  documented with citations in `IHRH_track2_report.md` — cite the report
  in the video description for judges who want the sources.
