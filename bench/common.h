#ifndef COMMON_H
#define COMMON_H

#define BLOCK_SIZE 4096

int create_data_file(std::string filename, uint64_t size) {
  uint64_t buf[BLOCK_SIZE/sizeof(uint64_t)];
  int fd = open(filename.c_str(), O_WRONLY | O_CREAT | O_TRUNC,  0644);
  for (uint64_t i=0; i < size; i+=BLOCK_SIZE) {
    for (int j=0; j<BLOCK_SIZE/sizeof(uint64_t); j++) {
      buf[j] = i*BLOCK_SIZE + j;
    }
    write(fd, (char *)buf, BLOCK_SIZE);
  }
  close(fd);
  return 0;
}

void check_block(char *cbuf, uint64_t block_id) {
    uint64_t *buf = (uint64_t *)(cbuf);
    for (int j=0; j<BLOCK_SIZE/sizeof(uint64_t); j++) {
      if (buf[j] != block_id*BLOCK_SIZE + j) abort();
    }
}

std::string getWorkerDataFileName(int i) {
  return "test." + std::to_string(i);
}


#endif
