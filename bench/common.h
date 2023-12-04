#ifndef COMMON_H
#define COMMON_H

#define BS 4096

std::string getWorkerDataFileName(int i) {
  return "test." + std::to_string(i);
}


int create_data_file(std::string filename, uint64_t filesize) {
  uint64_t buf[BS/sizeof(uint64_t)];
  int fd = open(filename.c_str(), O_WRONLY | O_CREAT | O_TRUNC,  0644);
  for (uint64_t i=0; i < filesize; i+=BS) {
    for (uint64_t j=0; j<BS/sizeof(uint64_t); j++) {
      buf[j] = i + j;
    }
    int ret = pwrite(fd, (char *)buf, BS, i);
    if (ret < 0) {
      perror("write");
      abort();
    }
  }
  close(fd);
  return 0;
}


void init_data(int num_workers, uint64_t file_size) {
  // Setup input files for each worker
  // TODO: Initialize files offline.
  for (int i=0; i < num_workers; i++) {
    create_data_file(getWorkerDataFileName(i), file_size);
  }
}

uint64_t check_block(char *cbuf, uint64_t block_id) {
    uint64_t *buf = (uint64_t *)(cbuf);
    uint64_t block_offset = block_id * BS;
    uint64_t checksum = 0;
    for (int j=0; j<BS/sizeof(uint64_t); j++) {
      if (buf[j] != block_offset + j) abort();
      checksum = checksum ^ buf[j];
    }
    return checksum;
}


#endif
