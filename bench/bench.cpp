#include <iostream>
#include <thread>
#include <unistd.h>
#include <fcntl.h>
#include <openssl/rand.h>
#include <chrono>
#include <vector>
#include <nlohmann/json.hpp>
#include "common.h"
#include <fstream>
using json = nlohmann::json;
using namespace std;
using namespace chrono;

#include "bench_io_uring.h"

void read_sync(std::string filename, uint64_t size) {
  char buf[BS];
  int fd = open(filename.c_str(), O_RDONLY | O_DIRECT);
  uint64_t x = 0;
  uint64_t block_id = 0;
  for (uint64_t i=0; i < size; i+=BS) {
    int bytes_read = 0;
    while (bytes_read < BS) {
        bytes_read += read(fd, buf, 4096);
    }
    check_block(buf, block_id++);
  }
  fprintf(stderr, "checksum: %lld\n", x);
  close(fd);
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

int main(int argc, char **argv) {
  if (argc < 2) {
      fprintf(stderr, "Please specify input benchmark JSON spec file");
      abort();
  }
  std::string options_path(argv[1]);
  std::ifstream options_ifstream(options_path);
  json options  = json::parse(options_ifstream);

  
  uint64_t file_size = options["file_size"]; // (1ULL << 30);
  int num_workers = options["num_workers"]; // 8;
  bool should_init_data = options["should_init_data"];

  if (should_init_data) {
    init_data(num_workers, file_size);
  }
  auto begin = high_resolution_clock::now(); 
  if (options["ioengine"] == "sync") {
    bench_sync(num_workers, file_size);
  } else if (options["ioengine"] == "iou") {
    bench_iou(num_workers, file_size, options);
  } else {
    abort();
  }
  auto end = high_resolution_clock::now(); 
  auto duration = duration_cast<nanoseconds>(end-begin).count();
  float bw = (1e9 * num_workers * (file_size / (1ULL << 20))) / duration;
  printf("%lf\n", bw);
}
