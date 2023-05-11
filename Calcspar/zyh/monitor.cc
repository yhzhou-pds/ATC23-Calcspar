#include "zyh/monitor.h"

#include <unistd.h>

#include <vector>

#include "logging/event_logger.h"
#include "map"
#include "util/util.h"

using namespace std;

namespace rocksdb {

Monitor::Monitor() {}

Monitor& Monitor::_GetInst() {
  static Monitor i;
  return i;
}

void Monitor::Init() {
  static Monitor& i = _GetInst();
  i._Init();
}

int Monitor::GetHighUsed() {
  static Monitor& i = _GetInst();
  return i.left;
}


int Monitor::GetAll() {
  static Monitor& i = _GetInst();
  return i.all;
}
void Monitor::_Init() {
  if(inited)
  {
    return;
  }
  inited=true;
  log_ = fopen("./Monitor.log", "a+");
  if (log_ == NULL) {
    printf("open log file error\n");
    exit(1);
  }

  fprintf(log_, "time ALLIOPS   Ur   Fw    Cr   Cw   Fr  Prefetch\n");

  io_lock_.lock();
  for (int i = 0; i < 7; i++) io_.push_back(0);
  io_lock_.unlock();

  print_io_stop = false;
  print_io_ = new thread(bind(&rocksdb::Monitor::_print, this));
}

void Monitor::_print() {
  int t = 0;
  while (!print_io_stop) {
    sleep(1);
    io_lock_.lock();
    left = io_[1];
    all=io_[0];
    fprintf(log_, "%d  ", t);
    for (int i = 0; i < 7; i++) {
      fprintf(log_, "%d  ", io_[i]);
      io_[i] = 0;
    }
    fprintf(log_, "  \n");
    fflush(log_);
    t++;
    io_lock_.unlock();
  }
}

void Monitor::CollectIO(int type, int num) {
  static Monitor& i = _GetInst();
  i._CollectIO(type, num);
}

void Monitor::_CollectIO(int type, int num) {
  io_lock_.lock();
  io_[0] += num;
  io_[type] += num;
  io_lock_.unlock();
}

void Monitor::Shutdown() {
  static Monitor& i = _GetInst();
  i._Shutdown();
}

void Monitor::_Shutdown() {
  printf("Monitor shutdown\n");
  print_io_stop = true;
  if (print_io_) {
    print_io_->join();
    delete print_io_;
    print_io_ = nullptr;
  }
  fclose(log_);
}

}  // namespace rocksdb