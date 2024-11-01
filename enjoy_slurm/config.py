delimiter = "|"

skip_args = [
    "dependency_type",
]

default_sacct_format = [
    "jobid",
    "elapsed",
    "ncpus",
    "ntasks",
    "state",
    "start",
    "end",
    "jobname",
]

# interpreter dictionary
interp_dict = {
    "bourne": ["/bin/sh"],
    "bash": ["bash"],
    "python3": ["python3"],
    "python2": ["python2"],
    "python": ["python"],
}

# shebang
shebang_format = "#!/usr/bin/env {exe}"

shebang_dict = {
    "bourne": "#!/bin/sh",
    "bash": "#!/bin/bash",
}

fields = """
Fields available:

 Account             AdminComment        AllocCPUS           AllocNodes
 AllocTRES           AssocID             AveCPU              AveCPUFreq
 AveDiskRead         AveDiskWrite        AvePages            AveRSS
 AveVMSize           BlockID             Cluster             Comment
 Constraints         ConsumedEnergy      ConsumedEnergyRaw   CPUTime
 CPUTimeRAW          DBIndex             DerivedExitCode     Elapsed
 ElapsedRaw          Eligible            End                 ExitCode
 Flags               GID                 Group               JobID
 JobIDRaw            JobName             Layout              MaxDiskRead
 MaxDiskReadNode     MaxDiskReadTask     MaxDiskWrite        MaxDiskWriteNode
 MaxDiskWriteTask    MaxPages            MaxPagesNode        MaxPagesTask
 MaxRSS              MaxRSSNode          MaxRSSTask          MaxVMSize
 MaxVMSizeNode       MaxVMSizeTask       McsLabel            MinCPU
 MinCPUNode          MinCPUTask          NCPUS               NNodes
 NodeList            NTasks              Priority            Partition
 QOS                 QOSRAW              Reason              ReqCPUFreq
 ReqCPUFreqMin       ReqCPUFreqMax       ReqCPUFreqGov       ReqCPUS
 ReqMem              ReqNodes            ReqTRES             Reservation
 ReservationId       Reserved            ResvCPU             ResvCPURAW
 Start               State               Submit              Suspended
 SystemCPU           SystemComment       Timelimit           TimelimitRaw
 TotalCPU            TRESUsageInAve      TRESUsageInMax      TRESUsageInMaxNode
 TRESUsageInMaxTask  TRESUsageInMin      TRESUsageInMinNode  TRESUsageInMinTask
 TRESUsageInTot      TRESUsageOutAve     TRESUsageOutMax     TRESUsageOutMaxNode
 TRESUsageOutMaxTask TRESUsageOutMin     TRESUsageOutMinNode TRESUsageOutMinTask
 TRESUsageOutTot     UID                 User                UserCPU
 WCKey               WCKeyID             WorkDir
"""
