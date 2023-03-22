import subprocess

from .utils import (
    kwargs_to_list,
    args_to_list,
    parse_sacct,
    execute,
    create_scontrol_func,
    handle_sacct_format,
)


def sbatch(jobscript=None, dependency=None, kill_on_invalid_dep=None, *args, **kwargs):
    """
    Submit a batch script to Slurm

    Many sbatch command line arguments can be passed via **kwargs. For example,
    the ``partion="compute"`` argument would be translated into the
    ``--partion=compute`` command line argument for sbatch. For all available
    options, please consult the sbatch manpage. However, some of the most useful
    argument are also documented here.


    Parameters
    ----------
    jobscript : str
        Path to jobscript file. If no jobscript is provided, you can use the
        ``wrap`` keyword to directly pass shell commands.
    depdendency : str, tuple or list
        A list of jobids this job depends on. This can also an original slurm command
        as a string, e.g., ``"afterok:1:2:3"``. The default dependency type will be ``afterok``
        which means that this job will only start if all depedending jobs have exit code 0.
        If depdendency is a tuple, the first entry defines the dependency type and the second will be the
        list of jobids, e.g., ``("afterany", [1, 2, 3])``. See also the sbatch manpage for more details.
    kill_on_invalid_dep : bool or str
        If a job has an invalid dependency and it can never run this parameter tells Slurm to terminate
        it or not. A terminated job state will be ``JOB_CANCELLED``. If this option is not specified,
        the system wide behavior applies. By default the job stays pending with reason ``DependencyNeverSatisfied``
        or if the kill_invalid_depend is specified in slurm.conf the job is terminated.

    Returns
    -------
    jobid : int
        Slurm jobid.

    Examples
    --------
    >>> from enjoy_slurm import sbatch
    >>> jobids = [slurm.sbatch(wrap=f"echo Hello World from job {i}") for in range(0,10)]
    >>> slurm.sbatch(wrap="All jobs finished", dependency=jobids)
    """
    if jobscript is None:
        jobscript = []
    else:
        jobscript = [jobscript]

    kwargs.update(
        {"dependency": dependency, "kill_on_invalid_dep": kill_on_invalid_dep}
    )

    command = (
        ["sbatch", "--parsable"]
        + args_to_list(args)
        + kwargs_to_list(kwargs)
        + jobscript
    )
    return command

    jobid = int(execute(command))

    return jobid


def sacct(jobid=None, format=None, steps=None, **kwargs):
    """
    Accounting data for all jobs and job steps in the Slurm job accounting log or Slurm database

    Parameters
    ----------
    jobid : int
        If provided, displays information about the specified job.
    format : list
        List of columns that should be shown.
    steps : str
        Jobsteps that should be shown. If ``None``, all jobsteps are returned.
        Use ``mininmal`` to return only the main inclusive step.

    Returns
    -------
    sacct info : DataFrame
        Slurm accounting data.

    """
    # return handle_sacct_format(format, kwargs)
    command = (
        ["sacct", "--parsable2"]
        + handle_sacct_format(format, kwargs)
        + kwargs_to_list(kwargs)
    )

    if jobid is not None:
        command += ["-j", str(jobid)]

    output = execute(command)

    return parse_sacct(output, steps)


def jobinfo(jobid=None, format=None, steps="minimal", **kwargs):
    """
    Accounting data for all jobs and job steps.

    Parameters
    ----------
    jobid : int
        If provided, displays information about the specified job.
    format : list
        List of columns that should be shown.
    steps : str
        Jobsteps that should be shown. If ``None``, all jobsteps are returned.
        Use ``mininmal`` to return only the main inclusive step.

    Returns
    -------
    sacct info : dict
        Slurm accounting data.

    """
    if not isinstance(format, list):
        format = [format]
    if format is not None and "JobID" not in format:
        format.append("JobID")
    acct = sacct(jobid, format, steps, **kwargs)

    return acct.set_index("JobID").to_dict(orient="index")


class SControl(type):
    def __getattr__(cls, key):
        return create_scontrol_func(key)


class scontrol(metaclass=SControl):
    """
    View or modify Slurm configuration and state
    """

    def show(*args, **kwargs):
        """
        Display state of identified entity, default is all records.

        Entity may be "aliases", "assoc_mgr", "bbstat", "burstBuffer",
        "config", "daemons", "dwstat", "federation", "frontend",
        "hostlist", "hostlistsorted", "hostnames", "job", "node",
        "partition", "reservation", "slurmd", "step", or "topology".

        """
        return create_scontrol_func("show")(*args, **kwargs)
