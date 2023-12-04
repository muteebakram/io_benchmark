#include <iostream>
#include <thread>
#include <unistd.h>
#include <fcntl.h>
#include <openssl/rand.h>
#include <chrono>
#include <vector>
#include <nlohmann/json.hpp>
#include "common.h"
using json = nlohmann::json;
using namespace std;
using namespace chrono;

#include "bench_io_uring.h"

void read_sync(std::string filename, uint64_t size) {
  char buf[BLOCK_SIZE];
  int fd = open(filename.c_str(), O_RDONLY | O_DIRECT);
  uint64_t x = 0;
  for (uint64_t i=0; i < size; i+=BLOCK_SIZE) {
    read(fd, buf, 4096);
    for (int j=0; j < BLOCK_SIZE; j+=8) {
      uint64_t b = *(uint64_t *)(buf + j);
      x = x ^ b;
    } 
  }
  fprintf(stderr, "checksum: %lld\n", x);
  close(fd);
}

void init_data(int num_workers, uint64_t file_size) {
  // Setup input files for each worker
  // TODO: Initialize files offline.
  for (int i=0; i < num_workers; i++) {
    create_data_file(getWorkerDataFileName(i), file_size);
  }
}

void bench_sync(int num_workers, uint64_t file_size) {
  // Setup input files for each worker
  // TODO: Initialize files offline.
  std::vector<std::thread> threads;
  for (uint64_t i=0; i < num_workers; i++) {
    threads.push_back(std::thread(read_sync, getWorkerDataFileName(i), file_size));
  }
  for (uint64_t i=0; i < num_workers; i++) {
    threads[i].join();
  }
}

int main() {
  json input;
  input["file_size"] = (1ULL << 30);
  input["num_workers"] = 1;
  input["should_init_data"] = true;
  input["ioengine"] = "sync";
  input["ioengine"] = "iou";
  
  uint64_t file_size = input["file_size"]; // (1ULL << 30);
  int num_workers = input["num_workers"]; // 8;
  bool should_init_data = input["should_init_data"];

  if (should_init_data) {
    init_data(num_workers, file_size);
  }
  auto begin = high_resolution_clock::now(); 
  if (input["ioengine"] == "sync") {
    bench_sync(num_workers, file_size);
  } else if (input["ioengine"] == "iou") {
    bench_iou(num_workers, file_size);
  } else {
    abort();
  }
  auto end = high_resolution_clock::now(); 
  auto duration = duration_cast<nanoseconds>(end-begin).count();
  float bw = (1e9 * num_workers * (file_size / (1ULL << 20))) / duration;
  printf("Duration: %lld\n Bandwitdh: %lf\n", duration, bw);
}
