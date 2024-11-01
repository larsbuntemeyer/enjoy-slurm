import copy
from os import path as op
from pathlib import Path
from warnings import warn

from .parser import (
    handle_sacct_format,
    kwargs_to_list,
    parse_header,
    parse_sacct,
    split_script,
)
from .utils import (  # create_scontrol_func,
    execute,
    interp_from_shebang,
    shebang_from_interp,
)


def sbatch(
    jobscript=None,
    dependency=None,
    dependency_type=None,
    kill_on_invalid_dep=None,
    verbose=False,
    **kwargs,
):
    """
    Submit a batch script to Slurm

    All of sbatch command line arguments that are not explicitly documented here can
    still be passed via ``**kwargs``. For example, ``partition="compute"`` would be
    translated into the ``--partion compute`` command line argument for sbatch.
    For all available options, please consult the sbatch manpage.
    However, some of the most useful argument are also documented here.

    Parameters
    ----------
    jobscript : str
        Path to jobscript file. If no jobscript is provided, you can use the
        ``wrap`` keyword to directly pass shell commands.
    depdendency : str, tuple or list
        A list of jobids this job depends on. This can also be an original slurm command
        as a string, e.g., ``"afterok:1:2:3"``. The default dependency type will be ``afterok``
        which means that this job will only start if all depedending jobs have exit code 0.
        To set the dependency type, use the ``dependency_type`` keyword. See also the sbatch
        manpage for more details.
    depdendency_type: str
        The type of the dependency. This can be ``afterok``, ``afternotok``, ``afterany``,
        ``after`` or ``singleton``. The default is ``afterok``. Only applies if ``dependency`` is a list.
    kill_on_invalid_dep : bool or str
        If a job has an invalid dependency and it can never run, this parameter tells Slurm to terminate
        it or not. A terminated job state will be ``JOB_CANCELLED``. If this option is not specified,
        the system wide behavior applies. By default the job stays pending with reason ``DependencyNeverSatisfied``
        or if the kill_invalid_depend is specified in slurm.conf the job is terminated.
    verbose : bool
        Print sbatch command.

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
        {
            "dependency": dependency,
            "kill_on_invalid_dep": kill_on_invalid_dep,
            "dependency_type": dependency_type,
        }
    )

    command = ["sbatch", "--parsable"] + kwargs_to_list(kwargs) + jobscript

    jobid = int(execute(command, verbose=verbose))

    return jobid


def sacct(jobid=None, format=None, steps=None, verbose=False, **kwargs):
    """
    Accounting data for all jobs and job steps in the Slurm job accounting log or Slurm database

    Parameters
    ----------
    jobid : int
        If provided, displays information about the specified job.
    format : list
        List of columns that should be shown.
    steps : str
        Jobsteps that should be shown. If ``all``, all jobsteps are returned.
        Use ``mininmal`` to return only the main inclusive step. Default us ``minimal``.
    verbose : bool
        Print sacct command.

    Returns
    -------
    sacct info : DataFrame
        Slurm accounting data.

    """
    if steps is None:
        steps = "minimal"
    # return handle_sacct_format(format, kwargs)
    command = (
        ["sacct", "--parsable2"]
        + handle_sacct_format(format, kwargs)
        + kwargs_to_list(kwargs)
    )

    if jobid is not None:
        command += ["-j", str(jobid)]

    output = execute(command, verbose=verbose)

    return parse_sacct(output, steps)


def jobinfo(jobid=None, format=None, steps=None, **kwargs):
    """
    Accounting data for all jobs and job steps.

    Parameters
    ----------
    jobid : int
        If provided, displays information about the specified job.
    format : list
        List of columns that should be shown.
    steps : str
        Jobsteps that should be shown. If ``all``, all jobsteps are returned.
        Use ``mininmal`` to return only the main inclusive step. Default is ``minimal``.

    Returns
    -------
    sacct info : dict
        Slurm accounting data.

    """
    if format is not None and not isinstance(format, list):
        format = [format]
    if format is not None and "JobID" not in format:
        format.append("JobID")
    acct = sacct(jobid, format, steps, **kwargs)

    return acct.set_index("JobID").to_dict(orient="index")


# class SControl(type):
#     def __getattr__(cls, key):
#         return create_scontrol_func(key)


# class scontrol(metaclass=SControl):
#     """
#     View or modify Slurm configuration and state
#     """

#     def show(*args, **kwargs):
#         """
#         Display state of identified entity, default is all records.

#         Entity may be "aliases", "assoc_mgr", "bbstat", "burstBuffer",
#         "config", "daemons", "dwstat", "federation", "frontend",
#         "hostlist", "hostlistsorted", "hostnames", "job", "node",
#         "partition", "reservation", "slurmd", "step", or "topology".

#         """
#         return create_scontrol_func("show")(*args, **kwargs)


class Job:
    """
    Slurm Job class.

    The Job class can manage meta data and submission of a Slurm job.

    Parameters
    ----------
    job : str
        Path to jobscript or a command that should be wrapped.
    jobid : int
        Jobid to create a Job instance from.

    Returns
    -------
    job : Job
        Job instance either created from jobid or jobscript.
    """

    def __init__(
        self,
        job=None,
        jobid=None,
        interpreter=None,
        shebang=None,
        verbose=False,
        **kwargs,
    ):
        self.job = job
        self.jobid = jobid
        self.interpreter = interpreter
        self.shebang = shebang
        self.verbose = verbose
        self.kwargs = kwargs
        self.config = {}
        self.filename = None

        if job is None:
            self.job = ""
        self.wrap = None

        if op.isfile(self.job):
            self.filename = op.abspath(self.job)
            self._init_from_file()
        elif job:
            self.job = job
            self.filename = None
            self._init_from_job()

        if self.jobid and not self.jobinfo():
            warn(f"jobid {self.jobid} seems to be invalid")

    @property
    def script(self):
        return self.shebang + "\n" + self.header + "\n" + self.command

    def _init_from_file(self):
        """Init job from file"""
        self.path = Path(self.filename)
        with open(self.filename) as f:
            self.job = f.read()
        self._init_from_job()

    def _init_from_job(self):
        """Init job from string"""

        self.header, self.command, shebang = split_script(self.job, strip=True)
        self.config = parse_header(self.header, eval_types=True)
        self.config.update(self.kwargs)

        if not self.shebang and shebang:
            self.shebang = shebang

        if not self.interpreter and self.shebang:
            self.interpreter = interp_from_shebang(self.shebang)
        elif self.interpreter and not self.shebang:
            self.shebang = shebang_from_interp(self.interpreter)

    def __eq__(self, other):
        return self.jobid == other.jobid

    def __getattr__(self, key):
        return self.jobinfo(format=key)

    def __repr__(self):
        indent = 2 * " "
        # txt = f"job         : {self.job}\n"
        txt = f"filename    : {self.filename}\n"
        txt += f"jobid       : {self.jobid}\n\n"
        txt += "Slurm\n"
        for k, v in self.config.items():
            txt += indent + f"{k} : {v}\n"
        return txt

    @property
    def fields(self):
        """Available job attributes"""
        return list(self.sacct(format="all").columns)

    def sbatch(self, **kwargs):
        """Submit job to Slurm"""
        config = self.config.copy()
        config.update(kwargs)
        jobid = sbatch(self.filename, wrap=self.wrap, **config)
        # self.scontrol = scontrol.show(jobid=jobid)
        if self.jobid is None:
            self.jobid = jobid
            return self
        job = copy.copy(self)
        job.jobid = jobid
        return job

    def sacct(self, **kwargs):
        """Get accounting for this job"""
        if self.jobid:
            return sacct(jobid=self.jobid, **kwargs)
        return None

    def jobinfo(self, **kwargs):
        """Jobinfo as dictionary"""
        if self.jobid:
            return jobinfo(self.jobid, **kwargs)
        return None

    def run(self):
        """Run the script without submitting it so Slurm."""
        command = [self.interpreter, self.filename]
        return execute(command)
