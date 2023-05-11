#include "token_limiter2/token_limiter2.h"

#include <algorithm>
#include <cassert>
#include <cstddef>
#include <cstdint>
#include <deque>
#include <iostream>
#include <memory>
#include <random>
#include <ratio>

#include "prefetcher/prefetcher.h"
#include "util/mutexlock.h"
#include "zyh/monitor.h"

namespace rocksdb {

static std::unique_ptr<TokenLimiter2> default_limiter = nullptr;

int64_t now() {
  struct timeval tv;
  ::gettimeofday(&tv, 0);
  int64_t seconds = tv.tv_sec;
  return seconds * NS_PER_SECOND + tv.tv_usec * NS_PER_USECOND;
}

// static----------------------------------------------------------------------
void TokenLimiter2::SetDefaultInstance(std::unique_ptr<TokenLimiter2> limiter) {
  if (default_limiter != nullptr) {
    return;
  }
  assert(default_limiter == nullptr && limiter != nullptr);
  default_limiter = std::move(limiter);
}
void TokenLimiter2::RequestDefaultToken(Env::IOSource io_src, IOType io_type,
                                        int32_t n) {
  if (default_limiter != nullptr) {
    default_limiter->RequestToken(io_src, io_type, n);
  }
}

// ----------------------------------------------------------------------------

TokenLimiter2::TokenLimiter2(int high, int middle, int low)
    : h(high), m(middle), l(low) {
  lastTime = now();
}

void TokenLimiter2::RequestToken(Env::IOSource io_src, IOType io_type,
                                 int32_t n) {
  assert(io_src >= Env::IOSource::IO_SRC_PREFETCH &&
         io_src <= Env::IOSource::IO_SRC_DEFAULT);
  if (io_src == Env::IOSource::IO_SRC_PREFETCH) {
    for (int i = 0; i < n; i++) {
      l.pass();
    }
  } else if (io_src == Env::IOSource::IO_SRC_FLUSH_L0COMP ||
             io_src == Env::IOSource::IO_SRC_USER) {
    for (int i = 0; i < n; i++) {
      h.pass();
    }
  } else if (io_src == Env::IOSource::IO_SRC_COMPACTION) {
    for (int i = 0; i < n; i++) {
      m.pass();
    }
  }
  int64_t cur = now();
  if (cur - lastTime >= NS_PER_SECOND) {
    R_2 = R_1;
    R_1 = Monitor::GetHighUsed();
    int t=R_2-R_1;
    if(I_high-R_1>100)
    {
        t+=20;
    }
    else if(I_high-R_1<50)
    {
        t-=10;
    }
    
    I_middle = std::max((double)0, I_middle + 0.7 * t);
    I_low = std::max((double)0, I_low + 0.3 * t);
    I_middle = std::max(50, I_middle);
    I_middle=std::min(400,I_middle);
    I_low=std::max(10, I_low);
    I_low=std::min(100,I_low);
    I_high=1000-I_middle-I_low;
    l.SetQps(I_low);
    m.SetQps(I_middle);
    h.SetQps(I_high);
    lastTime=cur;
    Prefetcher::RecordLimiterTime(0, 0, 0, I_low, I_middle, I_high,R_2, R_1);
  }
}

}  // namespace rocksdb