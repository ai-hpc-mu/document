Large Language Model 
=========================

Large language model (LLM) is a language model notable for its ability to achieve general-purpose language generation. LLMs acquire these abilities by learning statistical relationships from text documents during a computationally intensive self-supervised and semi-supervised training process. LLMs are artificial neural networks typically built with a transformer-based architecture. Some recent implementations are based on alternative architectures such as recurrent neural network variants and Mamba (a state space model).

LLMs can be used for text generation, a form of generative AI, by taking an input text and repeatedly predicting the next token or word. Up to 2020, fine tuning was the only way a model could be adapted to be able to accomplish specific tasks. Larger sized models, such as GPT-3, however, can be prompt-engineered to achieve similar results. They are thought to acquire knowledge about syntax, semantics and "ontology" inherent in human language corpora, but also inaccuracies and biases present in the corpora.

`Large language model <https://en.wikipedia.org/wiki/Large_language_model>`_

LLaMA
------

The first LLM open model we are interested is LLaMA that OpenThaiGPT based on this model.
LLaMA (Large Language Model Meta AI) is a family of autoregressive large language models (LLMs), released by Meta AI starting in February 2023.
`OpenThaiGPT Finetune <https://github.com/OpenThaiGPT/openthaigpt-finetune>`

LoRA: AI at the edge is comming.
----------------------------------
However, after we proved that we can make use resource to finetune LLaMa model in one night one A100 server, answer for Thai language is more room to improve. So with LoRA or Low-Rank Adaptation method is a fine-tuning method introduced by a team of Microsoft researchers in 2021. Since then, it has become a very popular approach to fine-tuning large language models. It makes possible edge resource to finetune LLM.

Goolge's LLM: Gemma
--------------------

There are LLM model from Goolge, the lastest one is Gemma. Google has unveiled Gemma, a collection of lightweight, open-source AI models, following the triumph of their flagship Gemini models. Gemma targets developers aiming to integrate AI capabilities into their applications, unlike Gemini, which primarily serves end-users via platforms like search engines or virtual assistants or prompt engineering. 

Responsible AI
---------------
There are many feature that suitable for developer to start working on LLM with challenge resource. The following are main features of Gemma:
- Lightweight: Unlike Gemini, Gemma models are compact and can operate on laptops, desktops, and IoT devices, without hefty computing requirements
- Responsible AI Toolkit: Developers receive a Responsible Generative AI Toolkit alongside Gemma models, facilitating the creation of safer AI applications.
- Closed Model versus Open Source: Gemini is closed-source, while Gemma is open-source, granting developers more freedom and control.
- Target Audience: Gemini targets general consumers, whereas Gemma caters to developers seeking to integrate AI features
- Adaptability: Gemma allows for high adaptability, enabling developers to fine-tune models for specific tasks or datasets.

Inference Gemma on DGX A100:
----------------------------
To test feature of Gemma model and tools, the model and Singularity image is provide for AI developer to apply for projects.

.. code-block:: console

   $ salloc -w omega -t 1:0:0 --gres=gpu:1

Assume you get resource compute node.
In case you got many gpus, specify which one you will use.

.. code-block:: console

   export CUDA_VISIBLE_DEVICES=1

Set up environment

.. code-block:: console

   export PROMPT="ความหมาย ของ ชีวิตคืออะไร"
   export VARIANT=7b
   export  CKPT_PATH=/shared/models/Gemma/ckpt/${VARIANT}

Execute Pyton script to run interference in singularity image

.. code-block:: console

   singularity run --nv -B ${CKPT_PATH}:"/tmp/ckpt" /app/gemma.sif python scripts/run.py  --device=cuda  --ckpt=/tmp/ckpt/gemma-${VARIANT}.ckpt --variant=${VARIANT}  --prompt="${PROMPT}"

Get up and running with large language models on private cloud
==============================================================
Serving large language models (LLMs) locally can be super helpful—whether you'd like to play around with LLMs or build more powerful apps using them. But configuring your working environment and getting LLMs to run on your machine is not trivial.

So how do you run LLMs locally or on primise cloud without any of the annoyance? Enter Ollama, a platform that makes local development with open-source large language models. With Ollama, everything you need to run an LLM—model weights and all of the config—is packaged into a single Modelfile. Think kubernetes for LLMs. 

In this tutorial, we’ll take a look at how to get started with Ollama to run large language models on AI/HPC cluster . So let’s get right into the steps!

Get Source repository and make them work on K8S  for Ollama
--------------------------------


.. code-block:: console

   $ git  clone https://github.com/ollama/ollama.git

   $ cd ~/ollama/examples/kubernetes/

Modify gpu.yaml to your with your namespace. 
With follow step replace the correct namespace. 


.. code-block:: console

   $ kubectl apply -f gpu.yaml

   $ kubectl -n ollama port-forward service/ollama 11434:80

   $ kubectl get pod -n ollama

Connect to pod and pull LLM models as your want to use.


.. code-block:: console

   $ kubectl -n ollama exec --stdin --tty ollama-58fcd9f74d-8rp92  -- /bin/bash

   # ollama pull gemma2

Test on the server inside Pod: 
 
.. code-block:: console

   # ollama run gemma2 "How should Mahidol University do to be favorite place for researcher around the world in next 20 years?"

RestAPI test on host that port forwarded
------------------------------------------

On host that we set up port forward for ollama service, we can test RestAPI for model response.

.. code-block:: console 

  $ curl --noproxy "*"  http://127.0.0.1:11434/api/generate -d '{
     "model": "gemma2",
     "prompt": "How should Mahidol University do to be favorite place for researcher around the world in next 20 years?"
   }'

To deploy on Exascale cluster, ingress proxy need to be verified.

Reference:

`Get up and running with Large language model <https://ollama.com/>`_


Build LLM Apps with Low-code
==============================
Having settle down with serving LLM model, we can build application deploy those model in AI application with low-code tool for developers to build customized LLM orchestration flow & AI agents.

`Build LLM Application with FlowiseAI <https://flowiseai.com/>`_




