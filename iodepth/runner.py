#!/usr/bin/python3
import os
import subprocess
import pandas as pd
import json

#TODO: Make this a flag.
FIO_BIN = "fio" # Assumes FIO is in $PATH. 
RESULT_PATH = "iodepth/iodepth_results.json" 

common_flags = [
    "--time_based", 
    "--ramp_time=4", 
    "--output-format=json",
    "--size=1M",
    "--direct=1",
    "--runtime=3",
    "--group_reporting",
    "--lat_percentiles=1"
]

workloads = ["read"]
io_depths = [1, 4, 16, 64, 128]

EXPERIMENT_LIST = {
    "SingleCPU" : {
        "aio": {
            "flags": ["--ioengine=libaio", "--cpus_allowed=1"]
        },
        "iou": {
            "flags":  ["--ioengine=io_uring", "--cpus_allowed=1"]
        },
        "iou+p": {
            "flags":  ["--ioengine=io_uring", "--hipri=1", "--cpus_allowed=1"]
        },
        # We give iou+kernel a single cpu by restricting the kernel poll cpu and allowed cpu to be the same.
        "iou+k": {
            "flags":  ["--ioengine=io_uring", "--sqthread_poll", "--sqthread_poll_cpu=1", "--cpus_allowed=1"]
        }
    },
    "TwoCPU" : {
        "aio": {
            "flags": ["--numjobs=2", "--ioengine=libaio", "--cpus_allowed=1,2"]
        },
        "iou": {
            "flags":  ["--numjobs=2", "--ioengine=io_uring", "--cpus_allowed=1,2"]
        },
        "iou+p": {
            "flags":  ["--numjobs=2", "--ioengine=io_uring", "--hipri=1", "--cpus_allowed=1,2"]
        },
        "iou+k": {
            "flags":  ["--numjobs=2", "--ioengine=io_uring", "--sqthread_poll", "--sqthread_poll_cpu=1", "--cpus_allowed=1,2"]
        },
        "iou+ke": {
            "flags":  ["--numjobs=2", "--ioengine=io_uring", "--sqthread_poll", "--sqthread_poll_cpu=1", "--cpus_allowed=2"]
        }
    }
}


os.makedirs("data", exist_ok=True)
def run_experiment(experiment_name, experiments):
    results = []
    for tc_name,params in experiments.items():
        for workload in workloads:
            for io_depth in io_depths:
                process = [FIO_BIN]
                process += common_flags
                process += [f"--iodepth={io_depth}"]
                process += params["flags"]
                process += ["--readwrite="+workload]
                #Since we run sequentially, its ok to reuse the name
                process += ["--name=test"] 
                process += ["--filename=data/input_data"] 
                print(' '.join(process))
                result = subprocess.run(process, capture_output=True)
                result_json = json.loads(result.stdout)
                result_json['test_name'] = tc_name
                result_json['experiment_name'] = experiment_name
                results.append(result_json)
    return results

def run_all_experiments():
    results = []
    for name, exp in EXPERIMENT_LIST.items():
        results+= (run_experiment(name, exp))

    # Spit out all the results to a file.
    # We will analyze these offline.
    result_string = json.dumps(results)
    with open(RESULT_PATH, "w") as result_f:
        result_f.write(result_string)

run_all_experiments()
