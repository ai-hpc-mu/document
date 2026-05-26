---
name: watchdog-checkpoint-survival
authors: [Snit Sanghlao, Owen]
description: Universal guide for preventing data loss in long-running jobs (SLURM, training, simulations)
created: 2026-05-15
---

# Watchdog & Checkpoint Survival Guide

**Authors:** Snit Sanghlao · Owen

## Core Principle

**Any job running longer than 1 hour must have crash-proof checkpoints.** A single checkpoint file is a single point of failure — corruption, interrupted writes, or node failures will lose everything since the last good save.

## Golden Rules

### 1. Numbered Checkpoints Are Mandatory

Never rely on a single `latest` file. At every save interval, write BOTH:
- `ckpt_00100.dat` — numbered, immutable, survives corruption
- `latest.dat` — copy for quick resume

```python
def save_checkpoint(state, step):
    k = step // 1_000
    numbered = f"ckpt_{k:05d}.dat"
    save(state, numbered)   # Immutable, survives corruption
    save(state, "latest.dat")  # Quick resume
```

### 2. Atomic Writes Prevent Corruption

Never overwrite a checkpoint in-place. Write to a temp file, then atomically rename:

```python
import tempfile, os

def atomic_save(state, path):
    dir = os.path.dirname(path)
    fd, tmp = tempfile.mkstemp(dir=dir, suffix=".tmp")
    try:
        with os.fdopen(fd, 'wb') as f:
            serialize(state, f)
        os.rename(tmp, path)  # Atomic on same filesystem
    except:
        os.unlink(tmp)  # Cleanup on failure
```

**Why:** If a job crashes mid-write, the original file is untouched. `os.rename()` is atomic on Linux ext4/xfs.

### 3. Smart Resume Logic

On startup, scan for the best numbered checkpoint:

```python
import glob, re

def find_best_checkpoint(pattern="ckpt_*.dat"):
    files = glob.glob(pattern)
    if not files:
        return None
    def extract_num(f):
        m = re.search(r'ckpt_(\d+)', f)
        return int(m.group(1)) if m else 0
    return max(files, key=extract_num)

# Resume
ckpt = find_best_checkpoint() or "latest.dat"
load(ckpt)
```

If `latest.dat` is corrupted, fall back to the best numbered checkpoint automatically.

### 4. Checkpoint Interval vs. Risk

| Job Length | Max Checkpoint Interval | Max Loss |
|-----------|------------------------|----------|
| 1 hour | 5 minutes | 5 min of work |
| 1 day | 30 minutes | 30 min of work |
| 1 week | 2 hours | 2 hours of work |
| 1 month | 6 hours | 6 hours of work |

**Rule:** Maximum acceptable loss = 1% of total job runtime. Never lose more than you can afford to redo.

### 5. SLURM-Specific: Handle Job Preemption

SLURM sends `SIGTERM` before preempting or expiring a job. Catch it:

```python
import signal, sys

def handle_shutdown(signum, frame):
    save_checkpoint(state, current_step)
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGUSR1, handle_shutdown)
```

In your SLURM script, use `--signal=B:USR1@120` to get a warning 120 seconds before preemption:

```bash
#SBATCH --signal=B:USR1@120
#SBATCH --time=7-00:00:00
#SBATCH --requeue
```

### 6. SLURM Checkpoint Directory on Persistent Storage

**Never store checkpoints on scratch/tmp filesystems.** Use persistent storage:

```bash
# BAD — lost on node reboot
CHECKPOINT_DIR=/scratch/$USER/job123/ckpts/

# GOOD — survives node failure
CHECKPOINT_DIR=$HOME/checkpoints/job123/
# Or shared filesystem
CHECKPOINT_DIR=/shared/projects/myteam/checkpoints/job123/
```

### 7. Progress Metadata Is Unreliable

JSON/log files reporting progress can be written by crashed processes with stale or incorrect data. Always verify against actual checkpoint files:

```bash
# Verify checkpoint integrity before resuming
python -c "import torch; torch.load('$CKPT'); print('OK')" 2>/dev/null || echo "CORRUPTED"
```

### 8. Limit Checkpoint Count to Save Disk Space

Keep only the last N numbered checkpoints plus milestones:

```python
import glob, os

def prune_old_checkpoints(prefix="ckpt_", keep_last=5, milestone_every=500_000):
    files = sorted(glob.glob(f"{prefix}*.dat"))
    for f in files[:-keep_last]:
        step = extract_step(f)
        if step % milestone_every != 0:  # Keep milestones forever
            os.remove(f)
```

## SLURM Job Template (Crash-Proof)

```bash
#!/bin/bash
#SBATCH --job-name=mylongjob
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:1
#SBATCH --time=7-00:00:00
#SBATCH --signal=B:USR1@120
#SBATCH --requeue
#SBATCH --output=logs/%x_%j.out

export CHECKPOINT_DIR=$HOME/checkpoints/myjob
mkdir -p "$CHECKPOINT_DIR"

# Find best checkpoint for resume
BEST=$(ls "$CHECKPOINT_DIR"/ckpt_*.dat 2>/dev/null | sort | tail -1)
if [ -n "$BEST" ]; then
    echo "Resuming from: $BEST"
    python myjob.py --resume "$BEST"
else
    echo "Starting fresh"
    python myjob.py
fi
```

## Watchdog / Monitoring Script

```bash
#!/bin/bash
# watchdog.sh — runs via cron, restarts job if dead

JOB_NAME="myjob.py"
PID_FILE="/var/run/myjob.pid"
CKPT_DIR="$HOME/checkpoints/myjob"
LOG="/var/log/myjob-watchdog.log"

# Find running process
PID=$(pgrep -f "$JOB_NAME" | head -1)

if [ -z "$PID" ]; then
    # Find best checkpoint
    BEST=$(ls "$CKPT_DIR"/ckpt_*.dat 2>/dev/null | sort | tail -1)
    if [ -n "$BEST" ]; then
        echo "$(date) Job died. Restarting from $BEST" >> "$LOG"
        nohup python "$JOB_NAME" --resume "$BEST" &
        echo $! > "$PID_FILE"
    else
        echo "$(date) Job died. No checkpoint found. Starting fresh." >> "$LOG"
        nohup python "$JOB_NAME" &
        echo $! > "$PID_FILE"
    fi
else
    echo "$(date) Job alive (PID $PID)" >> "$LOG"
fi
```

Cron: `*/15 * * * * /path/to/watchdog.sh`

## Implementation Checklist

- [ ] Numbered checkpoints at every save interval
- [ ] Atomic writes (temp file + rename)
- [ ] `latest` file as secondary for quick resume
- [ ] Smart resume scans for best numbered checkpoint
- [ ] Signal handlers (SIGTERM, SIGUSR1) save before exit
- [ ] Checkpoint interval ≤1% of total job time
- [ ] Milestone checkpoints kept forever (major boundaries)
- [ ] Old checkpoints pruned to save disk space
- [ ] Checkpoints stored on persistent storage (not scratch)
- [ ] SLURM: `--signal=B:USR1@120` for preemption warning
- [ ] Watchdog monitors and restarts with best checkpoint

## Anti-Patterns (Don't Do These)

| Anti-Pattern | Consequence |
|-------------|-------------|
| Single checkpoint file (`latest.pt` only) | Corruption loses all progress |
| Overwriting checkpoint in-place | Mid-write crash corrupts the file |
| No signal handlers | Node shutdown kills unsaved work |
| Checkpoints on scratch/tmp | Lost on node reboot |
| Checkpoint interval too wide | Loses days of computation |
| Trusting progress JSON over checkpoints | Crashed process writes fake progress |
| Keeping all checkpoints | Fills disk, causes OOM |
| Watchdog hardcoded to `latest` file | Restarts from corrupted state |

## Recovery Procedure

When a job crashes:

1. **Don't panic** — numbered checkpoints survive
2. Check which checkpoints exist: `ls -lt ckpt_*.dat | head`
3. Verify integrity of latest: `python -c "load('ckpt_XXXX.dat'); print('OK')"`
4. If corrupted, go back one: try `ckpt_(N-1).dat`
5. Resume from best valid checkpoint
6. Investigate root cause (OOM? hardware? bug?)
7. Fix before restarting

## Cost of Getting It Wrong

Real example: Lost ~100K training steps (~50 hours GPU time, ~$30 cloud cost) because a single checkpoint file was corrupted during a crash. The fix took 2 hours to implement. The prevention is 30 lines of code.

**Invest 30 minutes setting up crash-proof checkpoints. Save days of recomputation.**
