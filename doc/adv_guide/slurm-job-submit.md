# SLURM Job Submit Guide

แนะนำให้เขียน SLURM script ประมาณนี้ครับ

## Basic SLURM Script

```bash
#!/bin/bash
#SBATCH --job-name=my_job
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --gpus=1
#SBATCH --mem=16G
#SBATCH --time=01:00:00
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err

SCRATCHDIR=/scratch/$USER

mkdir -p /scratch/$USER
cp input.DAT /scratch/$USER

srun python mycode.py $SCRATCHDIR/input.DAT
```

## คำอธิบาย SBATCH Options

| Option | คำอธิบาย |
|---|---|
| `--job-name` | ชื่อ job ที่จะแสดงใน queue |
| `--partition` | partition ที่ต้องการใช้ (cluster นี้มี partition เดียวคือ `defq`) |
| `--nodes` | จำนวน node ที่ต้องการ |
| `--ntasks` | จำนวน task (process) ทั้งหมด |
| `--cpus-per-task` | จำนวน CPU cores ต่อ task |
| `--gpus` | จำนวน GPU ที่ต้องการ |
| `--mem` | จำนวน memory ที่ต้องการ |
| `--time` | เวลาสูงสุดที่ job จะรัน (format: HH:MM:SS) |
| `--output` | ไฟล์สำหรับ stdout (`%j` = job ID) |
| `--error` | ไฟล์สำหรับ stderr |

## การใช้ /scratch

แนะนำให้ copy ข้อมูลไปที่ `/scratch` ก่อนรัน job เพื่อประสิทธิภาพ I/O ที่ดีกว่า และ copy ผลลัพธ์กลับมาเมื่อเสร็จ

```bash
SCRATCHDIR=/scratch/$USER/$SLURM_JOB_ID

# สร้าง scratch directory
mkdir -p $SCRATCHDIR

# copy input ไปที่ scratch
cp input.DAT $SCRATCHDIR/

# รัน job
srun python mycode.py $SCRATCHDIR/input.DAT

# copy ผลลัพธ์กลับมา
cp $SCRATCHDIR/output.* $SLURM_SUBMIT_DIR/

# cleanup scratch
rm -rf $SCRATCHDIR
```

## Multi-GPU Job

```bash
#!/bin/bash
#SBATCH --job-name=multi_gpu
#SBATCH --partition=defq
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --gpus=4
#SBATCH --mem=64G
#SBATCH --time=04:00:00
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err

SCRATCHDIR=/scratch/$USER/$SLURM_JOB_ID
mkdir -p $SCRATCHDIR
cp -r data/ $SCRATCHDIR/

srun python train.py --data_dir $SCRATCHDIR/data --gpus 4

cp $SCRATCHDIR/checkpoints/* $SLURM_SUBMIT_DIR/checkpoints/
rm -rf $SCRATCHDIR
```

## Multi-Node Job

```bash
#!/bin/bash
#SBATCH --job-name=multi_node
#SBATCH --partition=defq
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gpus-per-node=4
#SBATCH --mem=64G
#SBATCH --time=08:00:00
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err

SCRATCHDIR=/scratch/$USER/$SLURM_JOB_ID
mkdir -p $SCRATCHDIR
cp -r data/ $SCRATCHDIR/

srun python -m torch.distributed.run \
    --nproc_per_node=4 \
    --nnodes=$SLURM_NNODES \
    --node_rank=$SLURM_NODEID \
    --master_addr=$(scontrol show hostname $SLURM_NODELIST | head -n1) \
    --master_port=29500 \
    train.py --data_dir $SCRATCHDIR/data

cp $SCRATCHDIR/checkpoints/* $SLURM_SUBMIT_DIR/checkpoints/
rm -rf $SCRATCHDIR
```

## คำสั่งที่ใช้บ่อย

```bash
# submit job
sbatch myjob.sh

# ดู queue
squeue -u $USER

# ยกเลิก job
scancel <job_id>

# ดูรายละเอียด job
scontrol show job <job_id>

# ดู partition ที่ใช้ได้
sinfo

# ดู resource ที่ใช้หลัง job เสร็จ
sacct -j <job_id> --format=JobID,Elapsed,MaxRSS,MaxVMSize,State
```
