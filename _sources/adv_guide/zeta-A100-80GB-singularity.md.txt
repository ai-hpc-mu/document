
---

# Zeta A100 SXM4 80GB — Singularity Precaution Guide
**Author**: Snit Sanhlao , AI Assitant Claude AI

**Node:** zeta
**GPU:** 8× NVIDIA A100-SXM4-80GB (NVLink 3.0 + NVSwitch)
**Singularity:** CE 4.1.3
**Driver stack:** nvidia-container-toolkit (CDI)

---

##  Use `--nvccli` (Preferred) on Zeta

```bash
singularity exec --nvccli [other flags] image.sif command
```

**Both `--nv` and `--nvccli` work on zeta** (tested 2026-03-26). However, `--nvccli` is preferred as it's the modern standard and more portable.

> Note: Earlier versions of this guide warned against `--nv` due to hangs. The cluster stack has since been updated with compatibility layers.

---

## Pre-flight Check Script

Run this before submitting any GPU Singularity job to a node:

```bash
#!/bin/bash
# check-singularity-gpu.sh <nodename>
# Usage: bash check-singularity-gpu.sh zeta

NODE=${1:-$(hostname)}

echo "=== Singularity GPU Check: $NODE ==="

srun --nodelist=$NODE --gres=gpu:1 --pty bash -c '
    echo "Node: $(hostname)"
    echo "--- GPU hardware ---"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

    echo "--- Singularity flag ---"
    if ls /usr/bin/nvidia-container-cli &>/dev/null; then
        echo "USE --nvccli  (CDI stack detected)"
    else
        echo "USE --nv      (legacy driver stack)"
    fi

    echo "--- nvidia-container-cli path ---"
    ls -la /usr/bin/nvidia-container-cli 2>/dev/null || echo "not found"
'
```

---

## Why `--nvccli` is Preferred on Zeta

`--nv` uses **legacy library injection** — it scans the host for NVIDIA `.so`
files and bind-mounts them into the container. This was built for older
driver setups where libraries live in well-known paths.

`--nvccli` delegates GPU setup to `/usr/bin/nvidia-container-cli` — the
same binary Docker uses internally. It handles CDI correctly.

```
--nv      → Legacy library injection     → works (with compatibility layer)
--nvccli  → nvidia-container-cli setup  → works (modern standard, preferred)
```

**Update (2026-03-26):** Both flags now work on zeta. The cluster stack was updated
with compatibility layers. `--nvccli` remains preferred for portability across
container runtimes (Docker, Podman, Kubernetes).

---

## Portable Flag Detection (use in all sbatch scripts)

Paste this block into any sbatch script that runs Singularity with GPU:

```bash
# Auto-detect Singularity GPU flag
if ls /usr/bin/nvidia-container-cli &>/dev/null; then
    NV_FLAG="--nvccli"
else
    NV_FLAG="--nv"
fi
echo "[singularity] GPU flag: $NV_FLAG"

singularity exec $NV_FLAG "$SIF" command ...
```

---

## Node Reference Table (Tested 2026-03-26)

| Node | GPU | VRAM | Both Flags Work | Recommended |
|------|-----|------|-----------------|-------------|
| zeta | A100 SXM4 80GB | 8× 80GB = 640GB | Yes | `--nvccli` |
| tensorcore | A100 SXM4 40GB | 8× 40GB = 320GB | Yes | `--nvccli` |
| tau | H100 80GB | varies | Yes | `--nvccli` |

> All nodes now support both `--nv` and `--nvccli`. Use `--nvccli` for portability.

## Why `--nvccli` is Recommended

| Reason | Explanation |
|--------|-------------|
| **Modern standard** | Uses `nvidia-container-toolkit`, same as Docker/Podman/Kubernetes |
| **Portable** | Same command works across different container runtimes and clusters |
| **CDI support** | Handles Container Device Interface (the new spec) correctly |
| **Future-proof** | `--nv` is legacy/deprecated upstream |
| **Cleaner isolation** | Delegates GPU setup to dedicated binary, not singularity's library injection |

**Bottom line:** Both work on all nodes. Use `--nvccli` for scripts you want to reuse elsewhere.

---

## User Trip — Cancelling a Live GPU Job (Learned 2026-03-21)

### What Happened

`scancel` was used to kill a running vLLM job (8-way NCCL across all GPUs).
The NCCL workers did not clean up cleanly → GPU memory stayed allocated →
Slurm epilog detected leftover GPU usage → **zeta marked as `UnavailableNodes`**.

Next job submission: `PENDING (ReqNodeNotAvail, UnavailableNodes:zeta)`

### Fix (admin required)

```bash
# 1. SSH to zeta and check for leftover processes
ps aux | grep -E 'python|vllm|nccl' | grep -v grep

# 2. Check if GPU memory is still held
nvidia-smi | grep -E 'MiB|Processes'

# 3a. If GPU is clear → resume node in Slurm (from login node)
scontrol update node=zeta state=resume

# 3b. If processes still stuck → kill first, then resume
kill -9 $(ps aux | grep python | grep -v grep | awk '{print $2}')
scontrol update node=zeta state=resume
```

### Prevention — Graceful Job Cancellation

Never use bare `scancel` on a live NCCL/multi-GPU Singularity job.
Use SIGINT first to allow clean GPU release:

```bash
scancel --signal=SIGINT <JOBID>   # Ctrl+C → NCCL releases GPU contexts
sleep 10
scancel <JOBID>                   # force kill if still running
```

---

## Symptoms of Wrong Flag

| Symptom | Likely Cause |
|---------|-------------|
| `CUDA not available` / `False 0` | No GPU flag passed at all |
| Container exits immediately | Wrong SIF path or missing image |
| `unrecognized arguments` | Using `singularity run` with vLLM args — use `singularity exec` instead |

> Note: The "`--nv` hangs" issue from earlier versions has been resolved via cluster updates.


