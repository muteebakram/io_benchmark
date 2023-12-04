#ifndef BENCH_IO_URING_H
#define BENCH_IO_URING_H

#include <sys/uio.h>
#include <sys/ioctl.h>
#include <stdlib.h>

#include <liburing.h>
#include "common.h"

#define QUEUE_DEPTH 128

struct read_entry {
  uint64_t block_id; // Offset of block that was read.
  struct iovec iov; // Read Result.
};

void read_iou(std::string filename, uint64_t file_size) {
  struct io_uring ring;
  io_uring_queue_init(QUEUE_DEPTH, &ring, 0 /* params */);
  printf("%d\n", ring.ring_fd);

  int fd = open(filename.c_str(), O_RDONLY | O_DIRECT);
  char buf[BLOCK_SIZE];

  // We need one iovec for each read.
  struct read_entry re;
  re.block_id = 123; // Read first 4 kb
  re.iov.iov_base = buf;
  re.iov.iov_len = BLOCK_SIZE;

  /* Get an SQE */
  struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);
  io_uring_prep_readv(sqe, fd, &re.iov, 1, 0);
  io_uring_sqe_set_data(sqe, &re);
  io_uring_submit(&ring);

  struct io_uring_cqe *cqe;
  int ret = io_uring_wait_cqe(&ring, &cqe);
  if (ret < 0) {
      perror("io_uring_wait_cqe");
      return;
  }
  struct read_entry *reFromQ = (struct read_entry *)io_uring_cqe_get_data(cqe);
  io_uring_cqe_seen(&ring, cqe);
  return;
}

void bench_iou(int num_workers, uint64_t file_size) {
  read_iou(getWorkerDataFileName(0), 10000);
}

#endif
