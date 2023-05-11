#pragma once
#include <assert.h>
#include <fcntl.h>
#include <hdr/hdr_histogram.h>
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
#include <list>
#include <map>
#include <set>
#include <thread>
#include <unordered_map>

#include "db/db_impl/db_impl.h"
#include "db/event_helpers.h"
#include "db/version_edit.h"
#include "logging/event_logger.h"
#include "rocksdb/options.h"
#include "table/block_based/block_based_table_reader.h"
#include "util/mutexlock.h"

#define NS_PER_SECOND 1000000000
#define NS_PER_USECOND 1000
#define BUF_SIZE 1024 * 1024

namespace rocksdb {

class SstTemp {
 public:
  uint64_t sst_id_blk;
  double get_times;
  SstTemp(uint64_t sst_id_blk_) {
    sst_id_blk = sst_id_blk_;
    get_times = 1;
  }

  SstTemp(uint64_t sst_id_blk_, double get_times_) {
    sst_id_blk = sst_id_blk_;
    get_times = get_times_;
  }
  ~SstTemp() {}
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
  int maxIndex = 0;
  int minIndex = 0;
  void sortSst() {
    sortedV.clear();
    sortedV.insert(sortedV.begin(), sstMap.begin(), sstMap.end());
    sort(sortedV.begin(), sortedV.end(), CmpByValue());
    maxIndex = sortedV.size() - 1;
    minIndex = 0;
  }

  uint64_t getMax() {
    uint64_t key = 0;
    double num = 0;
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
    double num = UINT32_MAX;
    for (auto it = sstMap.begin(); it != sstMap.end(); it++) {
      if (it->second->get_times < num) {
        num = it->second->get_times;
        key = it->first;
      }
    }
    return key;
  }
};

#define IOPS_MAX 1000

class Prefetcher {
 public:
  int calcuTimes = 0;
  BlockBasedTableOptions* options_ = nullptr;

  DBImpl* impl_;
  bool paused = false;
  std::list<int> lastIOPS;
  uint64_t hit_times = 0;
  uint64_t all_times = 0;

  uint64_t all_prefetch_hit_times = 0;
  uint64_t all_prefetch_all_times = 0;
  uint64_t all_blkcache_all_times = 0;
  uint64_t all_blkcache_hit_times = 0;

  uint64_t prefetch_times = 0;

  uint64_t blkcache_insert_times = 0;

  uint64_t blkcache_all_times = 0;
  uint64_t blkcache_hit_times = 0;
  std::unordered_map<uint64_t, char*> sst_blocks;

  static Prefetcher& _GetInst();
  char* buf_ = nullptr;
  bool inited = false;

  bool logRWlat = false;

  static void Init(DBImpl* impl, bool doPrefetch_,std::vector<DbPath> paths_);
  void _Init(DBImpl* impl, bool doPrefetch_);
  static void SetOptions(BlockBasedTableOptions* options);
  static int64_t now();

  struct hdr_histogram* hdr_last_1s_read = NULL;
  struct hdr_histogram* hdr_last_1s_write = NULL;
  struct hdr_histogram* hdr_last_1s_size = NULL;
  FILE* logFp_read = nullptr;
  FILE* logFp_write = nullptr;
  FILE* logFp_size = nullptr;
  FILE* logFp_prefetch_times = nullptr;
  FILE* logFp_limiter_time = nullptr;

  FILE* tempLog = nullptr;

  uint64_t limiter_star_time = 0;

  int log_time = 0;
  uint64_t prefetch_start = 0;
  int t_prefetch_times = 0;

  int readiops = 0;
  int writeiops = 0;
  uint64_t tiktoks = 0;
  uint64_t tiktok_start = 0;

  static void RecordTime(int op, uint64_t tx_xtime, size_t size);
  void _RecordTime(int op, uint64_t tx_xtime, size_t size);
  void latency_hiccup_read(uint64_t iops, uint64_t alliops);
  void latency_hiccup_write(uint64_t iops);
  void latency_hiccup_size();

  void log_prefetch_times(int time, int times);

  ~Prefetcher();

  Env* env_ = nullptr;
  mutable port::Mutex lock_;
  mutable port::Mutex lock_sst_io;

  mutable port::Mutex lock_rw;

  mutable port::Mutex lock_mem;

  mutable port::Mutex lock_blkcache;
  mutable port::Mutex lock_blkcache2;

  std::unordered_map<std::string, int> blkcache_iotimes;
  std::unordered_map<std::string, double> blkcache_heat;
  double blkcacheMinHeats = 0;

  std::unordered_map<uint64_t, int> sst_iotimes;

  SstManager cloudManager;
  SstManager ssdManager;

  static void SstRead(uint64_t sst_id, uint64_t offset, size_t size,
                      bool isGp2);
  void _SstRead(uint64_t sst_id, uint64_t offset, size_t size, bool isGp2);
  static void CaluateSstHeat();
  void _CaluateSstHeat();
  static void Prefetche();

  void _PrefetcherToMem();

  static size_t TryGetFromPrefetcher(uint64_t sst_id, uint64_t offset, size_t n,
                                     char* scratch);
  size_t _TryGetFromPrefetcher(uint64_t sst_id, uint64_t offset, size_t n,
                               char* scratch);

  size_t _PrefetcherFromMem(uint64_t key, uint64_t offset, size_t n,
                            char* scratch);

  size_t _Prefetcher2BlocksFromMem(uint64_t key, uint64_t offset, size_t n,
                                   char* scratch);

  static void blkcacheInsert();
  static void blkcacheInsert(const Slice& key, uint64_t PrefetchKey);
  static void blkcacheTryGet();
  static void blkcacheGet(const Slice& key);
  std::vector<std::string> delKeys;
  static void blkcacheDelete(const Slice& key);

  static void RecordLimiterTime(uint64_t prefetch, uint64_t compaction,
                                uint64_t flush);

  static void RecordLimiterTime(uint64_t prefetch, uint64_t compaction,
                                uint64_t flush, int prefetch_iops,
                                int compaction_iops, int high, int R2, int R1);

  static bool getCompactionPaused();
};
}  // namespace rocksdb