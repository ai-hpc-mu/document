---
myst:
  html_meta:
    "description lang=en": |
      Documentation for users who wish to use software on cluster.
      pydata-sphinx-theme.
---

# User Guides

To provide comprehensive guide for HPC users and native cloud users.
```{danger}
This guide is still under active development, and we make no promises
about the reliability of content. Your feedback and contribution help improving document.
```


```{toctree}
:maxdepth: 3
:caption: Get started

home
quickStart
swguide
slurm-job-submit
array-jobs
watchdog-checkpoint-survival
```

```{toctree}
:maxdepth: 2
:caption: Math\/Physics tools

mathphysic
quantumml
rstudio
```

```{toctree}
:maxdepth: 2
:caption: Bioinformatics tools

bioinfo
alphafold
parabricks
cellbender
```

```{toctree}
:maxdepth: 2
:caption: Large Model tools


ollama
llm
qwen3.5
metasearch
openclaw
```

```{toctree}
:maxdepth: 2
:caption: Engineering


hfss
fpga
```

```{toctree}
:maxdepth: 2
:caption: DevOps - AI


claudevai
ddp-training
```


```{toctree}
:maxdepth: 2
:caption: Caution!

temp
tmuxwarning
zeta-A100-80GB-singularity
```
