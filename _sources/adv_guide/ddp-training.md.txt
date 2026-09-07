# HPC-AI User Guide: NCCL DDP Multi-Node Training

**Author:** Snit Sanghlao and Qwen  
**Institution:** Mahidol AI Center  
**Date:** 2026-05-19  
**Cluster:** MAI HPC (Slurm) — tau, zeta, omega

---

## Table of Contents

1. [Cluster Overview](#1-cluster-overview)
2. [Preparation: Smoke Tests](#2-preparation-smoke-tests)
3. [NCCL Environment Variables Reference](#3-nccl-environment-variables-reference)
4. [DDP Training: General Guidelines](#4-ddp-training-general-guidelines)
5. [Common Pitfalls](#5-common-pitfalls)
6. [Benchmark Results](#6-benchmark-results)
7. [Quick Reference: Submit a Job](#7-quick-reference-submit-a-job)

---

## Executive Summary

This guide covers Distributed Data Parallel (DDP) training across multiple GPUs and nodes using NVIDIA NCCL on the Mahidol AI Center HPC cluster.

### Why NCCL + DDP + InfiniBand?

| Factor | Single GPU | DDP (Ethernet) | DDP (InfiniBand) |
|--------|-----------|----------------|------------------|
| Throughput | — | ~10 Gb/s | ~200 Gb/s (20×) |
| Training time (CIFAR-10, 2 GPUs) | Baseline | 37.7s | **18.1s** |
| Speedup | 1× | — | **~2.1× over Ethernet** |
| Scalability | N/A | Limited by bandwidth | Scales to many nodes |

- **NCCL** (NVIDIA Collective Communications Library) is the standard communication backend for multi-GPU PyTorch training. It provides optimized `all_reduce`, `all_gather`, and `broadcast` operations.
- **DDP** (Distributed Data Parallel) splits training data across GPUs, each holding a full model copy, and synchronizes gradients via NCCL after every backward pass.
- **InfiniBand** provides low-latency, high-bandwidth interconnect between nodes — critical for multi-node DDP where gradient synchronization becomes the bottleneck.

> **Bottom line:** Without InfiniBand, multi-node DDP is bottlenecked by Ethernet bandwidth. With it, you get near-linear scaling across nodes.

---

## 1. Cluster Overview

### Hardware

| Node | CPU | Cores (HT) | Memory | GPUs | IB Ports (Active) |
|------|-----|-----------|--------|------|-------------------|
| **tau** | x86_64 | 112 × 2 = 224 | ~2 TB | 8× NVIDIA H100 80GB | `mlx5_3`, `mlx5_4`, `mlx5_6`, `mlx5_11` (200 Gb/s) |
| **zeta** | x86_64 | 128 × 2 = 256 | ~2 TB | 8× NVIDIA A100 80GB | `mlx5_0`–`mlx5_3`, `mlx5_6`–`mlx5_9` (200 Gb/s) |
| **omega** | — | — | — | — | DOWN (maintenance) |

### Slurm Configuration

| Parameter | Value |
|-----------|-------|
| Cluster | `slurm` |
| Partition | `defq` (default) |
| Total nodes | 3 (2 active) |
| Total GPUs | 16 |
| Scheduler | `select/cons_tres` |
| MPI default | `pmix` |

---

## 2. Preparation: Smoke Tests

Before running production training, always verify connectivity and NCCL health.

### 2.1 Basic 2-Node Connectivity

```bash
#!/bin/bash
# smoke2node.sh
#SBATCH --job-name=smoke2node
#SBATCH --partition=defq
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=2
#SBATCH --time=00:02:00

srun -N 2 bash -c 'echo "Rank=$SLURM_PROCID  Host=$(hostname)"'
```

**Expected output:** Both ranks print their hostname.

### 2.2 NCCL Smoke Test (Ethernet)

```bash
#!/bin/bash
# nccl_smoke_2node.sh
#SBATCH --job-name=nccl_smoke2n
#SBATCH --partition=defq
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:05:00

module load cuda12.2/toolkit nccl2-cuda12.2-gcc11/2.18.3 default-environment
eval "$(conda shell.bash hook)"
conda activate hpc_lab

export MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n1)
export MASTER_PORT=29500
export NCCL_IB_DISABLE=1
export NCCL_SOCKET_IFNAME=bond

srun -N 2 python3 -c "
import os, torch, torch.distributed as dist
rank       = int(os.environ['SLURM_PROCID'])
world_size = int(os.environ['SLURM_NTASKS'])
local_rank = int(os.environ.get('SLURM_LOCALID', 0))
master     = os.environ['MASTER_ADDR']
port       = os.environ['MASTER_PORT']
torch.cuda.set_device(local_rank)
device = torch.device(f'cuda:{local_rank}')
dist.init_process_group('nccl', rank=rank, world_size=world_size,
                        init_method=f'tcp://{master}:{port}')
x = torch.ones(1, device=device) * rank
dist.all_reduce(x, op=dist.ReduceOp.SUM)
print(f'Rank {rank}: all_reduce = {x.item()}')
dist.destroy_process_group()
"
```

**Expected output:** Both ranks print `all_reduce = 1.0` (0 + 1).

### 2.3 NCCL Smoke Test (InfiniBand)

```bash
#!/bin/bash
# nccl_smoke_2node_ib.sh
#SBATCH --job-name=nccl_ib2n
#SBATCH --partition=defq
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:05:00

module load cuda12.2/toolkit nccl2-cuda12.2-gcc11/2.18.3 default-environment
eval "$(conda shell.bash hook)"
conda activate hpc_lab

export MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n1)
export MASTER_PORT=29500
export NCCL_IB_DISABLE=0
export NCCL_SOCKET_IFNAME=bond
export NCCL_IB_HCA=mlx5_3,mlx5_6
export NCCL_IB_GID_INDEX=3
export NCCL_DEBUG=INFO

srun -N 2 python3 -c "
import os, torch, torch.distributed as dist
rank       = int(os.environ['SLURM_PROCID'])
world_size = int(os.environ['SLURM_NTASKS'])
local_rank = int(os.environ.get('SLURM_LOCALID', 0))
master     = os.environ['MASTER_ADDR']
port       = os.environ['MASTER_PORT']
torch.cuda.set_device(local_rank)
device = torch.device(f'cuda:{local_rank}')
dist.init_process_group('nccl', rank=rank, world_size=world_size,
                        init_method=f'tcp://{master}:{port}')
x = torch.ones(1, device=device) * rank
dist.all_reduce(x, op=dist.ReduceOp.SUM)
print(f'Rank {rank}: all_reduce = {x.item()}')
dist.destroy_process_group()
"
```

**Expected output:** NCCL log shows `Using network IB`, both ranks print `all_reduce = 1.0`.

### 2.4 Troubleshooting Smoke Tests

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Socket timed out` | Node still draining | Wait for node to reach `IDLE` state |
| `No route to host` | NCCL picked down IB port | Set `NCCL_IB_HCA` to active ports only |
| `QOSMaxMemoryPerUser` | Memory QoS limit exceeded | Reduce `--mem` or wait for lower usage |
| Job stuck in `CG` (Completing) | Orphaned srun step | Contact admin or restart slurmctld |
| `NCCL error: unhandled cuda error` | GPU not accessible | Verify `--gres=gpu:N` matches request |

---

## 3. NCCL Environment Variables Reference

| Variable | Purpose | Recommended Value |
|----------|---------|-------------------|
| `NCCL_IB_DISABLE` | Enable/disable IB transport | `0` (enable) for IB, `1` for Ethernet-only |
| `NCCL_SOCKET_IFNAME` | Bootstrap interface | `bond` — always use Ethernet for bootstrap |
| `NCCL_IB_HCA` | Explicit IB HCAs to use | `mlx5_3,mlx5_6` (active ports on both tau and zeta) |
| `NCCL_IB_GID_INDEX` | GID index for RoCE/IB | `3` |
| `NCCL_DEBUG` | Debug verbosity | `INFO` for troubleshooting, unset for production |
| `NCCL_NET_PLUGIN` | Custom network plugin | Leave default (internal) |
| `NCCL_P2P_DISABLE` | Disable P2P between GPUs | `0` (enable P2P for same-node GPUs) |
| `NCCL_SHM_DISABLE` | Disable shared memory | `0` (enable for same-node communication) |

### Key Principle: Bootstrap over Ethernet, Transport over IB

> Always set `NCCL_SOCKET_IFNAME=bond` so process discovery uses Ethernet, then let NCCL use IB for actual data transfer. This prevents NCCL from selecting a down IB port during bootstrap.

---

## 4. DDP Training: General Guidelines

### 4.1 Single-Node, Multi-GPU

Use `torchrun` for single-node DDP:

```bash
#!/bin/bash
# ddp_job_1node.sh
#SBATCH --job-name=cifar10_ddp_1n
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:2
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --time=00:30:00

module load cuda12.2/toolkit nccl2-cuda12.2-gcc11/2.18.3 default-environment
eval "$(conda shell.bash hook)"
conda activate hpc_lab

torchrun --nproc_per_node=2 --nnodes=1 --rdzv_endpoint=localhost:29500 train_ddp.py
```

**Python code** (`train_ddp.py`):
```python
import os
import torch.distributed as dist

dist.init_process_group("nccl")  # torchrun sets all env vars automatically
rank       = dist.get_rank()
local_rank = int(os.environ['LOCAL_RANK'])
```

### 4.2 Multi-Node DDP

Use `srun` with SLURM environment variables:

```bash
#!/bin/bash
# ddp_job_2node.sh
#SBATCH --job-name=cifar10_ddp_2n
#SBATCH --partition=defq
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=8G
#SBATCH --time=00:30:00

module load cuda12.2/toolkit nccl2-cuda12.2-gcc11/2.18.3 default-environment
eval "$(conda shell.bash hook)"
conda activate hpc_lab

export MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n1)
export MASTER_PORT=29500
export NCCL_IB_DISABLE=0
export NCCL_SOCKET_IFNAME=bond
export NCCL_IB_HCA=mlx5_3,mlx5_6
export NCCL_IB_GID_INDEX=3

srun -N 2 python3 train_ddp_2node.py
```

**Python code** (`train_ddp_2node.py`):
```python
import os
import torch.distributed as dist

rank       = int(os.environ['SLURM_PROCID'])
world_size = int(os.environ['SLURM_NTASKS'])
local_rank = int(os.environ.get('SLURM_LOCALID', 0))
master     = os.environ['MASTER_ADDR']
port       = os.environ['MASTER_PORT']

dist.init_process_group('nccl', rank=rank, world_size=world_size,
                        init_method=f'tcp://{master}:{port}')
```

### 4.3 Best Practices

1. **Always run smoke tests first** — verify NCCL works before launching expensive training
2. **Use `DistributedSampler`** — ensures each GPU gets unique data per epoch
3. **Call `train_sampler.set_epoch(epoch)`** — shuffles data differently each epoch
4. **Save checkpoints on rank 0 only** — avoids file write conflicts
5. **Use `pin_memory=True`** in DataLoader — enables async CPU→GPU transfer
6. **Set `num_workers` appropriately** — 4 per GPU is a good starting point
7. **Use `model.module.state_dict()`** — unwrap DDP wrapper before saving
8. **Call `dist.destroy_process_group()`** — ensures clean shutdown
9. **Use `NCCL_DEBUG=INFO` only for debugging** — adds overhead in production
10. **Monitor with `nvidia-smi`** — verify all GPUs are utilized

### 4.4 Performance Checklist

| Check | Command |
|-------|---------|
| All GPUs active | `nvidia-smi` on each node |
| IB link up | `ibstat` — look for `State: Active` |
| NCCL using IB | `NCCL_DEBUG=INFO` log shows `Using network IB` |
| No Ethernet fallback | Log should **not** show `Using network Socket` |
| GPU utilization | `nvidia-smi dmon` — should show >80% utilization |
| Memory balanced | All GPUs using similar VRAM |

---

## 5. Common Pitfalls

### 5.1 NCCL Picks Down IB Port

**Symptom:** `No route to host` during NCCL init.

**Cause:** NCCL auto-detects all IB HCAs, including down ones.

**Fix:** Explicitly restrict NCCL to active ports:
```bash
export NCCL_IB_HCA=mlx5_3,mlx5_6
```

Verify active ports first with `ibstat | grep -A5 "Port 1"` and confirm `State: Active`.

### 5.2 Node Still Draining

**Symptom:** `Socket timed out on send/recv operation`.

**Cause:** Node was resumed from `drain` but `slurmd` isn't ready.

**Fix:** Wait 1–2 minutes, then resubmit. Check node state with:
```bash
sinfo -o "%N %t"
```

### 5.3 QoS Memory Limit

**Symptom:** Job pending with `QOSMaxMemoryPerUser`.

**Cause:** Your total memory across all jobs exceeds the QoS limit.

**Fix:** Cancel other jobs or reduce `--mem` request. Check current usage with:
```bash
squeue -u $USER -o "%A %j %m %t"
```

### 5.4 Stuck COMPLETING State

**Symptom:** Job shows `CG` indefinitely.

**Cause:** Orphaned `srun` step that failed to launch.

**Fix:** Contact the cluster admin to force-clear the job. In the meantime you can cancel with `scancel <jobid>` — if that hangs, the admin needs to run `scontrol requeue <jobid>` or restart `slurmctld`.

---

## 6. Benchmark Results

| Configuration | GPUs | Transport | Time (5 epochs) | Test Accuracy |
|---------------|------|-----------|-----------------|---------------|
| 2-node, 2 GPU | tau + zeta | Ethernet (bond0) | 37.7s | 71.0% |
| 2-node, 2 GPU | tau + zeta | **InfiniBand** | **18.1s** | **71.9%** |

**Speedup:** ~2.1× with InfiniBand over Ethernet for 2-node DDP.

---

## 7. Quick Reference: Submit a Job

```bash
# 1. Smoke test: basic 2-node connectivity
sbatch smoke2node.sh

# 2. Smoke test: NCCL over Ethernet
sbatch nccl_smoke_2node.sh

# 3. Smoke test: NCCL over InfiniBand
sbatch nccl_smoke_2node_ib.sh

# 4. DDP training (single node, 2 GPUs)
sbatch ddp_job_1node.sh

# 5. DDP training (2 nodes, InfiniBand)
sbatch ddp_job_2node.sh

# Monitor jobs
squeue -u $USER -o "%A %N %j %t %R"

# Check output
cat ddp_2node-*.out
```

---

*Mahidol AI Center — HPC-AI User Guide v1.0*
