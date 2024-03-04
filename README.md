# io_benchmark


Analyze and benchmark different async I/O protocols like libaio, Intel SPDK, and io_uring (variants) using the fio tool.
The storage devices are getting extremely fast and have reached sub-10 microseconds latency, and the kernel support for IO needs to catch up and utilize the high bandwidth of these devices.

Recent asynchronous IO protocols like libaio, io_uring, and SPDK aim to bridge this gap. These protocols scale differently depending on the cores, storage device type, and configurations such as iodepth.

An interesting IO protocol configuration we wanted to explore is io_uring with kernel submission queue polling (SQPOLL). This option has the kernel continuously poll for submission queue requests in the shared memory submission queue, allowing users to submit IO requests without using a system call.

From our benchmark results, the io_uring SQPoll with multiple kernel workers outperforms the SQPoll pinning, and the number of kernel threads to assign depends on the workload.

## Report

[Link](./pdfs/Report%20-%20Async%20IO%20Benchmark;%20Muteeb,%20Prikshit,%20Yuvraj.pdf)