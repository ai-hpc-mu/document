---
title: "Array Jobs"
author: "Snit Sanghlao, Claude, QWEN AI agents"
---

# SLURM Array Jobs Guide

*Author: Snit Sanghlao, Claude, QWEN AI agents*

## Quick Start

```bash
# Submit 16 parallel FFT tasks
sbatch --array=0-15 slurm/fft-example.sh

# Check status
squeue -u $USER

# View results
cat logs/fft-*.log
```

---

## Why Array Jobs?

### 1. Parallel Execution

Run 16 experiments simultaneously instead of sequentially:

| Approach    | Time (16 tasks × 5min) |
|-------------|------------------------|
| Sequential  | 80 minutes             |
| Array Job   | ~5 minutes             |

### 2. QOS Limit Workaround

Clusters limit concurrent jobs per user (typically 3-10). Array jobs count as **ONE** job:

| Approach              | Job Count | Result               |
|-----------------------|-----------|---------------------|
| 32 individual jobs    | 32        | REJECTED after 3    |
| 1 array job (32 tasks)| 1         | All 32 run          |

### 3. Fairness & Resource Utilization

Array jobs + QOS limits together ensure fair cluster access:

| User | Individual Jobs | Array Jobs |
|------|-----------------|------------|
| A    | 32 jobs (blocked)| 1 job ✓   |
| B    | 32 jobs (blocked)| 1 job ✓   |
| C    | 32 jobs (blocked)| 1 job ✓   |

Without array jobs, users would spam the queue. With array jobs, everyone gets equal job slots.

---

## FFT Frequency Analysis Example

### Task Distribution

| Task | Signal          | Freq Band |
|------|-----------------|-----------|
| 0    | traffic_speed   | low       |
| 1    | traffic_volume  | low       |
| 2    | intersection_delay | low    |
| 3    | traffic_speed   | high      |
| 4    | traffic_volume  | high      |
| 5    | intersection_delay | high   |
| 6    | traffic_speed   | all       |
| 7-15 | (repeat cycle)  | ...       |

### `scripts/fft_analysis.py`

```python
#!/usr/bin/env python3
"""FFT Frequency Analysis — Array Job Worker"""

import argparse
import json
import os
import numpy as np
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--signal",    type=str,   default="traffic_speed")
    parser.add_argument("--freq-band", type=str,   default="all")
    parser.add_argument("--output",    type=str,   default="./results")
    args = parser.parse_args()

    task_id = int(os.getenv("SLURM_ARRAY_TASK_ID", 0))

    # Generate sample signal (replace with real data)
    np.random.seed(task_id)
    t = np.linspace(0, 10, 1000)
    signal = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 12 * t) + np.random.randn(1000) * 0.1

    # Compute FFT
    fft = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), d=0.01)

    # Extract dominant frequencies
    magnitudes = np.abs(fft[:len(fft)//2])
    top_idx = np.argsort(magnitudes)[-5:][::-1]
    top_freqs = [(freqs[i], magnitudes[i]) for i in top_idx]

    result = {
        "task_id": task_id,
        "signal": args.signal,
        "freq_band": args.freq_band,
        "dominant_freqs": [{"freq": float(f), "mag": float(m)} for f, m in top_freqs],
        "status": "complete",
    }

    out_dir = Path(args.output) / "fft" / f"task{task_id}"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "result.json", "w") as f:
        json.dump(result, f, indent=2)

    print(f"Task {task_id}: Top freqs = {top_freqs[:3]}")
    return 0

if __name__ == "__main__":
    main()
```

### `slurm/fft-example.sh`

```bash
#!/bin/bash
# FFT Array Job — Parallel frequency analysis
# Submit: sbatch --array=0-15 slurm/fft-example.sh

#SBATCH --job-name=fft-analysis
#SBATCH --nodes=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --partition=defq
#SBATCH --output=logs/fft-%A_%a.log

source /cm/shared/apps/anaconda3/etc/profile.d/conda.sh
conda activate traffic

TASK_ID=$SLURM_ARRAY_TASK_ID

# Signal configurations (16 combinations)
SIGNALS=(traffic_speed traffic_volume intersection_delay)
FREQ_BANDS=(low high all)

# Map task_id to parameters
SIG_IDX=$((TASK_ID % 3))
FREQ_IDX=$(((TASK_ID / 3) % 3))

SIGNAL=${SIGNALS[$SIG_IDX]}
FREQ_BAND=${FREQ_BANDS[$FREQ_IDX]}

echo "Task $TASK_ID: signal=$SIGNAL, freq_band=$FREQ_BAND"

python3 scripts/fft_analysis.py \
    --signal $SIGNAL \
    --freq-band $FREQ_BAND \
    --output /scratch/$USER/fft-results
```

---

## Smoke Test (No Real Data)

Validate infrastructure before running full experiments:

### `scripts/fft_smoke_test.py`

```python
#!/usr/bin/env python3
"""FFT Smoke Test — Validates FFT array job infrastructure"""

import argparse
import json
import os
import numpy as np
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--signal",    type=str, default="test")
    parser.add_argument("--freq-band", type=str, default="all")
    parser.add_argument("--output",    type=str, default="./results")
    args = parser.parse_args()

    task_id = int(os.getenv("SLURM_ARRAY_TASK_ID", 0))

    # Generate synthetic signal (no real data needed)
    np.random.seed(task_id)
    t = np.linspace(0, 10, 1000)
    signal = np.sin(2 * np.pi * 5 * t) + np.random.randn(1000) * 0.1

    # Compute FFT
    fft = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), d=0.01)

    # Extract top frequencies
    magnitudes = np.abs(fft[:len(fft)//2])
    top_idx = np.argsort(magnitudes)[-3:][::-1]
    top_freqs = [(freqs[i], magnitudes[i]) for i in top_idx]

    result = {
        "task_id": task_id,
        "signal": args.signal,
        "freq_band": args.freq_band,
        "dominant_freqs": [{"freq": float(f), "mag": float(m)} for f, m in top_freqs],
        "status": "complete",
        "smoke_test": True,
    }

    out_dir = Path(args.output) / "fft-smoke" / f"task{task_id}"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "result.json", "w") as f:
        json.dump(result, f, indent=2)

    print(f"Task {task_id}: Top freq = {top_freqs[0]}")
    return 0

if __name__ == "__main__":
    main()
```

### `slurm/fft-smoke-test.sh`

```bash
#!/bin/bash
# FFT Smoke Test — 16 parallel tasks, no real data
# Submit: sbatch --array=0-15 slurm/fft-smoke-test.sh

#SBATCH --job-name=fft-smoke
#SBATCH --nodes=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=2G
#SBATCH --time=00:05:00
#SBATCH --partition=defq
#SBATCH --output=logs/fft-smoke-%A_%a.log

source /cm/shared/apps/anaconda3/etc/profile.d/conda.sh
conda activate python3

TASK_ID=$SLURM_ARRAY_TASK_ID

# 16 synthetic configurations
SIGNALS=(synthetic_1 synthetic_2 synthetic_3 synthetic_4)
FREQ_BANDS=(low high all)

SIG_IDX=$((TASK_ID % 4))
FREQ_IDX=$(((TASK_ID / 4) % 3))

SIGNAL=${SIGNALS[$SIG_IDX]}
FREQ_BAND=${FREQ_BANDS[$FREQ_IDX]}

echo "Task $TASK_ID: signal=$SIGNAL, freq_band=$FREQ_BAND"

python3 scripts/fft_smoke_test.py \
    --signal $SIGNAL \
    --freq-band $FREQ_BAND \
    --output /scratch/$USER/fft-results
```

### Run Smoke Test

```bash
sbatch --array=0-15 slurm/fft-smoke-test.sh
```

---

## QOS Limits Explained

### What You See

```
JOBID          STATE
339846_[0-2]   R    (running)
339846_[3-31]  PD   (QOSMaxJobsPerUserLimit)
```

### Meaning

- **PD** = Pending (waiting)
- **QOSMaxJobsPerUserLimit** = Cluster allows only 3 concurrent jobs per user

### Why QOS Limits Exist

| Reason              | Explanation                          |
|---------------------|--------------------------------------|
| Fair Share          | Prevent one user from monopolizing   |
| Resource Protection | Protect login nodes, scheduler       |
| Cost Control        | Compute resources are expensive      |

### How Array Jobs Help

Array jobs count as **ONE** job entry:

```bash
# Individual jobs (hit QOS limit)
sbatch job1.sh    # Job 1 ✓
sbatch job2.sh    # Job 2 ✓
sbatch job3.sh    # Job 3 ✓
sbatch job4.sh    # REJECTED

# Array job (bypasses QOS limit)
sbatch --array=0-31 exp.sh   # Job 1 ✓ (32 tasks under 1 entry)
```

### Check Your Cluster's QOS

```bash
# View QOS definitions
scontrol show qos

# Check your QOS limits
sacctmgr show qos format=Name,MaxJobs,MaxSubmitJobs

# Check current jobs
squeue -u $USER -o "%A %a %J %T"
```

---

## Commands Reference

| Action              | Command                                      |
|---------------------|----------------------------------------------|
| Submit array job    | `sbatch --array=0-15 script.sh`              |
| Check status        | `squeue -u $USER`                            |
| Check specific job  | `squeue -j <JOB_ID>`                         |
| Cancel entire array | `scancel <JOB_ID>`                           |
| Cancel specific task| `scancel <JOB_ID>_[0,5,10]`                  |
| View logs           | `cat logs/fft-*.log`                         |
| View QOS limits     | `scontrol show qos`                          |

---

## Resource Efficiency

### Task Sizing Guide

| Task Type         | CPUs  | Memory | Time   |
|-------------------|-------|--------|--------|
| FFT (light)       | 2     | 2GB    | 5 min  |
| Traffic sim (med) | 2     | 4GB    | 1 hour |
| ML training (heavy)| 8    | 32GB   | 4 hours|

### CPU-Oriented Tasks

For compute-bound workloads (FFT, matrix ops, simulations):

| Scenario              | CPUs Per Task | Reason                          |
|-----------------------|---------------|---------------------------------|
| Single-threaded FFT   | 2             | 1 for compute, 1 for I/O        |
| Multi-threaded FFT    | 4-8           | Parallelize across cores        |
| Vectorized (numpy)    | 2-4           | Leverage SIMD, avoid oversubscribe|
| Parallel (multiprocessing) | 8-16     | Spawn worker processes          |

### Node Packing (CPU-Heavy)

**Node: 64 CPUs, 256GB RAM**

| Task Type         | CPUs/Task | Tasks/Node | Total Time (32 tasks) |
|-------------------|-----------|------------|----------------------|
| Light (2 CPUs)    | 2         | 32         | ~5 min               |
| Medium (4 CPUs)   | 4         | 16         | ~10 min (2 batches)  |
| Heavy (8 CPUs)    | 8         | 8          | ~20 min (4 batches)  |
| Very Heavy (16)   | 16        | 4          | ~40 min (8 batches)  |

### When to Increase CPUs Per Task

```bash
# Single task, more cores = faster
#SBATCH --cpus-per-task=8    # FFT with parallel backend

# Many tasks, limit total cores
#SBATCH --cpus-per-task=2    # 32 tasks × 2 = 64 cores
```

### Memory-Bound vs CPU-Bound

| Type          | Bottleneck    | Solution                    |
|---------------|---------------|-----------------------------|
| CPU-bound     | Compute       | Add more CPUs               |
| Memory-bound  | RAM           | Add more memory             |
| I/O-bound     | Disk/Network  | Reduce I/O, cache results   |

### Right-Sizing Matters

```bash
# Over-allocated (waste)
#SBATCH --cpus-per-task=8    # Only uses 2
#SBATCH --mem=16G           # Only uses 2GB
# Result: 75% waste, fewer tasks per node

# Right-sized (efficient)
#SBATCH --cpus-per-task=2
#SBATCH --mem=2G
# Result: 100% utilization, more tasks per node
```

---

## Output Format

```json
{
  "task_id": 5,
  "signal": "traffic_volume",
  "freq_band": "high",
  "dominant_freqs": [
    {"freq": 12.0, "mag": 45.3},
    {"freq": 5.0, "mag": 32.1},
    {"freq": 0.5, "mag": 12.8}
  ],
  "status": "complete"
}
```

---

## Aggregating Results

```python
import json
from pathlib import Path

results_dir = Path("/scratch/$USER/fft-results/fft")
results = []

for task_dir in results_dir.glob("task*"):
    result_file = task_dir / "result.json"
    if result_file.exists():
        results.append(json.loads(result_file.read_text()))

# Print summary
for r in results:
    print(f"Task {r['task_id']}: {r['signal']} | {r['freq_band']} | {r['status']}")
```

---

## Best Practices

| Practice            | Why                                          |
|---------------------|----------------------------------------------|
| Use array jobs      | Counts as 1 job, bypasses QOS limit          |
| Right-size tasks    | Maximize nodes, reduce waste                 |
| Run smoke test      | Validate before full experiment              |
| Monitor utilization | Check actual vs allocated resources          |
| Batch similar tasks | Group by resource requirements               |

---

## Summary

| Concept             | Key Point                                    |
|---------------------|----------------------------------------------|
| Array jobs          | 1 job entry, N tasks                         |
| QOS limits          | Fair share, prevent monopolization           |
| Fairness            | Array + QOS = equal access for all users     |
| Efficiency          | Right-size tasks, pack nodes fully           |
| Smoke test          | Validate infrastructure before real work     |
