import os, json

read_iops = []
write_iops = []
# io_portocol = "sqthread"
io_portocol = "io_uring_readwrite_iodepth_"
data_path = "data/"

for file_name in [file for file in os.listdir(data_path)]:
    if io_portocol in file_name:
        with open(data_path + file_name) as json_file:
            data = json.load(json_file)
            read_iops.append(data["jobs"][0]["read"]["iops"])
            write_iops.append(data["jobs"][0]["write"]["iops"])

print(read_iops)
print(write_iops)
