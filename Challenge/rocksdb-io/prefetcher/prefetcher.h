#pragma once
#include <assert.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <map>
#include <set>
#include <thread>
#include <unordered_map>
#include <cstring>

#include <hdr/hdr_histogram.h>

#include "db/db_impl/db_impl.h"
#include "db/event_helpers.h"
#include "db/version_edit.h"
#include "logging/event_logger.h"
#include "rocksdb/options.h"
#include "table/block_based/block_based_table_reader.h"
#include "util/mutexlock.h"

#define NS_PER_SECOND 1000000000  //一秒的纳秒数
#define NS_PER_USECOND 1000       //一微秒的纳秒数
#define BUF_SIZE 1024 * 1024

namespace rocksdb {

class SstTemp {
 public:
  uint64_t sst_id_blk;
  uint32_t get_times;  //访问次数
  SstTemp(uint64_t sst_id_blk_) {
    sst_id_blk = sst_id_blk_;
    get_times = 1;
  }

  SstTemp(uint64_t sst_id_blk_, uint32_t get_times_) {
    sst_id_blk = sst_id_blk_;
    get_times = get_times_;
  }
  ~SstTemp()
  {
  }
};

typedef std::pair<uint64_t, SstTemp*> PAIR;
struct CmpByValue {
  bool operator()(const PAIR& lhs, const PAIR& rhs) {
    if (lhs.second == nullptr && rhs.second == nullptr) {
      return true;
    } else if (lhs.second == nullptr) {
      return true;
    } else if (rhs.second == nullptr) {
      return false;
    }
    return lhs.second->get_times < rhs.second->get_times;
  }
};

class SstManager {
 public:
  std::unordered_map<uint64_t, SstTemp*> sstMap;
  
  std::vector<PAIR> sortedV;
  bool isSorted = false;
  void sortSst() {
    if (isSorted) {
      return;
    }
    sortedV.clear();
    sortedV.insert(sortedV.begin(), sstMap.begin(), sstMap.end());
    sort(sortedV.begin(), sortedV.end(), CmpByValue());
  }
  uint64_t getMax() {
    uint64_t key = 0;
    uint32_t num = 0;
    for (auto it = sstMap.begin(); it != sstMap.end(); it++) {
      if (it->second->get_times > num || num == 0) {
        num = it->second->get_times;
        key = it->first;
      }
    }
    return key;
  }
  uint64_t getMin() {
    uint64_t key = 0;
    uint32_t num = UINT32_MAX;
    for (auto it = sstMap.begin(); it != sstMap.end(); it++) {
      if (it->second->get_times < num) {
        num = it->second->get_times;
        key = it->first;
      }
    }
    return key;
  }
};

class Prefetcher {
 public:
  uint64_t hit_times=0;
  uint64_t all_times=0;
  std::unordered_map<uint64_t, char*> sst_blocks;
  std::vector<char*> mems;

  static Prefetcher& _GetInst();
  char* buf_ = nullptr;
  bool inited = false;

  bool logRWlat=true;

  static void Init();
  void _Init();
  static void Init2();
  void _Init2();
  static int64_t now();

  struct hdr_histogram *hdr_last_1s_read = NULL;
  struct hdr_histogram *hdr_last_1s_write = NULL;
  struct hdr_histogram *hdr_last_1s_size = NULL;
  FILE *logFp_read = nullptr;
  FILE *logFp_write = nullptr;
  FILE *logFp_size = nullptr;
  int readiops = 0;
  int writeiops = 0;
  uint64_t tiktoks = 0;
  uint64_t tiktok_start = 0;
  static void RecordTime(int op, uint64_t tx_xtime,size_t size);
  void _RecordTime(int op, uint64_t tx_xtime,size_t size);
  void latency_hiccup_read(uint64_t iops);
  void latency_hiccup_write(uint64_t iops);
  void latency_hiccup_size();

  ~Prefetcher() {
    fprintf(stderr,"prefetcher hit times: %lu    all times: %lu\n",hit_times,all_times);
    if(logFp_read!=nullptr)
    {
      fprintf(logFp_size,"prefetcher hit times: %lu    all times: %lu\n",hit_times,all_times);
      fclose(logFp_read);
      fclose(logFp_write);
      fclose(logFp_size);

      free(hdr_last_1s_read);
      free(hdr_last_1s_write);
      free(hdr_last_1s_size);
    }
    
    if (buf_ != nullptr) {
      free(buf_);
      buf_ = nullptr;
    }
    fprintf(stderr, "~Prefetcher\n");
  }

  const size_t MAXSSTNUM = 20*1036;  // ssd中缓存的sst_blk的最大数目

  Env* env_ = nullptr;
  mutable port::Mutex lock_;        // synchronization primitive
  mutable port::Mutex lock_sst_io;  // synchronization primitive


  mutable port::Mutex lock_rw;        // synchronization primitive

  mutable port::Mutex lock_mem;        // synchronization primitive



  std::unordered_map<uint64_t, int>
      sst_iotimes;  //统计一秒内的sst块(256k)的io次数 key : sstidk
                    //(后4位k为第几个256k块 从0开始)

  SstManager cloudManager;
  SstManager ssdManager;

  static void SstRead(uint64_t sst_id, uint64_t offset, size_t size,
                      bool isGp2);  //更新sst的读写次数(热度)
  void _SstRead(uint64_t sst_id, uint64_t offset, size_t size, bool isGp2);
  static void CaluateSstHeat();
  void _CaluateSstHeat();
  static void Prefetche();
  void _Prefetcher();

  void _PrefetcherToMem();

  static size_t TryGetFromPrefetcher(uint64_t sst_id, uint64_t offset, size_t n,
                                     char* scratch);
  size_t _TryGetFromPrefetcher(uint64_t sst_id, uint64_t offset, size_t n,
                               char* scratch);

  size_t _PrefetcherOneFile(uint64_t key, uint64_t offset, size_t n,
                            char* scratch);
  size_t _PrefetcherTwoFiles(uint64_t key, uint64_t offset, size_t n,
                             char* scratch);


  size_t _PrefetcherFromMem(uint64_t key, uint64_t offset, size_t n,
                            char* scratch);
};
}  // namespace rocksdb