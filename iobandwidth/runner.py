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

workloads = ["randread", "read"]

# Number of io request to be kept ready in the queue.
# io_depths = [1]
io_depths = [32, 64, 128]

# Number of CPU cores to be utilized to initiate fio task.
# cpus_allowed = [1]
# cpus_allowed = [1, 2, 4, 8, 16]
MAX_CPU_ID=127
cpus_allowed = [1, 4, 16, 64, 128] # Always leave last CPU open as extra thread for SQPollThread

EXPERIMENT_LIST = {
    "CoresVsIOBandwidth": {
        "iou": {"flags": ["--ioengine=io_uring", "--filename=data/input_data"]},
        "iou+p": {"flags": ["--ioengine=io_uring", "--hipri=1", "--filename=data/input_data"]},
        "iou+k": {"flags": ["--ioengine=io_uring", "--sqthread_poll", "--filename=data/input_data"]},
        "iou+k(+2)": {"flags": ["--ioengine=io_uring", "--sqthread_poll", "--filename=data/input_data"], 'extra_cpus': 2},
        "iou+k(+1)": {"flags": ["--ioengine=io_uring", "--sqthread_poll", "--filename=data/input_data"], 'extra_cpus': 1},
        "aio": {"flags": ["--ioengine=libaio", "--filename=data/input_data"]},
        "spdk": {"flags": ["--ioengine=/users/prikshit/spdk/build/fio/spdk_nvme", "--filename=trtype=PCIe traddr=0000.c1.00.0 ns=1", "--thread=1"]}
    }
}

os.makedirs("data", exist_ok=True)

def switch_off_cpus(min_cpu_id, max_cpu_id):
    for i in range(1, min_cpu_id):
        cpu_control_file = f'/sys/devices/system/cpu/cpu{i}/online'
        with open(cpu_control_file, "w") as outfile:
            outfile.write("1")

    print(min_cpu_id)
    for i in range(min_cpu_id, max_cpu_id+1):
        cpu_control_file = f'/sys/devices/system/cpu/cpu{i}/online'
        with open(cpu_control_file, "w") as outfile:
            outfile.write("0")



def run_experiment(experiment_name, experiments):
    results = []
    for tc_name, params in experiments.items():
        for workload in workloads:
            for cpus in cpus_allowed:
                total_cpus = cpus
                if 'extra_cpus' in params.keys():
                    total_cpus = cpus + params['extra_cpus']
                switch_off_cpus(total_cpus, MAX_CPU_ID)
                for io_depth in io_depths:
                    process = [FIO_BIN]
                    process += common_flags
                    process += [f"--iodepth={io_depth}"]
                    process += ["--readwrite=" + workload]
                    # Since we run sequentially, its ok to reuse the name
                    process += [f"--name={experiment_name}_{tc_name}"]
                    process += [f"--numjobs={cpus}"]
                    process += [f"--cpus_allowed=0-{total_cpus - 1}"]  # CPUs start with 0.
                    process += params["flags"]

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
