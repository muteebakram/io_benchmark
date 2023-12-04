#ifndef BENCH_IO_URING_H
#define BENCH_IO_URING_H

#include <sys/uio.h>
#include <sys/ioctl.h>
#include <stdlib.h>

#include <liburing.h>
#include "common.h"

#define QUEUE_DEPTH 128
#define SQPOLL_CPU 1

struct readReqResp {
  uint64_t block_id; // Offset of block that was read.
  struct iovec iov; // Read Result.
  char buf[BS];
};
struct io_uring *init_rings(int num_workers, json options){
  struct io_uring *rings = new io_uring[num_workers];
  struct io_uring_params params;
  bool use_sqthread_poll = options["sqthread_poll"];
  bool use_sqthread_pin = options["sqthread_poll_pin"];
  int num_sqthread_workers = options["num_sqthread_workers"];

  for (int i=0; i < num_workers; i++) {
    memset(&params, 0, sizeof(params));
    if (use_sqthread_poll) {
      params.flags |= IORING_SETUP_SQPOLL;
      params.sq_thread_idle = 2000;

      if (i >= num_sqthread_workers && num_sqthread_workers!=0) {
          params.wq_fd = rings[i%num_sqthread_workers].ring_fd;
          params.flags |= IORING_SETUP_ATTACH_WQ;
      } else {
     	  params.flags |= IORING_SETUP_SQ_AFF;
          params.sq_thread_cpu = i;
      }
    }
    io_uring_queue_init_params(QUEUE_DEPTH, &rings[i], &params);
  }
  return rings;
}

void read_iou(std::string filename, uint64_t file_size, struct io_uring *ring) {
  uint64_t num_blocks = file_size / BS;
  int fd = open(filename.c_str(), O_RDONLY | O_DIRECT);

  struct readReqResp *re = (struct readReqResp *)malloc(QUEUE_DEPTH * sizeof(readReqResp));
  for (int i=0; i < QUEUE_DEPTH; i++) {
    re[i].iov.iov_base = re[i].buf;
    re[i].iov.iov_len = BS;
    re[i].block_id = rand() % num_blocks;

    struct io_uring_sqe *sqe = io_uring_get_sqe(ring);
    io_uring_prep_readv(sqe, fd, &(re[i].iov), 1, re[i].block_id * BS);
    io_uring_sqe_set_data(sqe, &re[i]);
    int ret = io_uring_submit(ring);
    if (ret < 0) abort();
  }

  uint64_t num_blocks_read = 0;
  while (true) {
    struct io_uring_cqe *cqe;
    int ret = io_uring_wait_cqe(ring, &cqe);
    if (ret == -EAGAIN) {
      continue;
    }
    if (ret < 0) {
      abort();
    }
    struct readReqResp *resp= (struct readReqResp *)io_uring_cqe_get_data(cqe);
    check_block((char *)resp->buf, resp->block_id);
    io_uring_cqe_seen(ring, cqe);
    num_blocks_read++;

    // Let's add the resp back into the queue as a request.
    struct readReqResp *nextReq = resp;
    nextReq->block_id = rand() % num_blocks;
    struct io_uring_sqe *sqe = io_uring_get_sqe(ring);
    io_uring_prep_readv(sqe, fd, &(nextReq->iov), 1, nextReq->block_id * BS);
    io_uring_sqe_set_data(sqe, nextReq);
    ret = io_uring_submit(ring);
    if (ret < 0) abort();
  }

  return;
}

void bench_iou(int num_workers, uint64_t file_size, json options) {
  struct io_uring *rings = init_rings(num_workers, options);
  std::vector<std::thread> threads;
  for (uint64_t i=0; i < num_workers; i++) {
    threads.push_back(std::thread(read_iou, getWorkerDataFileName(i), file_size, &rings[i]));
  }
  for (uint64_t i=0; i < num_workers; i++) {
    threads[i].join();
  }
}

#endif
