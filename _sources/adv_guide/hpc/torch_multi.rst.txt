Pytorch DISTRIBUTED DATA PARALLEL
=================================

Motivated by how fast we can train Large language model (LLM) on multi-gpu multi-node. DistributedDataParallel (DDP) implements data parallelism at the module level which can run across multiple machines. Applications using DDP should spawn multiple processes and create a single DDP instance per process. DDP uses collective communications in the torch.distributed package to synchronize gradients and buffers. More specifically, DDP registers an autograd hook for each parameter given by model.parameters() and the hook will fire when the corresponding gradient is computed in the backward pass. Then DDP uses that signal to trigger gradient synchronization across processes. 

`GETTING STARTED WITH DISTRIBUTED DATA PARALLEL <https://pytorch.org/tutorials/intermediate/ddp_tutorial.html>`_

Multi-node Multi-GPU Training
-----------------------------
The code in this tutorial runs on an 2-GPU  each on two DGX A100 servers, but it can be easily generalized to other environments.

Pre-requirement installing Pytorch with GPU support on Slurm Cluster.
`Install PyTorch <https://pytorch.org/get-started/locally/>`_

Toy model with PyTorch 
----------------------

PyTorch Elastic to simplify the DDP code and initialize the job more easily. Let’s still use the Toymodel example and create a file named elastic_ddp.py.

elastic_ddp.py::

        import torch
        import torch.distributed as dist
        import torch.nn as nn
        import torch.optim as optim

        from torch.nn.parallel import DistributedDataParallel as DDP

        class ToyModel(nn.Module):
            def __init__(self):
                super(ToyModel, self).__init__()
                self.net1 = nn.Linear(10, 10)
                self.relu = nn.ReLU()
                self.net2 = nn.Linear(10, 5)

            def forward(self, x):
                return self.net2(self.relu(self.net1(x)))


        def demo_basic():
            dist.init_process_group("nccl")
            rank = dist.get_rank()
            print(f"Start running basic DDP example on rank {rank}.")
        
            # create model and move it to GPU with id rank
            device_id = rank % torch.cuda.device_count()
            model = ToyModel().to(device_id)
            ddp_model = DDP(model, device_ids=[device_id])

            loss_fn = nn.MSELoss()
            optimizer = optim.SGD(ddp_model.parameters(), lr=0.001)

            optimizer.zero_grad()
            outputs = ddp_model(torch.randn(20, 10))
            labels = torch.randn(20, 5).to(device_id)
            loss_fn(outputs, labels).backward()
            optimizer.step()
            dist.destroy_process_group()

        if __name__ == "__main__":
            demo_basic()
.. code-block:: python
The script file for launch Slurm interactive job::

        #!/bin/bash 
        export MASTER_ADDR=$(scontrol show hostname ${SLURM_NODELIST} | head -n 1) 
        torchrun --nnodes=2 --nproc_per_node=2 --rdzv_id=100 --rdzv_backend=c10d --rdzv_endpoint=$MASTER_ADDR:29400 elastic_ddp.py 
.. code-block:: bash
Launch interactive job on Slurm cluster::

   $ srun --nodes=2 --gres=gpu:2 ./torchrun_script.sh 
.. code-block:: console
