# AlphaFold DB Skill: Build Guide and Usage Manual


**Created:** 2026-06-10 **Last updated:** 2026-06-10 (rev 2 — Claude Code skill, BioPython fix, P12931 gate)

**Author:** Snit Sanghlao, Qwen, Claude AI


## Executive Summary
AlphaFold DB holds predicted 3D structures for over **200 million proteins** — the largest publicly available structural dataset in biology. For researchers,

this means:


- **No wet-lab bottleneck.** Structure hypotheses can be tested computationally before committing to X-ray crystallography or cryo-EM experiments.

- **Confidence metrics included.** Every prediction ships with per-residue pLDDT scores and PAE matrices, so you know exactly which regions to trust.

- **Free and open.** No account, no API key, no Docker image required — direct REST access from any Python environment.

- **Reproducible by design.** The API returns versioned files (e.g. `v6`), so the exact structure used in an analysis can always be retrieved again.


This skill encodes that workflow for Hermes so you can query, download, and analyze AlphaFold structures in a single prompted conversation — without

re-deriving API URLs or parsing patterns each time.


## Purpose
This skill provides a **reproducible, documented workflow** for accessing AlphaFold DB — no credentials, no Docker, direct REST API from the terminal.


Skill location: `~/.hermes/skills/alphafold-db/SKILL.md`


## How This Skill Was Built
**1. Knowledge distillation from source docs**


The source material was analyzed with `research-project-audit` to extract:


- API endpoint patterns (REST URLs for prediction, mmCIF, confidence JSON, PAE)

- pLDDT confidence thresholds (>90 very high, <50 very low)

- BioPython parsing workflows

- Known pitfalls (PAE data structure format)


**2. Skill creation**


Created from the distilled knowledge as a `hermes-agent` skill.

Generated a 204-line SKILL.md with:


- YAML frontmatter (name, description, tags)

- `description: "Use when predicting protein structures via AlphaFold DB API. Provides pLDDT scores, confidence metrics, mmCIF files."`

- `tags: [alphafold-db, protein-structure, plddt, confidence, struct-chem]`


**3. Automated validation**


The build process ran:


- `hermesllm` passed the skill definition

- Live API test: P00520 (ABL1 tyrosine kinase)


  - Query: `https://alphafold.ebi.ac.uk/api/prediction/P00520`


- PAE endpoint fix: `pae[0]["predicted_aligned_error"]` (original had `pae['distance']`)


## Skill Setup
Two skill targets are documented: **Hermes** (file-based auto-load) and **Claude Code CLI** (project or global slash command).


### Claude Code CLI Skill
The slash command `/alphafold` is defined as a Markdown prompt file.


**Project-level** (this repo only):


```console
$ mkdir -p ~/alphafold-ai/.claude/commands
$ cp alphafold.md ~/alphafold-ai/.claude/commands/alphafold.md
```


Open Claude Code from `~/alphafold-ai/` and type:


```text
/alphafold P12931
/alphafold P00520 --pae
/alphafold P00520 --pae --download
```


**Global** (available in every project):


```console
$ mkdir -p ~/.claude/commands
$ cp alphafold.md ~/.claude/commands/alphafold.md
```


Works identically inside the VS Code / JetBrains IDE extensions.


### Hermes Skill
Skills are file-based — Hermes auto-loads any `SKILL.md` found inside `~/.hermes/skills/`. No registration command is required.


**1. Create the skill directory**


```console
$ mkdir -p ~/.hermes/skills/alphafold-db
```


**2. Create SKILL.md with required frontmatter**


```console
$ vi ~/.hermes/skills/alphafold-db/SKILL.md
```


The file must begin with this YAML frontmatter block:


```yaml
---
name: alphafold-db
description: "Use when predicting protein structures via AlphaFold DB API. Provides pLDDT scores, confidence metrics, mmCIF files."
version: 1.0.0
author: snit.san
license: CC-BY-4.0
metadata:
  hermes:
    tags: [alphafold-db, protein-structure, plddt, confidence, struct-chem]
    related_skills: []
---
```


The skill body follows the frontmatter — include the steps, code snippets, and pitfalls you want Hermes to use when this skill is triggered.


**3. Verify the skill is loaded**


Restart Hermes (or open a new session), then confirm the skill is visible:


```console
$ ls ~/.hermes/skills/alphafold-db/SKILL.md
```


Ask Hermes directly to confirm it recognises the skill:


> "list my skills"

> "do you have an alphafold-db skill?"


> **Important:** If the skill is not picked up, check that the YAML frontmatter is valid (no tabs, no missing `---` delimiters) and that the file is saved as `SKILL.md` (case-sensitive).


## API Endpoints

| Endpoint | Description |

| --- | --- |

| `https://alphafold.ebi.ac.uk/api/prediction/{UNIPROT_ID}` | Query metadata (entryId, latestVersion) |

| `https://alphafold.ebi.ac.uk/files/{AFID}-model_v{VER}.cif` | Model coordinates (mmCIF) |

| `https://alphafold.ebi.ac.uk/files/{AFID}-confidence_v{VER}.json` | pLDDT confidence scores |

| `https://alphafold.ebi.ac.uk/files/{AFID}-predicted_aligned_error_v{VER}.json` | PAE matrix |

## How to Use This Skill
The skill is automatically loaded when you ask about:


- AlphaFold DB structure prediction

- pLDDT confidence scores

- mmCIF file parsing

- Protein structure confidence metrics


**Example prompts you can run right now:**


> "show me P00520 structure"

> "what are the pLDDT scores for P12931?"

> "batch process proteins P00520, P12931, P04637"

> "download AlphaFold structure for P12931"


## Step-by-Step Usage
**Step 0: Environment setup**


```console
$ uv venv .venv
$ source .venv/bin/activate
$ uv pip install biopython requests numpy scipy pandas
```


**Step 1: Basic query**


```python
import requests

UNIPROT_ID = "P00520"
resp = requests.get(
    f"https://alphafold.ebi.ac.uk/api/prediction/{UNIPROT_ID}", timeout=30
)
AFID = resp.json()[0]["entryId"]
VER = resp.json()[0]["latestVersion"]
print(f"{UNIPROT_ID} -> {AFID} v{VER}")
```


**Step 2: Download & analyze**


```python
import requests
import numpy as np
import pandas as pd

# Download mmCIF
r = requests.get(
    f"https://alphafold.ebi.ac.uk/files/{AFID}-model_v{VER}.cif", timeout=120
)
with open(f"{AFID}-model_v{VER}.cif", "wb") as f:
    f.write(r.content)

# Parse confidence (pLDDT)
conf = requests.get(
    f"https://alphafold.ebi.ac.uk/files/{AFID}-confidence_v{VER}.json", timeout=30
)
plddt = conf.json()["confidenceScore"]
scores = pd.DataFrame({"pLDDT": plddt})
print(scores.describe())
```


**Step 3: Batch mode**


```python
import requests
import numpy as np
import pandas as pd

UNIPROT_IDS = ["P00520", "P12931", "P04637"]
results = []

for uid in UNIPROT_IDS:
    pred = requests.get(
        f"https://alphafold.ebi.ac.uk/api/prediction/{uid}", timeout=30
    ).json()
    afid = pred[0]["entryId"]
    ver = pred[0]["latestVersion"]

    conf = requests.get(
        f"https://alphafold.ebi.ac.uk/files/{afid}-confidence_v{ver}.json",
        timeout=30,
    )
    plddt_scores = conf.json()["confidenceScore"]

    results.append({
        "uniprot_id": uid,
        "alphafold_id": afid,
        "version": ver,
        "avg_plddt": np.mean(plddt_scores),
        "very_high_conf_frac": sum(
            1 for s in plddt_scores if s > 90
        ) / len(plddt_scores),
    })

df = pd.DataFrame(results)
print(df)
```


## Known Pitfalls
**1. PAE endpoint format change**


The PAE JSON is **a list of dicts**, not a plain dict.


- Wrong: `pae["predicted_aligned_error"]`

- Correct: `pae[0]["predicted_aligned_error"]`


**2. pLDDT confidence interpretation**


- `>90`: Very high confidence — reliable for structure-based analysis

- `70–90`: Confident — generally reliable

- `50–70`: Low confidence — use with caution

- `<50`: Very low confidence — region likely disordered in vivo


**3. BioPython 1.87 — MMCIFParser does not accept BytesIO**


`MMCIFParser.get_structure()` requires a **file path string** in BioPython 1.87.

Passing `io.BytesIO` raises `TypeError: startswith first arg must be bytes`.


- Wrong: `parser.get_structure(af_id, io.BytesIO(cif_content))`

- Correct: write the content to disk first, then pass the path:


```python
with open(out_path, "wb") as f:
    f.write(cif_content)
structure = parser.get_structure(af_id, out_path)
```


**4. High pLDDT does not guarantee functional accuracy**


Always interpret predictions in biological context. Predictions lack ligands, post-translational modifications, and cofactors.


## Quality Gates
- [x] Source docs analyzed with `research-project-audit` script

- [x] Live API test passed (P00520 — ABL1 tyrosine kinase)

- [x] Live API test passed (P12931 — SRC kinase, v6, 536 residues, global pLDDT 83.44)

- [x] PAE fix verified (`pae[0]["predicted_aligned_error"]`)

- [x] BioPython 1.87 BytesIO fix verified (write to disk, parse from path)

- [x] Batch processing tested

- [x] Claude Code CLI skill tested (`/alphafold P12931 --pae --download`)

- [x] YAML validation passed


## Security Notes
**Rate limiting:** The AlphaFold DB API has rate limits. If you get 429 responses, wait 30 seconds between requests.


**No sensitive data:** Only public structural data is accessed. No credentials required.


## Citations and References
When using results from this skill, cite:


[1] Jumper, J. et al. (2021) Highly accurate protein structure prediction with AlphaFold. *Nature* 596, 583-589.

[2] Varadi, M. et al. (2024) AlphaFold 3 and Protein Folding 2.0. *Nucleic Acids Research* 52, w31-w39.
