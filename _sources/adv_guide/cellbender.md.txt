# CellBender Quick-Start Tutorial

**Author:** Snit Sanghlao
**AI Assistant:** Claude Opus 4.6 (Anthropic)


> **Source:** [CellBender 0.3.2 Documentation](https://cellbender.readthedocs.io/en/latest/tutorial/index.html)
>
> **Citation:** Stephen J Fleming, Mark D Chaffin, Alessandro Arduini, Amer-Denis Akkad, Eric Banks, John C Marioni, Anthony A Philippakis, Patrick T Ellinor, and Mehrtash Babadi. *Unsupervised removal of systematic background noise from droplet-based single-cell experiments using CellBender.* Nature Methods, 2023. <https://doi.org/10.1038/s41592-023-01943-7>

---

## Introduction

CellBender is a software package for eliminating technical artifacts from high-throughput single-cell RNA sequencing (scRNA-seq) data. Despite recent progress in improving droplet-based single-cell omics protocols, the complexity of these experiments leaves room for systematic biases and background noise in the raw observations. These nuisances can be traced back to undesirable enzymatic processes that produce spurious library fragments, contamination by exogenous or endogenous ambient transcripts, impurity of barcode beads, and barcode swapping during amplification and/or sequencing.

The main purpose of CellBender is to take raw gene-by-cell count matrices and molecule-level information produced by third-party pipelines (e.g., CellRanger, Alevin, DropSeq, StarSolo, etc.), to model and remove systematic biases and background noise, and to produce improved estimates of gene expression.



---

## Installation

To fully leverage the DGX H100/A100, your environment must be correctly configured to interface with CUDA.

```bash
# Create a dedicated conda environment
conda create -n cellbender python=3.8
conda activate cellbender

# Install CUDA 12.1 compatible PyTorch (optimized for sm_90)
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia

# Install CellBender
pip install cellbender

# Down source + examples
git clone https://github.com/broadinstitute/CellBender.git
```

---

## Quick-Start Tutorial: `remove-background`

In this tutorial, we will run `remove-background` on a small dataset derived from the 10x Genomics **heart10k** snRNA-seq dataset (v3 Chemistry, CellRanger 3.0.2).

### Step 1: Download and Prepare the Dataset

As a first step, we download the full dataset and generate a smaller trimmed copy by selecting **500 barcodes** with high UMI count (likely non-empty) and an additional **50,000 barcodes** with small UMI count (likely empty). We also trim to keep only the **top 100 most highly-expressed genes**.

> **Note:** The trimming step is performed in order to allow us to go through this tutorial in a minute on a typical CPU. Processing the full untrimmed dataset requires a CUDA-enabled GPU (e.g., NVIDIA Tesla T4) and takes about 30 minutes to finish. **Trimming is NOT part of the recommended workflow**, and is only for the purposes of a quick demo run.

Navigate to `examples/remove_background/` under your CellBender installation root directory and run the following command in the console:

```bash
python generate_tiny_10x_pbmc.py
```

After successful completion of the script, you should have a new file named `tiny_raw_feature_bc_matrix.h5ad`.

### Step 2: Run `remove-background`

We proceed to run `remove-background` on the trimmed dataset using the following command:(compute node, with CUDA)

```bash
cellbender remove-background \
    --input tiny_raw_feature_bc_matrix.h5ad \
    --output tiny_output.h5 \
    --expected-cells 500 \
    --cuda
    --total-droplets-included 2000
```

### Step 3: Examine Output Files

The tool outputs the following files:

| File | Description |
|------|-------------|
| `tiny_output.h5` | An HDF5 file containing a detailed output of the inference procedure, including the normalized abundance of ambient transcripts, contamination fraction of each droplet, a low-dimensional representation of the real gene expression of each cell, the background-corrected counts matrix, and the posterior probability of each droplet being a cell. |
| `tiny_output_filtered.h5` | Filtered count matrix as an h5 file, with background RNA removed. "Filtered" means this file contains only the droplets determined to have a > 50% posterior probability of containing cells. |
| `tiny_output_cell_barcodes.csv` | CSV file containing all the droplet barcodes determined to have a > 50% posterior probability of containing cells. |
| `tiny_output_metrics.csv` | Metrics file (not used by most users, but can be incorporated into automated pipelines which could re-run CellBender automatically with different parameters if something goes wrong). |
| `tiny_output_report.html` | An HTML report which points out a few things about the run and highlights differences between the output and the input. Issues warnings if there are any aspects of the run that look anomalous, and makes suggestions. |
| `ckpt.tar.gz` | Checkpoint file that can be used to restart training. |

### Step 4: Experiment with Parameters

Try running the tool with `--expected-cells 100` and `--expected-cells 1000`. You should find that the output remains virtually the same.

---

## Downstream Analysis

The count matrix that `remove-background` generates can be easily loaded and used for downstream analyses in **scanpy** and **Seurat**.

### Loading in scanpy

Load the **filtered** count matrix (containing only cells):

```python
import scanpy as sc

# Load the filtered data
adata = sc.read_10x_h5('tiny_output_filtered.h5')
```

### Loading with CellBender's helper functions

For more detailed loading with all CellBender metadata:

```python
from cellbender.remove_background.downstream import anndata_from_h5

# Load the data
adata = anndata_from_h5('tiny_output.h5')
```

This yields an AnnData object with all the cell barcodes analyzed by CellBender (all the `--total-droplets-included`), along with all the metadata and latent variables inferred by CellBender:

```
AnnData object with n_obs × n_vars = 1000 × 100
    obs: 'background_fraction', 'cell_probability', 'cell_size', 'droplet_efficiency'
    var: 'ambient_expression', 'features_analyzed_inds', 'feature_type', 'genome', 'gene_id'
    uns: 'cell_size_lognormal_std', 'empty_droplet_size_lognormal_loc',
         'empty_droplet_size_lognormal_scale', 'posterior_regularization_lambda',
         'swapping_fraction_dist_params', 'target_false_positive_rate',
         'fraction_data_used_for_testing', 'test_elbo', 'test_epoch',
         'train_elbo', 'train_epoch'
    obsm: 'gene_expression_encoding'
```

### Loading both raw and CellBender output together

This is great for downstream analysis, because it allows you to plot the effect of CellBender, and you can always look back at the raw data:

```python
from cellbender.remove_background.downstream import load_anndata_from_input_and_output

adata = load_anndata_from_input_and_output(
    input_file='tiny_raw_feature_bc_matrix.h5ad',
    output_file='tiny_output.h5',
    input_layer_key='raw',
)
```

### Loading in Seurat

Seurat 4.0.2 uses a dataloader `Read10X_h5()` which is not currently compatible with the CellBender output file format. Use PyTables to strip the extra CellBender information:

```bash
ptrepack --complevel 5 tiny_output_filtered.h5:/matrix tiny_output_filtered_seurat.h5:/matrix
```

The flag `--complevel 5` ensures that the file size does not increase. The file `tiny_output_filtered_seurat.h5` is now formatted exactly like a CellRanger v3 h5 file, so Seurat can load it:

```r
# Load Seurat library
library(Seurat)

# Load data from the filtered h5 file
data.file <- 'tiny_output_filtered_seurat.h5'
data.data <- Read10X_h5(filename = data.file, use.names = TRUE)

# Create Seurat object
obj <- CreateSeuratObject(counts = data.data)
obj
```

---

## Usage Guide: Running on Real Data

### Recommended Workflow

1. Run `cellranger count` or some other quantification tool to obtain a count matrix.
2. Run `cellbender remove-background`:

```bash
cellbender remove-background \
    --cuda \
    --input raw_feature_bc_matrix.h5 \
    --output output.h5
```

3. Perform per-cell quality control checks, and filter out dead/dying cells, as appropriate for your experiment.
4. Perform all subsequent analyses using the CellBender count matrix.

> It is useful to also load the raw data: keep it as a layer in an anndata object.

### Output Files (Real Data)

| File | Description |
|------|-------------|
| `output_report.html` | HTML report including plots and commentary, along with any warnings or suggestions for improved parameter settings. |
| `output.h5` | Full count matrix as an h5 file, with background RNA removed. Contains all the original droplet barcodes. |
| `output_filtered.h5` | Filtered count matrix with background RNA removed. Contains only droplets with > 50% posterior probability of containing cells. |

### Key Parameters

**`--epochs`** (default: 150)
- 150 is typically a good choice
- Look for a reasonably-converged ELBO value in the output PDF learning curve (meaning it looks like it has reached some saturating value)
- It is not advisable to over-train (training for more than 300 epochs is too much)

**`--expected-cells`**
- As of v0.3.0, users will typically not need to set this value, as CellBender will choose reasonable values based on your dataset
- If needed, base this on either the number of cells expected a priori from the experimental design, or on the UMI curve

**`--total-droplets-included`**
- As of v0.3.0, users will typically not need to set this value
- If something goes wrong with the defaults, you can try to input this argument manually

**`--cuda`**
- Use this flag when running on a GPU (highly recommended for real datasets)

**`--fpr`** (False Positive Rate)
- Target false positive rate in (0, 1)
- A false positive is a true signal count that is erroneously removed
- More background removal is accompanied by more signal removal at high values of FPR
- You can specify multiple values by giving a space-separated string, which will create multiple output files

### Validation

Create some validation plots of various analyses with and without CellBender `remove-background`:

- UMAPs with and without CellBender (on the same set of cell barcodes)
- Marker gene dotplots and violin plots before and after CellBender (you should see less background noise)
- Directly subtract the output count matrix from the input count matrix and take a close look at what was removed

---

## Examining Output H5 Files

An h5 output file can be examined in detail using PyTables in Python:

```python
import tables

with tables.open_file('tiny_output.h5', 'r') as f:
    print(f)
```

This will show the file structure:

```
/tiny_output.h5 (File) 'CellBender remove-background output'
Object Tree:
/ (RootGroup) 'CellBender remove-background output'
/droplet_latents (Group) 'Latent variables per droplet'
/droplet_latents/background_fraction (CArray)
/droplet_latents/barcode_indices_for_latents (CArray)
/droplet_latents/cell_probability (CArray)
/droplet_latents/cell_size (CArray)
/droplet_latents/droplet_efficiency (CArray)
/droplet_latents/gene_expression_encoding (CArray)
/global_latents (Group) 'Global latent variables'
/global_latents/ambient_expression (CArray)
```

---

## Running on HPC (Example: Biowulf/Slurm)

```bash
#!/bin/bash
module load cellbender

cellbender remove-background \
    --cuda \
    --input tiny_raw_feature_bc_matrix.h5ad \
    --output tiny_output.h5 \
    --expected-cells 500 \
    --total-droplets-included 2000
```

Submit with:

```bash
sbatch --gres=gpu:1 --cpus-per-task=8 --mem=32g cellbender_job.sh
```

---

## Terra / WDL Workflow

A workflow written in the Workflow Description Language (WDL) is available for CellBender `remove-background`. For Terra users, a workflow called `cellbender/remove-background` is available from the Broad Methods repository. There is also a version available on Dockstore.

The WDL is designed to make use of an NVIDIA Tesla T4 GPU on Google Cloud architecture. As of v0.3.0, the WDL uses preemptible instances that are a fraction of the cost, and uses automatic restarting from checkpoints so that work is not lost.

---

## Command-Line Reference

```
usage: cellbender remove-background [-h]
    --input INPUT_FILE
    --output OUTPUT_FILE
    [--cuda]
    [--checkpoint INPUT_CHECKPOINT_TARBALL]
    [--force-use-checkpoint]
    [--expected-cells EXPECTED_CELL_COUNT]
    [--total-droplets-included TOTAL_DROPLETS]
    [--force-cell-umi-prior FORCE_CELL_UMI_PRIOR]
    [--force-empty-umi-prior FORCE_EMPTY_UMI_PRIOR]
    [--model {naive,simple,ambient,swapping,full}]
    [--epochs EPOCHS]
    [--low-count-threshold LOW_COUNT_THRESHOLD]
    [--z-dim Z_DIM]
    [--z-layers Z_HIDDEN_DIMS [Z_HIDDEN_DIMS ...]]
    [--training-fraction TRAINING_FRACTION]
    [--empty-drop-training-fraction FRACTION_EMPTIES]
    [--ignore-features BLACKLISTED_GENES [BLACKLISTED_GENES ...]]
    [--fpr FPR [FPR ...]]
    [--exclude-feature-types EXCLUDE_FEATURES [EXCLUDE_FEATURES ...]]
    [--projected-ambient-count-threshold AMBIENT_COUNTS_IN_CELLS_LOW_LIMIT]
    [--learning-rate LEARNING_RATE]
    [--checkpoint-mins CHECKPOINT_MIN]
    [--final-elbo-fail-fraction FINAL_ELBO_FAIL_FRACTION]
    [--epoch-elbo-fail-fraction EPOCH_ELBO_FAIL_FRACTION]
    [--posterior-batch-size POSTERIOR_BATCH_SIZE]
    [--cpu-threads CPU_THREADS]
    [--debug]
```

### Key Arguments

| Argument | Description |
|----------|-------------|
| `--input` | Raw count matrix file (h5, h5ad, or mtx directory) |
| `--output` | Output file name (h5) |
| `--cuda` | Use GPU acceleration |
| `--checkpoint` | Checkpoint tarball produced by v0.3.0+ to restart training |
| `--force-use-checkpoint` | Bypass workflow hash matching for checkpoint |
| `--expected-cells` | Rough estimate of expected cells (within factor of 2) |
| `--total-droplets-included` | Number of droplets from rank-ordered UMI plot to analyze |
| `--model` | Model type: `naive`, `simple`, `ambient`, `swapping`, `full` |
| `--epochs` | Number of training epochs (default: 150) |
| `--fpr` | Target false positive rate(s) |
| `--posterior-batch-size` | Batch size for posterior sampling (reduce if GPU OOM) |
| `--cpu-threads` | Number of CPU threads to use |

### Model Options

| Model | Description |
|-------|-------------|
| `naive` | Subtracts the estimated ambient profile |
| `simple` | Does not model ambient RNA or barcode swapping (debugging only) |
| `ambient` | Assumes background RNA is incorporated into droplets |
| `swapping` | Assumes background RNA comes from random barcode swapping |
| `full` | Combined ambient and swapping model |

---

## Restarting from Checkpoints

```bash
cellbender remove-background \
    --input my_raw_count_matrix_file.h5 \
    --output my_cellbender_output_file.h5 \
    --checkpoint path/to/ckpt.tar.gz \
    --force-use-checkpoint
```

Ensure that you pair up the right `--input` with the right `--checkpoint`.

---

## Troubleshooting

### GPU Out-of-Memory

- Try setting `--posterior-batch-size` to 64 (instead of default 128)
- Restart from checkpoint to avoid re-running inference
- Use an NVIDIA Tesla T4 GPU if possible (more RAM)
- CellBender only uses 1 GPU; extra GPUs will not help

### Cell Calling Issues

In certain cases, CellBender may fail to call cells accurately. `remove-background` equates "cell probability" with "the probability that a given droplet is not empty." These non-empty droplets might not all contain healthy cells with high counts. The recommended procedure would be to filter cells based on other criteria downstream (e.g., filter for percent mitochondrial reads).

If needed, experiment with `--expected-cells` and `--total-droplets-included` to guide CellBender toward a more reasonable solution.

### Learning Curve Issues

The "learning curve" (ELBO vs training epoch) should increase and approach a stable value. If the learning curve starts decreasing, has a large downward bump or spikes, something may have gone wrong. Try adjusting parameters or report the issue on GitHub.

### Cost Estimate (Google Cloud)

Typical cost is around $0.30 per run on Google Cloud (as of July 2022 pricing).

---

## Additional Resources

- **Documentation:** <https://cellbender.readthedocs.io/>
- **GitHub:** <https://github.com/broadinstitute/CellBender>
- **Paper:** <https://doi.org/10.1038/s41592-023-01943-7>