# HPC User Guide: Avoiding /tmp Full Errors on Compute Nodes
**Author**: Snit Sanghlao and Claude AI(Antropic)

**Cluster**: MAI AI-HPC (NVIDIA BCM)  
**Date**: 2026-03-21

---

## Why This Matters

The compute nodes have a **shared root partition** (`/`) that includes `/tmp`. When jobs write large files to `/tmp`, the entire node's OS disk fills up — crashing your job, draining the node, and blocking all other users.

**Golden rule**: Never write directly to `/tmp`. Always use `/workdir` or `$SLURM_TMPDIR`.

---

## 1. Use `$SLURM_TMPDIR` for Temporary Files

Slurm creates a per-job temporary directory that is **automatically cleaned up** when your job ends.

```bash
#!/bin/bash
#SBATCH --job-name=my_training
#SBATCH --gres=gpu:1

# Copy data to fast local storage
cp /home/$USER/dataset.tar.gz "$SLURM_TMPDIR/"
cd "$SLURM_TMPDIR"
tar -xf dataset.tar.gz

# Run your job from local storage (faster I/O)
python train.py --data_dir "$SLURM_TMPDIR/dataset"

# Copy results back before job ends
cp "$SLURM_TMPDIR/model_best.pt" /home/$USER/results/
```

If `$SLURM_TMPDIR` is not set on your cluster, use `/workdir` with a manual cleanup trap:

```bash
#!/bin/bash
#SBATCH --job-name=my_training
#SBATCH --gres=gpu:1

scratch="/workdir/${USER}_${SLURM_JOB_ID}"
mkdir -p "$scratch"
trap "rm -rf $scratch" EXIT    # auto-delete even if job crashes

cd "$scratch"
# ... your work here ...
```

---

## 2. Singularity / Apptainer

Singularity and Apptainer write **large temporary files** during container build and pull operations. By default these go to `/tmp` and can easily fill the root disk.

### 2.1 Redirect Cache and Temp Directories

Add these to your `~/.bashrc`:

```bash
# Singularity / Apptainer cache and temp
export SINGULARITY_CACHEDIR=/workdir/$USER/singularity_cache
export SINGULARITY_TMPDIR=/workdir/$USER/singularity_tmp
export APPTAINER_CACHEDIR=/workdir/$USER/apptainer_cache
export APPTAINER_TMPDIR=/workdir/$USER/apptainer_tmp

mkdir -p $SINGULARITY_CACHEDIR $SINGULARITY_TMPDIR \
         $APPTAINER_CACHEDIR $APPTAINER_TMPDIR
```

### 2.2 Building Containers

Always specify `--tmpdir` when building:

```bash
singularity build --tmpdir /workdir/$USER/singularity_tmp my_container.sif my_recipe.def
```

### 2.3 Running Containers with `--bind`

Bind `/workdir` into your container so jobs inside the container also write to the safe location:

```bash
singularity exec --nv \
  --bind /workdir/$USER:/scratch \
  my_container.sif python train.py --tmp_dir /scratch
```

### 2.4 Clean Up Old Caches Periodically

```bash
# Check cache size
du -sh /workdir/$USER/singularity_cache

# Clear cache (safe to run anytime)
singularity cache clean
# or
apptainer cache clean
```

---

## 3. Enroot / Pyxis (NVIDIA Containers)

If you use `srun --container-image=...` or Enroot directly, it caches container layers in `/tmp` by default.

Add to your `~/.bashrc`:

```bash
# Enroot / Pyxis cache
export ENROOT_CACHE_PATH=/workdir/$USER/enroot_cache
export ENROOT_DATA_PATH=/workdir/$USER/enroot_data
export ENROOT_RUNTIME_PATH=/workdir/$USER/enroot_runtime

mkdir -p $ENROOT_CACHE_PATH $ENROOT_DATA_PATH $ENROOT_RUNTIME_PATH
```

---

## 4. Python and pip

Python also writes to `/tmp` for package builds and temporary data.

### In Job Scripts

```bash
export TMPDIR=/workdir/$USER/tmp
export PIP_CACHE_DIR=/workdir/$USER/pip_cache
mkdir -p $TMPDIR $PIP_CACHE_DIR
```

### Installing Packages Inside Jobs

```bash
pip install --cache-dir /workdir/$USER/pip_cache my_package
```

---

## 5. PyTorch / Deep Learning Frameworks

Several frameworks create temp files during training:

```bash
# PyTorch compiled extensions
export TORCH_EXTENSIONS_DIR=/workdir/$USER/torch_extensions

# Hugging Face model cache
export HF_HOME=/workdir/$USER/huggingface
export TRANSFORMERS_CACHE=/workdir/$USER/huggingface/transformers

# Triton (GPU kernel cache)
export TRITON_CACHE_DIR=/workdir/$USER/triton_cache

mkdir -p $TORCH_EXTENSIONS_DIR $HF_HOME $TRITON_CACHE_DIR
```

---

## 6. Recommended ~/.bashrc Block

Copy this entire block to your `~/.bashrc` to cover all common cases:

```bash
# =============================================================
# HPC: Redirect all temp/cache away from /tmp to /workdir
# =============================================================
export TMPDIR=/workdir/$USER/tmp
export TEMP=$TMPDIR
export TMP=$TMPDIR

# Singularity / Apptainer
export SINGULARITY_CACHEDIR=/workdir/$USER/singularity_cache
export SINGULARITY_TMPDIR=/workdir/$USER/singularity_tmp
export APPTAINER_CACHEDIR=/workdir/$USER/apptainer_cache
export APPTAINER_TMPDIR=/workdir/$USER/apptainer_tmp

# Enroot / Pyxis
export ENROOT_CACHE_PATH=/workdir/$USER/enroot_cache
export ENROOT_DATA_PATH=/workdir/$USER/enroot_data
export ENROOT_RUNTIME_PATH=/workdir/$USER/enroot_runtime

# Python / pip
export PIP_CACHE_DIR=/workdir/$USER/pip_cache

# PyTorch / DL
export TORCH_EXTENSIONS_DIR=/workdir/$USER/torch_extensions
export HF_HOME=/workdir/$USER/huggingface
export TRANSFORMERS_CACHE=/workdir/$USER/huggingface/transformers
export TRITON_CACHE_DIR=/workdir/$USER/triton_cache

# Create all directories
mkdir -p $TMPDIR $SINGULARITY_CACHEDIR $SINGULARITY_TMPDIR \
         $APPTAINER_CACHEDIR $APPTAINER_TMPDIR \
         $ENROOT_CACHE_PATH $ENROOT_DATA_PATH $ENROOT_RUNTIME_PATH \
         $PIP_CACHE_DIR $TORCH_EXTENSIONS_DIR $HF_HOME $TRITON_CACHE_DIR \
         2>/dev/null
```

---

## 7. Quick Reference: What NOT To Do

| Bad Practice | Why It's Dangerous | Do This Instead |
|---|---|---|
| `cp dataset.tar.gz /tmp/` | Fills root partition | `cp dataset.tar.gz $SLURM_TMPDIR/` |
| `singularity build my.sif my.def` | Build temp goes to `/tmp` | `singularity build --tmpdir /workdir/$USER/singularity_tmp my.sif my.def` |
| `pip install big_package` (no cache redirect) | pip temp goes to `/tmp` | Set `TMPDIR` and `PIP_CACHE_DIR` first |
| Saving checkpoints to `/tmp/checkpoints` | Fills root, lost on job end | Save to `/home/$USER/` or `/workdir/$USER/` |
| Leaving old containers in cache | Wastes disk for everyone | Run `singularity cache clean` periodically |

---

## 8. Check Your Disk Usage

Before and after jobs, check that you're not leaving junk behind:

```bash
# Check /tmp usage (should be small)
du -sh /tmp/$USER* 2>/dev/null

# Check your /workdir usage
du -sh /workdir/$USER/*

# Check overall node disk
df -h /
df -h /workdir
```

If you see `/` above 90%, **alert the admin immediately** — the node may need manual cleanup before it crashes.

---

## Contact

If a node is drained or unresponsive due to disk full, contact the HPC admin team. Do not attempt to manually clean other users' files.