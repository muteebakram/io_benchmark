set -x
#!/bin/bash

# Read/write types
readwrite="read randread write randwrite readwrite randrw"

# Number of jobs
numjobs="1 2 4 8 16 32 64 128 256 512 1024 2048"

# Block sizes
blocksize="1k 2k 4k 8k 16k 32k 64k 128k 256k 512k 1m 2m"

# Zone sizes
zonesize="512k 1m 2m 4m 8m 16m 32m 64m 128m 256m 512m 1g"

# I/O protocols
ioengine="psync libaio io_uring"

# Async I/O queue sizes
iodepth="1 2 4 8 16 32 64 128"

# I/O size
size="1m"

# runtime used with time_based
runtime="30"

for io in ${ioengine}; do
  # for pattern in ${readwrite}; do
  #   for job in ${numjobs}; do
  #     filename="${io}_${pattern}_jobs_${job}"
  #     echo "${io} I/O, readwritepattern: ${pattern}, jobs: ${job}, filename: ${filename}"
  #     sync
  #     fio --name=${filename} --filename=${filename} --ioengine=${io} --size=${size} --time_based --runtime=${runtime} --ramp_time=4 --readwrite=${pattern} --direct=1 --numjobs=${job} --group_reporting --output-format=json --output="${filename}.json"
  #   done
  # done
  # for pattern in ${readwrite}; do
  #   for bs in ${blocksize}; do
  #     filename="${io}_${pattern}_blocksize_${bs}"
  #     echo "${io} I/O, readwritepattern: ${pattern}, blocksize: ${bs}, filename: ${filename}"
  #     sync
  #     fio --name=${filename} --filename=${filename} --ioengine=${io} --size=${size} --time_based --runtime=${runtime} --ramp_time=4 --readwrite=${pattern} --direct=1 --blocksize=${bs} --output-format=json --output="${filename}.json"
  #   done
  # done
  # for pattern in ${readwrite}; do
  #   for zs in ${zonesize}; do
  #     filename="${io}_${pattern}_zonesize_${bs}"
  #     echo "${io} I/O, readwritepattern: ${pattern}, zonesize: ${zs}, filename: ${filename}"
  #     sync
  #     fio --name=${filename} --filename=${filename} --ioengine=${io} --size=${size} --time_based --runtime=${runtime} --ramp_time=4 --readwrite=${pattern} --direct=1 --zonesize=${zs} --output-format=json --output="${filename}.json"
  #   done
  # done
  for pattern in ${readwrite}; do
    for depth in ${iodepth}; do
      filename="${io}_${pattern}_iodepth_${depth}"
      echo "${io} I/O, readwritepattern: ${pattern}, iodepth: ${depth}, filename: ${filename}"
      sync
      fio --name=${filename} --filename=${filename} --ioengine=${io} --size=${size} --time_based --runtime=${runtime} --ramp_time=4 --readwrite=${pattern} --direct=1 --iodepth=${depth} --output-format=json --output="${filename}.json"
    done
  done
done
