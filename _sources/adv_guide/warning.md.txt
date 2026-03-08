# Common Warnings — HPC Cluster (Mahidol DGX)

## WARNING: Do NOT run tmux on compute nodes via SLURM

### What happened (incident 2026-03-08)

A user started an interactive `srun bash` session on `tensorcore`, then launched `tmux` inside that session. The SLURM job hit its 30-minute time limit. SLURM attempted to terminate the job:

1. SLURM sent `SIGTERM` to the job process group
2. `tmux` daemonizes itself — it does **not** die on `SIGTERM`
3. SLURM escalated to `SIGKILL` — child processes were in uninterruptible sleep (network/NFS wait)
4. `SIGKILL` also failed → SLURM logged **"Kill task failed"**
5. Node `tensorcore` was automatically set to `DRAINING` state
6. All subsequent jobs were blocked from running on that node

**SLURM log evidence:**
```
Job 338652  bash  snit.san  TIMEOUT   06:44:31 → 07:14:55  tensorcore
Job 338652.0     CANCELLED  07:16:37
Node tensorcore: Reason=Kill task failed [root@2026-03-08T07:16:35]
```

---

### Root Cause

`tmux` is designed to survive terminal disconnects by running as a background server process. When launched inside a SLURM job, this behaviour conflicts with SLURM's job cleanup mechanism — the tmux server and its children cannot be cleanly terminated when the job time limit is reached.

---

### Correct Pattern

```
✅ CORRECT
Login node (bcm-ai-h02)
  └── tmux new -s mysession          # tmux lives on login node
        └── sbatch myjob.sbatch      # submit to SLURM from tmux
              └── compute node       # SLURM job runs and exits cleanly

❌ WRONG
Login node
  └── srun --pty bash                # interactive job on compute node
        └── tmux new -s mysession    # tmux inside SLURM job ← DANGER
              └── python long_job.py # process won't die at time limit
```

### Rules

1. **tmux belongs on the login node only.** Use it to keep your terminal session alive while waiting for jobs.
2. **Never run tmux inside `srun` or `sbatch` jobs.** SLURM cannot kill tmux cleanly.
3. **Set realistic time limits** on interactive `srun` sessions. When the limit is reached without tmux, SLURM cleans up correctly.
4. **For long-running CPU tasks** (downloads, API calls) that don't need a GPU: run directly on the login node inside tmux — no `srun` needed.

---

### Admin Recovery

When a node is stuck in `DRAINING` due to this issue:

```bash
# 1. Identify orphan jobs still running on the node
sacct -N tensorcore --starttime=TODAY --format=JobID,JobName,User,State

# 2. Cancel any stuck jobs
scancel <JOBID>

# 3. Verify no processes remain, then resume the node
scontrol update NodeName=tensorcore State=resume

# 4. Confirm node is back
sinfo
```

---

### Related

- See `slurm-job-submit.md` for correct job submission patterns
- See `tmu.md` in project `.think/` for tmux usage in the context of ML workflows
