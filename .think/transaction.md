# Transaction Log

## 2026-06-10 — AlphaFold Documentation Cleanup

### Files Touched

| File | Action |
|------|--------|
| `doc/adv_guide/alphafold-direct-method.md` | Proofread, fixed, renamed |
| `doc/adv_guide/alphafold-db-api-access.md` | Final filename after rename |
| `doc/adv_guide/alphafold.rst` | Proofread and fixed |

---

### alphafold-direct-method.md → alphafold-db-api-access.md

**Pass 1 — Proofread & Fix**
- Title: removed space before colon
- Nobel Prize section: added blank line before "These discoveries…" paragraph
- AlphaFold 3 paragraph: fixed grammar ("Google recently released", "as a service"), spelling ("avavailabel", "pacakge"), rewrote unclear sentence, "Notably," instead of "Surprisingly that", "as of November 2024"
- P00520 comment: corrected from "Hemoglobin subunit beta" → "ABL1 tyrosine kinase"
- Literal `\n` strings in code blocks (Step 4, Step 5): removed
- Step 0: added `scipy pandas` to pip install
- Step 3: pLDDT 70–90 label corrected to "Confident"; variable renamed to `very_high_conf_residues`
- Step 4: moved `scipy` import to top of block
- Step 5: added `import pandas as pd`
- `.. important::` block: added blank line + indented bullet list (RST compliance)

**Rename**
- `alphafold-direct-method.md` → `alphafold-db-api-access.md`
- Reason: new name reflects full scope (Database + API + access workflow)

**Pass 2 — Consistency & Code Quality**
- Removed unused `import io` (Step 1)
- Removed unused `import os` (Step 4)
- Step 5: added `import requests` and `import numpy as np` (self-contained block)
- `high_conf_fraction` → `very_high_conf_fraction` (consistent with Step 3 naming)
- Step 6 "please cite" list: added all 4 references (previously skipped [2] and [4])

---

### alphafold.rst — Proofread & Fix

- Title: removed double space and space before colon; capitalized "Inference Pipeline"
- Lines 10–11: added blank line before "These discoveries…" paragraph
- Lines 13–14: applied same AlphaFold 3 paragraph grammar fixes as .md file
- Dataset section (lines 21–29): formatted 9 items as RST bullet list (`- `)
- `.. important::` blocks (×2): added blank line + proper indentation
- Datasets important: rewrote "I uploaded those" → formal path with double-backtick
- Terms of Use paragraph: "We have to agree up on" → "You must agree to"; RST link space fix
- Step 0: "Firt" → "First"; "Assumed" → "Assume"; "Alphafold" → "AlphaFold" (consistent casing)
- Step 1: "Alphafold" → "AlphaFold"; added ``double-backtick`` for filename
- Step 2: underline length fixed; "We build singularity image on /app folder" → clear description; trailing `\` spaces removed
- Line 121: "this is take time" → "this will take time"; removed 2-space indent (was rendering as RST block quote)
- Step 3: "oupput" → "output"; "CIFs are  placed" → "CIFs are placed"; "for verify structure" → "to visualize the predicted structure"; "Alphafold" → "AlphaFold"
- References: "Reference:" → "References"; duplicate `https://https://` in ref [2] URL fixed; missing space before `<` in ref [4] link fixed

---

### alphafold-db-api-access.md — Pass 3 (Hermes rewrite cleanup)

Hermes replaced the file with a "Skill Build Guide". Fixed its issues:

- Title: space before colon
- Line 24: source path updated to current filename (was `alphafold-direct-method.md`)
- Line 34: broken backtick syntax `@hermes@hermes-agent``"` → ``hermes-agent``
- Line 44: P00520 label "Hemoglobin subunit beta" → "ABL1 tyrosine kinase"
- Lines 50, 147, 155, 200: section underlines with trailing `__` → valid RST dashes
- API Endpoints table: converted from plain text to RST `list-table`; corrected wrong URLs:
  - `/api/v1/prediction/` → `/api/prediction/`
  - `confidence_score_v` → `confidence_v`
  - `.mmCIF)` → `.cif`
- Line 96: same wrong `/api/v1/` URL fixed
- Line 114: "pPLDT" → "pLDDT"
- Line 136: `'afaffold_id'` → `'alphafold_id'`
- Lines 163–181: corrupted/garbage backtick fragments replaced with clean pLDDT table
- Line 151: duplicate "et al. et al." fixed; Markdown `_Nature._` → RST `*Nature.*`
- Step 3: added `import numpy as np`; added `timeout=30` to confidence request
- Pitfall items 3 & 4 (duplicates of #2) merged; section consolidated to 3 clear pitfalls

---

### alphafold-db-api-access.md — Pass 4 (content completeness)

- Added **Executive Summary** section (top of doc) — explains research value:
  200M+ proteins, confidence metrics, free/open API, versioned reproducibility
- Added **Skill Setup** section — covers full install flow:
  - Create `~/.hermes/skills/alphafold-db/` directory
  - Create `SKILL.md` with required YAML frontmatter (name, description, version, author, license, tags)
  - Verify skill loaded: `ls` check + Hermes prompt confirmation
  - `.. important::` note on common failure causes (bad YAML, wrong filename case)
- Updated **Author** line: `Snit Sanhlao, Qwen, Claude AI`

---

### Status

- [x] `alphafold-db-api-access.md` — complete (Executive Summary, Setup, Usage, Pitfalls, Citations)
- [x] `alphafold.rst` — clean
- [ ] Sphinx build not yet run
