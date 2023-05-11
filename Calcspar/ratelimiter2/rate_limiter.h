#pragma once

#include "sequence.h"
#include "spinlock.h"

#include <assert.h>
#include <mutex>

#define NS_PER_SECOND 1000000000//一秒的纳秒数
#define NS_PER_USECOND 1000//一微秒的纳秒数

class RateLimiter2 
{
public:
    //qps限制最大为十亿
    RateLimiter2(int64_t qps);

    DISALLOW_COPY_MOVE_AND_ASSIGN(RateLimiter2);

    //对外接口，能返回说明流量在限定值内
    void pass();

    void SetQps(int64_t qps);
    int getLeft();

private:

    //获得当前时间，单位ns
    int64_t now();

    //更新令牌桶中的令牌
    void supplyTokens();

    //尝试获得令牌
    //成功获得则返回true
    //失败则返回false
    bool tryGetToken();

    //必定成功获得令牌
    //其中会进行重试操作
    void mustGetToken();

    //令牌桶大小
    const int64_t bucketSize_;
    
    //剩下的token数
    AtomicSequence tokenLeft_;

    //补充令牌的单位时间
    int64_t supplyUnitTime_;

    //上次补充令牌的时间，单位纳秒
    int64_t lastAddTokenTime_;

    //自旋锁
    Spinlock lock_;

    std::mutex lockTime; // 保护counter


    int qps_now;
    AtomicSequence left;
};