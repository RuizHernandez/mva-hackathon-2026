# Rare Disease, Real Kid: MVA Hackathon 2026

Proyecto para participar en el [MVA Hackathon 2026](https://sagebio-rare-disease-real-kid-mva-hackathon-2026.hf.space/)
(SageBio + MVA Society + Hugging Face + BEACON). Caso real de un niño con
**Mosaic Variegated Aneuploidy (MVA)**, enfermedad ultra-rara sin tratamiento
establecido (<50 casos descritos).

- Dataset (gated): https://huggingface.co/datasets/SageBio/mva-hackathon-2026-data
- Submissions: 25 ago – 24 oct 2026 (23:59 UTC)
- Licencia de resultados: CC BY 4.0 · Licencia de datos crudos: uso restringido al hackathon, borrar al finalizar

## Tracks

### Track 1 — Variant Prediction
Dado el genoma del niño (FASTQ + VCF, GRCh38) y su fenotipo clínico, rankear
hasta 10 variantes candidatas (o pares compound-het) por probabilidad causal.

**Entregable:** CSV de predicciones + reporte de metodología (PDF/MD) + repo GitHub.
Máx. 6 envíos. Solo cuenta el de mejor score en el leaderboard.

Columnas del CSV (`submissions/track1/`):

| Campo | Tipo | Descripción |
|---|---|---|
| proband_id | string | ID del proband (del dataset) |
| chrom_1 | string | Cromosoma variante 1 (ej. chr15) |
| pos_1 | int | Posición GRCh38 |
| ref_1 | string | Alelo referencia |
| alt_1 | string | Alelo alternativo |
| chrom_2/pos_2/ref_2/alt_2 | — | Segunda variante (solo compound-het), vacío si no aplica |
| epcr | float (0,1] | Probabilidad causal estimada (ranking propio) |
| finding_type | string | `primary` o `secondary` |
| notes | string | Racional opcional |

Scoring automático: **rank points** (100pts si el top-1 es correcto, parcial si
está en el top-10, mitad si solo aciertas una de un par compound-het) + **F-max**
(mejor balance precisión/recall). El reporte de metodología lo evalúa un panel
(no es automático).

### Track 2 — Drug Repurposing
Caracterizar el mecanismo del/los gen(es) candidato(s) (LoF/GoF, vía afectada)
y proponer fármacos ya aprobados reposicionables.

**Entregable:** reporte (PDF/MD) + repo GitHub + video pitch de 3 min (YouTube/Vimeo).
Máx. 3 envíos, solo se revisa el último. Evaluación 100% panel de jueces:
rigor científico 35%, impacto potencial 25%, innovación 25%, escalabilidad 15%.

## Reglas clave a recordar

- Coordenadas siempre en **GRCh38**.
- Si se usa un LLM/asistente de IA, documentar en el reporte: proveedor, plan/tier
  y manejo de datos (ej. "Anthropic API, Claude Sonnet, términos comerciales,
  sin entrenamiento con contenido del cliente").
- El repo de GitHub puede quedar privado durante el hackathon, pero debe hacerse
  público al finalizar para que el jurado lo revise.
- Nombrar los archivos de submission con usuario/equipo + nombre del enfoque,
  ej. `jane-doe_gatk-haplotype.csv`, `jane-doe_track1_report.pdf`.
- Datos gated: requieren cuenta de Hugging Face propia + aceptar las Hackathon
  Rules / Data Transfer Agreement en la página del dataset (protocolo WCG IRB
  #20252010). Prohibido redistribuir; borrar al concluir el hackathon.

## Entorno

Reutilizamos el entorno `venv-bio` de `E:\2026 Escritorio\Entorno` (Python 3.12,
CUDA disponible). Paquetes relevantes ya instalados: `biopython`, `pandas`,
`numpy`, `scikit-learn`, `xgboost`, `shap`, `networkx`, `gseapy`, `rdkit`,
`torch`/`transformers`, `huggingface_hub`, `gget`, `pyvcf3`.

> `cyvcf2`/`pysam` no compilan en Windows nativo (requieren htslib). WSL Ubuntu
> ya tiene `bcftools`/`samtools`/`tabix`/`build-essential` instalados (se usó
> para la validación cruzada con `bcftools csq`, ver reporte de Track 1).

Activar entorno (PowerShell):

```powershell
& "E:\2026 Escritorio\Entorno\venv-bio\Scripts\Activate.ps1"
```

## Herramientas de investigación disponibles

Conectadas en esta sesión (vía MCP): Open Targets (asociación gen-enfermedad),
ChEMBL (mecanismo de fármacos/dianas — clave para Track 2), PubMed, bioRxiv,
ClinicalTrials.gov, Consensus.

## Estado / Próximos pasos

- [x] Explorar reglas del hackathon y formato de submission
- [x] Preparar entorno y estructura del proyecto
- [x] Login de Hugging Face y acceso al dataset concedido
- [x] Descargar README, fenotipo clínico, VCF + índice (FASTQ pendientes, no
      necesarios para Track 1 salvo que se quiera re-llamar variantes)
- [x] Caso confirmado como singleton (un solo proband: `WGS_EX2312012`, sin trío)
- [x] Pipeline de filtrado/priorización dirigido por fenotipo (panel de 13 genes
      candidatos de MVA/inestabilidad cromosómica) + anotación vía Ensembl VEP REST
- [x] **Hallazgo primario**: compuesto heterocigoto en BUB1B
      (chr15:40209701 T>G stop_gained patogénico en ClinVar +
      chr15:40220612 T>G missense novedoso deletéreo) — ver
      [reports/track1/IHRH_track1_report.md](reports/track1/IHRH_track1_report.md)
- [x] CSV de submission generado:
      [submissions/track1/IHRH_bub1b-compound-het.csv](submissions/track1/IHRH_bub1b-compound-het.csv)
- [x] Comparado contra el leaderboard público: ≥20 equipos independientes
      llegaron al mismo par BUB1B, confirmación cruzada fuerte
- [x] Añadida cita OMIM #257300, script `scripts/check_target_calls.py`
      (verificación redaction-safe de las 2 posiciones, sin exponer el resto
      del VCF) y mención del ángulo complementario de proteostasis/arimoclomol
      en Track 2
- [x] Escaneo genómico completo real (alternativa a bcftools que sí corre en
      Windows nativo: SnpEff 4.3t + GRCh38.86 sobre JRE portátil de Temurin,
      sin necesitar WSL/sudo). Resultado: BUB1B es la única variante de todo
      el genoma que combina rareza + ClinVar patogénico + coincidencia
      fenotípica. Además salieron 2 hallazgos secundarios (LZTR1, MAGI2) ya
      añadidos al CSV.
- [x] `Makefile` (`make test`/`check`/`all`/`clean`) + suite de tests
      (`tests/`, 7/7 pasan) + `docs/reproducibility.md` documentando el
      límite de qué datos nunca salen de la máquina local
- [x] Visualización 3D de las 2 variantes sobre el modelo AlphaFold de BUBR1
      (`Track 2/figures/bubr1_variants_structure.png`), referenciada en
      ambos reportes — ningún competidor revisado hizo esto
- [x] Tercera validación cruzada independiente con `bcftools csq` (WSL,
      Ensembl GRCh38.116) — coincide exactamente con VEP REST y SnpEff en
      los 4 hallazgos (BUB1B×2, LZTR1, MAGI2)
- [x] Repo de GitHub privado creado y pusheado:
      [github.com/RuizHernandez/mva-hackathon-2026](https://github.com/RuizHernandez/mva-hackathon-2026)
- [x] Confirmado username real de HF (`IHRH`) y renombrados todos los archivos
      de submission/reportes
- [x] Track 2: mecanismo de BUB1B-MVA caracterizado + candidatos de
      reposicionamiento (bosutinib, metformina) con evidencia de ChEMBL/Elicit/STRING/Reactome/cBioPortal
- [x] **Track 1 subido y evaluado**: Rank points 100.0/100, F-max 1.000,
      "Full match at rank 1" (proband_id correcto: `PROBAND01`, no el nombre
      de muestra del VCF — lección aprendida, corregido y documentado)
- [ ] Subir submission en "Submit - Track 2" del Space (pendiente: requiere
      video pitch)
- [ ] Grabar y subir el video pitch de 3 min (guion listo en
      `Track 2/pitch_video_script.md`)
- [ ] Hacer público el repo de GitHub (solo después de que cierre el
      hackathon, 24 oct 2026)

## Estructura

```
data/          # datos crudos descargados (gitignored)
scripts/       # pipeline de descarga, filtrado, anotación de variantes
notebooks/     # exploración
reports/       # borradores de reportes de metodología (track1/track2)
submissions/   # CSVs y archivos finales a subir
```
