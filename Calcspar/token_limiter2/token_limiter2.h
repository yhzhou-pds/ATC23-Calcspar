#pragma once

#include <cstdint>
#include <deque>
#include <memory>
#include <queue>
#include <random>
#include <ratio>

#include "port/port.h"
#include "port/port_posix.h"
#include "ratelimiter2/rate_limiter.h"
#include "rocksdb/env.h"

namespace rocksdb {

class TokenLimiter2 {
 public:
  enum IOType {
    kRead,
    kWrite,
  };
  static void SetDefaultInstance(std::unique_ptr<TokenLimiter2> limiter);
  static void RequestDefaultToken(Env::IOSource io_src, IOType io_type,
                                  int32_t n = 1);
  TokenLimiter2(int high, int middle, int low);

 private:
  RateLimiter2 h, m, l;
  void RequestToken(Env::IOSource io_src, IOType io_type, int32_t n = 1);

  int I_middle=200; //middle IOPS
  int I_low=100;
  int I_high=700;

  int64_t lastTime;
  int R_1=0; //前一秒到middle时间片时所剩余令牌数
  int R_2=0; //前2秒到middle时间片时所剩余令牌数

  int value=0;
};

}  // namespace rocksdb
