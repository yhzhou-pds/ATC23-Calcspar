#include "zyh/monitor.h"
#include "map"
#include "logging/event_logger.h"
#include "util/util.h"
#include <vector>
#include <unistd.h>

using namespace std;

namespace rocksdb {

Monitor::Monitor() {}

Monitor& Monitor::_GetInst(){
  static Monitor i;
  return i;
}

void Monitor::Init(){
  static Monitor& i = _GetInst();
  i._Init();
}

void Monitor::_Init() {
    log_ = fopen("./Monitor.log","a+");
    if(log_==NULL) {
      printf("open log file error\n");
      exit(1);
    }

    fprintf(log_, "time ALLIOPS   Ur   Fw    Cr   Cw\n");

    io_lock_.lock();
    for(int i=0;i<5;i++)
      io_.push_back(0);
    io_lock_.unlock();

    print_io_stop = false;
    print_io_ = new thread(bind(&rocksdb::Monitor::_print, this));
}


void Monitor::_print(){
  int t=0;
  while(!print_io_stop) {
    sleep(1);
    io_lock_.lock();
      fprintf(log_,"%d  ",t);
      for(int i=0;i<5;i++){
        fprintf(log_,"%d  ",io_[i]);
        io_[i]=0;
      }
      fprintf(log_,"  \n");
      fflush(log_);
    io_lock_.unlock();
    t++;
  }
}

void Monitor::CollectIO(int type, int num){
    static Monitor& i = _GetInst();
    i._CollectIO(type,num);
}

void Monitor::_CollectIO(int type, int num){
  io_lock_.lock();
  io_[0] += num;
  io_[type] += num;
  io_lock_.unlock();
}

void Monitor::Shutdown(){
  static Monitor& i = _GetInst();
  i._Shutdown();
}

void Monitor::_Shutdown() {
  printf("Monitor shutdown\n");
  print_io_stop = true;
  if(print_io_){
    print_io_->join();
    delete print_io_;
    print_io_ = nullptr;
  }
  fclose(log_);

}

}