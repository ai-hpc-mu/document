Electrical Energy  Saving
=========================
We can actually save money by using electricity and running appliances at these specific times of day. 

What are peak hours?
---------------------
On-peak hours are the hours of the day during which demand for electricity is the highest. During this time period, you will be paying the highest amount per kilowatt-hour used. 

.. note::
 Thailand On Peak:  9am. - 10pm.

What are off-peak hours?
-------------------------
Conversely to peak hours, off-peak hours are the times when electricity prices are cheaper. 

 .. note::
  Thailand Off Peak: 10pm. - 9am.


How much we can save Electrical bill if we run job Off Peak?
In November 2023: 37% off
`Time of Use Tariff <https://www.pea.co.th/Portals/0/demand_response/Electricity%20Reconsider.pdf?ver=2018-10-01-155123-370>`_

Recommend to submit job witch schedule to run during OFF PEAK
-------------------------------------------------------------

It may sometimes be useful to submit a job and tell Slurm to defer scheduling until later. This is possible using the --begin option, which works with both sbatch and srun. The job will be submitted immediately, but only considered to run at the specified time in the future. Some examples below:
.. example-code::
    #!/bin/bash

    #SBATCH --job-name=SubmitDelay
    #SBATCH --account=ict
    #SBATCH --partition=batch
    #SBATCH --begin=15:25

    hostname
    date

