#!/usr/bin/python3
import os
import subprocess
import pandas as pd
import json

common_flags = [
    "--time_based", 
    "--ramp_time=4", 
    "--output-format=json",
    "--size=1M",
    "--direct=1",
    "--runtime=5",
]

workloads = ["readwrite"]
io_depths = [1] # 2, 4, 8, 16, 32, 64, 128]

test_cases = {
    "libaio": {
        "flags": ["--ioengine=libaio"]
    },
    "io_uring": {
        "flags":  ["--ioengine=io_uring"]
    },
    "io_uring_user_sqpoll": {
        "flags":  ["--ioengine=io_uring", "--sqthread_poll=1"]
    }
}

#TODO: Make this a flag.
FIO_BIN = "fio" # Assumes FIO is in $PATH. 
RESULT_PATH = "iodepth/iodepth_results.json" 


os.makedirs("data", exist_ok=True)
results = []
for tc_name,params in test_cases.items():
    for workload in workloads:
        for io_depth in io_depths:
            process = [FIO_BIN]
            process += common_flags
            process += [f"--iodepth={io_depth}"]
            process += params["flags"]
            process += ["--readwrite="+workload]
            # Since we run sequentially, its ok to reuse the name
            process += ["--name=test"] 
            process += ["--filename=data/input_data"] 
            print(process)
            result = subprocess.run(process, capture_output=True)
            results.append(json.loads(result.stdout))

# Spit out all the results to a file.
# We will analyze these offline.
result_string = json.dumps(results)
with open(RESULT_PATH, "w") as result_f:
    result_f.write(result_string)
