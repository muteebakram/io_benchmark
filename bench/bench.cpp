#include <iostream>
#include <thread>
#include <unistd.h>
#include <fcntl.h>
#include <openssl/rand.h>
#include <chrono>
#include <vector>
using namespace std;
using namespace chrono;

#define BLOCK_SIZE 4096


int create_data_file(std::string filename, uint64_t size) {
  char buf[BLOCK_SIZE];
  int fd = open(filename.c_str(), O_WRONLY | O_CREAT | O_TRUNC,  0644);
  for (uint64_t i=0; i < size; i+=BLOCK_SIZE) {
    RAND_bytes((unsigned char *)buf, BLOCK_SIZE);
    write(fd, buf, 4096);
  }
  close(fd);
  return 0;
}

void read_data(std::string filename, uint64_t size) {
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

std::string getWorkerDataFileName(int i) {
  return "test." + std::to_string(i);
}

void init_data(int num_workers, uint64_t file_size) {
  // Setup input files for each worker
  // TODO: Initialize files offline.
  for (int i=0; i < num_workers; i++) {
    create_data_file(getWorkerDataFileName(i), file_size);
  }
}

void bench(int num_workers, uint64_t file_size) {
  // Setup input files for each worker
  // TODO: Initialize files offline.
  std::vector<std::thread> threads;
  for (uint64_t i=0; i < num_workers; i++) {
    threads.push_back(std::thread(read_data, getWorkerDataFileName(i), file_size));
  }
  for (uint64_t i=0; i < num_workers; i++) {
    threads[i].join();
  }
}

int main() {
  uint64_t file_size = (1ULL << 30);
  int num_workers = 8;
  bool should_init_data = true;
  if (should_init_data) {
    init_data(num_workers, file_size);
  }
  auto begin = high_resolution_clock::now(); 
  bench(num_workers, file_size);
  auto end = high_resolution_clock::now(); 
  auto duration = duration_cast<nanoseconds>(end-begin).count();
  float bw = (1e9 * num_workers * (file_size / (1ULL << 20))) / duration;
  printf("Duration: %lld\n Bandwitdh: %lf\n", duration, bw);
}
