#!/usr/bin/python3
import os
import json
import subprocess

# TODO: Make this a flag.
FIO_BIN = "./build/bench"  # Assumes FIO is in $PATH.

# Let's start with 3 jobs, with J, J+1, J+2, J+3
MAX_CPU_ID=15
cpus_allowed = [7, 9, 11, 13, 14] # Always leave CPU 16 open as extra thread for SQPollThread

common = {
    "file_size": 4*1024*1024*1024,
    "should_init_data": False,
    "num_workers": 7
}

#   "sync": {
#       "ioengine": "sync"
#   },
#   "iou": {
#       "ioengine": "iou",
#       "sqthread_poll": False,
#       "sqthread_poll_pin": False,
#       "num_sqthread_workers": 0
#   },
#
VARIANTS = {
    "iou": {
        "ioengine": "iou",
        "sqthread_poll": False,
        "sqthread_poll_pin": False,
        "num_sqthread_workers": 0
    },
    "iou+sq": {
        "ioengine": "iou",
        "sqthread_poll": True,
        "sqthread_poll_pin": False,
        "num_sqthread_workers": 0
    },
    "iou+sq_1tp": {
        "ioengine": "iou",
        "sqthread_poll": True,
        "sqthread_poll_pin": False,
        "num_sqthread_workers": 1
    },
    "iou+sq_3tp": {
        "ioengine": "iou",
        "sqthread_poll": True,
        "sqthread_poll_pin": False,
        "num_sqthread_workers": 3
    },
    "iou+sq_5tp": {
        "ioengine": "iou",
        "sqthread_poll": True,
        "sqthread_poll_pin": False,
        "num_sqthread_workers": 5
    },
    "iou+sq_7tp": {
        "ioengine": "iou",
        "sqthread_poll": True,
        "sqthread_poll_pin": False,
        "num_sqthread_workers": 7
    }
}


def switch_on_cpus(max_cpu_id):
    for i in range(1, max_cpu_id+1):
        cpu_control_file = f'/sys/devices/system/cpu/cpu{i}/online'
        with open(cpu_control_file, "w") as outfile:
            outfile.write("1")

def switch_off_cpus(num_cpus):
    switch_on_cpus(15)
    for i in range(num_cpus, 16):
        cpu_control_file = f'/sys/devices/system/cpu/cpu{i}/online'
        with open(cpu_control_file, "w") as outfile:
            outfile.write("0")




def run_experiment():
    results = []
    for cores in cpus_allowed:
        print(cores)
        for name,variant in VARIANTS.items():
            if name == "sync":
                continue
            switch_off_cpus(cores)
            job_config = variant
            job_config.update(common)
            json_object = json.dumps(job_config, indent=4)

             # Writing to sample.json
            with open(f"workloads/{name}_{cores}.json", "w") as outfile:
                outfile.write(json_object)
            workload = subprocess.Popen([FIO_BIN, f"workloads/{name}_{cores}.json"])
            print([FIO_BIN])
            print("----------------------------------")
            print("workload: ", name)
            metrics = subprocess.run(['iotop', '-n' '10', '-b', '-o', '-p', str(workload.pid)], capture_output=True, text=True)
            workload.terminate()
            workload.kill()
            workload.wait()
            print(metrics.stdout)
            print("---------------------------------")
    switch_on_cpus(MAX_CPU_ID)

run_experiment()

