set -x
#!/bin/bash

# Read/write types
readwrite="readwrite"

# I/O protocols
ioengine="libaio io_uring"

# Async I/O queue sizes
iodepth="1 2 4 8 16 32 64 128"

# I/O size
size="1m"

# runtime used with time_based
runtime="5"

mkdir data;

for io in ${ioengine}; do
  for pattern in ${readwrite}; do
    for depth in ${iodepth}; do
      filename="${io}_${pattern}_iodepth_${depth}"
      echo "${io} I/O, readwritepattern: ${pattern}, iodepth: ${depth}, filename: ${filename}"
      sync
      fio --name=${filename} --filename="data/${filename}.fio" --ioengine=${io} --size=${size} --time_based --runtime=${runtime} --ramp_time=4 --readwrite=${pattern} --direct=1 --iodepth=${depth} --output-format=json --output="${filename}.json"
    done
  done
done

# TODO iouring with polling requires specific kernel version and file system. Ex: kernel 5.7 and newer supports polling on ext4.
# for pattern in ${readwrite}; do
#   for depth in ${iodepth}; do
#     filename="io_uring_iothread_poll_${pattern}_iodepth_${depth}"
#     echo "io_uring IOPOLL I/O, readwritepattern: ${pattern}, iodepth: ${depth}, filename: ${filename}"
#     sync
#     fio --name=${filename} --filename="data/${filename}.fio" --ioengine="io_uring" --hipri=1 --size=${size} --time_based --runtime=${runtime} --ramp_time=4 --readwrite=${pattern} --direct=1 --iodepth=${depth} --output-format=json --output="${filename}.json"
#   done
# done

# sqthread_poll="1 2 4 8 16 32"
sqthread_poll="1"
for thread in ${sqthread_poll}; do
  for pattern in ${readwrite}; do
    for depth in ${iodepth}; do
      filename="io_uring_sqthread_poll_${thread}_${pattern}_iodepth_${depth}"
      echo "io_uring SQPOLL I/O, readwritepattern: ${pattern}, iodepth: ${depth}, filename: ${filename}"
      sync
      sudo fio --name=${filename} --filename="data/${filename}.fio" --ioengine="io_uring" --sqthread_poll=${thread} --size=${size} --time_based --runtime=${runtime} --ramp_time=4 --readwrite=${pattern} --direct=1 --iodepth=${depth} --output-format=json --output="${filename}.json"
    done
  done
done
