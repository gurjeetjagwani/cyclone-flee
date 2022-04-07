# **Remote execution on a supercomputer**

These advanced tasks are intended for those who have access to the Eagle supercomputer.

## **Setup tasks for advanced use**
Before running any simulation on a remote supercomputer, the following is required:

1. Make sure the target remote machine is properly defined in `(FabSim Home)/deploy/machines.yml` 

2. In Flee, some python libraries such as `numpy` will be used for the job execution, in case of nonexistent of those packages, we recommended to install a virtual environment (*_venv_*) on the target machine. It can be done by running:
	- For QCG machine: 
		```sh
		fab qcg install_app:QCG-PilotJob,venv=True
		```
	- For SLURM machine: 
		```sh
		fab <remote_machine_name> install_app:QCG-PilotJob,venv=True
		```

		!!! note
			The installation path (``virtual_env_path``) is set on ``machines.yml`` as one of parameters for the target remote machine. By installing this ``_venv_`` on the target remote machine, the QCG Pilot Job (https://github.com/vecma-project/QCG-PilotJob) service will be also installed alongside with other required dependencies.

## *Running an ensemble simulation on a supercomputer using Pilot Jobs and QCG Broker*
1. To run an ensumble simulation on QCG machine using Pilot Jobs, run the following:
	```sh
	fabsim qcg flee_ensemble:<conflict_name>,N=20,simulation_period=<number>,PJ=true
	```
	or
	```sh
	fabsim <remote_machine_name> flee_ensemble:<conflict_name>,replicas=20,simulation_period=<number>,PJ=true
	```
	
	To showcase the execution of ensemble simulation using Pilot Job, simply run Mali conflict instance:
		```sh
		fabsim eagle_vecma flee_ensemble:mali,replicas=20,simulation_period=50,PJ=true
		```

2. To check if your jobs are finished or not, simply run:
	```sh
	fabsim qcg/<remote_machine_name> job_stat_update
	```

3. Run the following command to copy back results from ``qcg`` or remote machine. The results will then be in a directory inside ``(FabSim Home)/results``, which is most likely called ``<conflict_name>_qcg_<number>`` or ``<conflict_name>_<remote_machine_name>_<number>`` (e.g. ``mali_qcg_16`` or ``mali_eagle_vecma_16``)
	```sh
	fabsim qcg/<remote_machine_name> fetch_results
	```
	
4. To generate plots from the obtained results:
	```sh
	fabsim localhost plot_uq_output:<conflict_name>_qcg_<number>,out
	```

## **Running the coupled simulation on a supercomputer**
1. To execute simulation jobs on a supercomputer, simply run: 
	```sh
	fabsim <remote_machine_name> flee_conflict_forecast:<conflict name>,N=20,simulation_period=<number>
	```

2. To check if your jobs are finished or not, simply type
	```sh
	fabsim <remote_machine_name> job_stat_update
	```

3. Run the following command to copy back results from `eagle` machine. The results will then be in a directory inside ``(FabSim Home)/results``, which is most likely called ``<conflict_name>_<remote_machine_name>_<number>`` (e.g. ``mali_eagle_vecma_16``):
	```sh
	fabsim <remote_machine_name> fetch_results
	```

4. To generate plots from the obtained results, simply type:
	```sh
	fabsim localhost plot_uq_output:<conflict_name>_<remote_machine_name>_<number>,out
	```

NOTE: We use the parameter ''replicas'' to indicate the number of replicated Flee instances, and the parameter ''N'' to indicate the number of replicated Flare instances. In most cases, Flare will exhibit a much higher degree of aleatoric uncertainty than Flee.
