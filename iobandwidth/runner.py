#!/usr/bin/python3
import os
import json
import subprocess

# TODO: Make this a flag.
FIO_BIN = "fio"  # Assumes FIO is in $PATH.
RESULT_PATH = "iobandwidth_results.json"

common_flags = [
    # fio will run for given runtime, if completed it will loop over the same run.
    "--time_based",
    # fio starts reporting after ramp_time to ensure io's are kick started.
    "--ramp_time=4",
    "--output-format=json",
    # fio size for i/o input operation file.at=json",
    "--size=1G",
    # fio forces to use direct buffer i.e, read/write to the disk without cache.
    # Used to evaluate drive performance but not real world as cache play important role for speed up.
    "--direct=1",
    # fio runs for so many seconds.
    "--runtime=30",
    # fio combine report of num_jobs (process/threads) instead of reporting per process performance.
    "--group_reporting",
    # fio provides report of percentile of latency.
    "--lat_percentiles=1",
]

workloads = ["read"]

# Number of io request to be kept ready in the queue.
# io_depths = [1]
io_depths = [1, 4, 16, 64, 128]

# Number of CPU cores to be utilized to initiate fio task.
# cpus_allowed = [1]
cpus_allowed = [2, 4, 8, 16, 32]

EXPERIMENT_LIST = {
    "CoresVsIOBandwidth": {
        "aio": {"flags": ["--ioengine=libaio"]},
        "iou": {"flags": ["--ioengine=io_uring"]},
        "iou+p": {"flags": ["--ioengine=io_uring", "--hipri=1"]},
        "iou+k": {"flags": ["--ioengine=io_uring"]},
    }
}


os.makedirs("data", exist_ok=True)


def run_experiment(experiment_name, experiments):
    results = []
    for tc_name, params in experiments.items():
        for workload in workloads:
            for cpus in cpus_allowed:
                for io_depth in io_depths:
                    process = [FIO_BIN]
                    process += common_flags
                    process += [f"--iodepth={io_depth}"]
                    process += ["--readwrite=" + workload]
                    # Since we run sequentially, its ok to reuse the name
                    process += [f"--name={experiment_name}_{tc_name}"]
                    process += ["--filename=data/input_data"]
                    process += [f"--numjobs={cpus}"]
                    process += [f"--cpus_allowed=0-{cpus - 1}"]  # CPUs start with 0.
                    process += params["flags"]
                    # For iou+k, add number of kernel threads to be used for kernel polling.
                    if tc_name == "iou+k":
                        process += [f"--sqthread_poll={cpus}"]

                    print(" ".join(process))
                    result = subprocess.run(process, capture_output=True)
                    result_json = json.loads(result.stdout)
                    result_json["test_name"] = tc_name
                    result_json["experiment_name"] = experiment_name
                    results.append(result_json)

    return results


def run_all_experiments():
    results = []
    for name, exp in EXPERIMENT_LIST.items():
        results += run_experiment(name, exp)

    # Spit out all the results to a file.
    # We will analyze these offline.
    result_string = json.dumps(results)
    with open(RESULT_PATH, "w") as result_f:
        result_f.write(result_string)


run_all_experiments()
