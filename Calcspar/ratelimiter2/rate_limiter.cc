#include "rate_limiter.h"
#include "spinlock_guard.h"

#include <sys/time.h>
#include <float.h>
#include <unistd.h>

#define RETRY_IMMEDIATELY_TIMES 100



RateLimiter2::RateLimiter2(int64_t qps) : 
    bucketSize_(1000), tokenLeft_(0), supplyUnitTime_(NS_PER_SECOND / qps), lastAddTokenTime_(0)
{ 
    assert(qps <= NS_PER_SECOND);
	assert(qps >= 0);
    lastAddTokenTime_ = now();
	qps_now=qps;
}

int64_t RateLimiter2::now()
{
	struct timeval tv;
	::gettimeofday(&tv, 0);
	int64_t seconds = tv.tv_sec;
	return seconds * NS_PER_SECOND + tv.tv_usec * NS_PER_USECOND;
}


void RateLimiter2::pass()
{
	return mustGetToken();
}


bool RateLimiter2::tryGetToken()
{
    supplyTokens();


	auto token = tokenLeft_.fetch_add(-1);
	if(token <= 0)
	{
		tokenLeft_.fetch_add(1);
		return false;
	}
	
    return true;
}


void RateLimiter2::mustGetToken()
{
	bool isGetToken = false;
	for(int i = 0; i < RETRY_IMMEDIATELY_TIMES; ++i)
	{
		isGetToken =  tryGetToken();
		if(isGetToken)
		{
			return;
		}
	}

	while(1)
	{
		isGetToken =  tryGetToken();
		if(isGetToken)
		{
			return;
		}
		else
		{
			sleep(0);
		}
	}
}

void RateLimiter2::SetQps(int64_t qps)
{
    supplyUnitTime_= NS_PER_SECOND / qps;
    assert(qps <= NS_PER_SECOND);
	assert(qps >= 0);
    lastAddTokenTime_ = now();
	qps_now=qps;
	tokenLeft_.store(qps);
}

int RateLimiter2::getLeft()
{
	return left.load();
}

void RateLimiter2::supplyTokens()
{
	auto cur = now();
	if (cur - lastAddTokenTime_ < NS_PER_SECOND)
	{
		return;
	}

	{
		SpinlockGuard lock(lock_);

		int64_t pastTime= cur - lastAddTokenTime_;
		if(pastTime<NS_PER_SECOND)
		{
			return;
		}
		lastAddTokenTime_=cur;
		left.store(tokenLeft_.load());
		tokenLeft_.store(qps_now);
	}
}

