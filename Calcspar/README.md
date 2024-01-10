## Calcspar: A Contract-Aware LSM-Tree for Cloud Storage with Low Latency Spikes
Calcspar is built as an extension of RocksDB https://rocksdb.org/

Important files for Calcspar implementation:

token_limiter.cc

prefetcher.cc

monitor.cc

Parameters need to be set before running:
    
    the IOPS of device: SetDefaultInstance in db_impl_open.cc
    the  total size of prefetcher and blkcache: CacheSize in prefetcher.cc

## build

1、Make sure HdrHistogram_c is installed first before running the script.

```
    git clone https://gitee.com/will_2333/HdrHistogram_c.git
    cd HdrHistogram_c
    mkdir build
    cd build
    cmake ..
    make
    sudo make install
```

2、Then configure the relevant parameters.

```
// Initialization and parameter setting can be done within the following functions (configured by default)
db/db_impl/db_impl_open.cc: #L1335 
    Status DBImpl::Open(const DBOptions& db_options, const std::string& dbname,
                    const std::vector<ColumnFamilyDescriptor>& column_families,
                    std::vector<ColumnFamilyHandle*>* handles, DB** dbptr,
                    const bool seq_per_batch, const bool batch_per_txn)

// Turn on heat monitoring and message monitoring
    Monitor::Init();

// The second parameter is true to enable prefetching
    Prefetcher::Init(impl,true,impl->immutable_db_options_.db_paths); 

// paid iops of volunme must be set
    TokenLimiter::SetDefaultInstance(
        std::unique_ptr<TokenLimiter>(new TokenLimiter(paid iops))); 

// Part of the logging information is turned on:
//  Calcspar\Calcspar\prefetcher\prefetcher.cc in class Prefetcher logRWlat set to true (off by default)

Calcspar/prefetcher/prefetcher.cc#L485

    // cache hit_ratio 
    tempLog = fopen("./hit_ratio.log", "a+");
    // read latency info
    logFp_read = std::fopen("./ssd_rlat.log", "w+");
    // write latency info
    logFp_write = std::fopen("./ssd_wlat.log", "w+");
    // read IO size
    logFp_size = std::fopen("./ssd_size.log", "w+");
    // Number of prefetches per second (for debugging)
    logFp_prefetch_times = std::fopen("./prefetch_times.log", "w+");
    // Time window information per second limiter to different priority levels
    logFp_limiter_time = std::fopen("./limite_times.log", "w+");

```

3、Build db_bench and run

```
build: 
    cd build
    make db_bench -j8

run:  
    load:
    sudo ./db_bench --benchmarks="fillseq,levelstats,stats" –perf_level=3 \
    -max_background_jobs=8 -subcompactions=1 \
    -use_direct_io_for_flush_and_compaction=true \
    -use_direct_reads=true -cache_size=268435456 \
    -key_size=16 -value_size=256 -num=100000000 \
    -bloom_bits=10 \
    -compression_type=none \
    -write_buffer_size=$((8*1024*1024)) \
    -target_file_size_base=$((8*1024*1024)) \
    -db=/home/ubuntu/data (io2 path)

    mixgraph workload:
 sudo ./db_bench --benchmarks="mixgraph,levelstats,stats" \
    -use_direct_io_for_flush_and_compaction=true \
    -use_direct_reads=true \
    -threads=10 \
    -max_background_flushes=4 \
    -max_background_compactions=4 -subcompactions=4 \
    -histogram=1 --statistics \
    -key_size=16 -value_size=256 \
    -cache_size=$((500*1024*1024)) \
    -key_dist_a=0.002312 -key_dist_b=0.3467 \
    -keyrange_dist_a=5.18 \
    -keyrange_dist_b=-2.917 \
    -keyrange_dist_c=0.0164 \
    -keyrange_dist_d=-0.08082 \
    -keyrange_num=30 \
    -mix_get_ratio=0.05 -mix_put_ratio=0.95 -mix_seek_ratio=0 \
    -sine_mix_rate_interval_milliseconds=50 \
    -sine_a=12000 -sine_b=0.035 -sine_c=4.17 -sine_d=32000 \
    –perf_level=2 -sine_mix_rate_noise=0.3 \
    -reads=500000 -num=100000000 \
    --report_interval_seconds=1 \
    -report_file="./report.log" \
    -stats_interval_seconds=1 \
    -bloom_bits=10 \
    -target_file_size_base=$((8*1024*1024)) \
    -sine_mix_rate=true \
    -compression_type=none \
    -open_files=10240 \
    -db=/home/ubuntu/data (io2 path) -use_existing_db=true

```

4、Several important parameters to be used in the follow-up evaluation
```
    mixgraph workload:
    ## threads:     set thread num
    ## cache_size:  set cache size
    ## mix_get_ratio: set read ratio
    ## mix_put_ratio: set write ratio
    ## mix_seek_ratio: set seek ratio
    ## sine_a/sine_b: set workload intensity

    Others you can find rocksdb's wiki (https://github.com/facebook/rocksdb/wiki/Benchmarking-tools).
```

5、Output

Dbbench outputs logs after running, which can be compared with the relevant data in figure.

The benchmark for our mixgraph workload is sine_a=(paid IOPS)/2 and sine_d=paid IOPS.
When cache is turned on, since cache will absorb more read requests, it can be raised to sine_a and sine_d to observe the better performance of calcspar. 
Note, however, that it is important to ensure that the same parameters are used for all comparison scenarios.

## Evaluation ## 
### Overall Performance ###

Mixgraph workloads are evaluated, using the above command line.

figure14:

Parameters configuration:
~~~
    100r：
        -sine_a=500 -sine_b=0.035 -sine_c=4.17 -sine_d=1200 \
    80r20w：
        -sine_a=725 -sine_b=0.035 -sine_c=4.17 -sine_d=1600
    60r40w：
        -sine_a=800 -sine_b=0.035 -sine_c=4.17 -sine_d=2000 \
    40r 60w：
        -sine_a=1350 -sine_b=0.035 -sine_c=4.17 -sine_d=3000 \
    20r 80w：
        -sine_a=2400 -sine_b=0.035 -sine_c=4.17 -sine_d=6000 \
    5r  95w:
        -sine_a=8000 -sine_b=0.035 -sine_c=4.17 -sine_d=24000 
~~~

figure15/16/17: 
YCSB evaluation using YCSB-C in folder: ../Challenge/YCSB-C.

~~~
    # run workloada.spec:
    ./testycsb.sh a
~~~

Determine the workload type by changing the parameters in workloadx.spec.
Adjust the intensity of the workload by changing sine_a and sine_d.
Since there is an effect of cache itself, it is possible to approximate the optimal effect by increasing sine_a and sine_d. Calcspar has the best effect space.


### Congestion Mitigation Effectiveness ###

figure18:
The parameter of threads in Mixgraph workload runs command line to determine the user threads, just modify it.

figure19:
Turn on monitoring, prefetching and congestion control and IOPS stabilizer at *Calcspar/db/db_impl/db_impl_open.cc#L1335*  

IOPS initial trial assignment and time window initial values are set at Calcspar/util/token_limiter.cc#L93

- NA: Each queue window opens at 0 and has paid IOPS tokens, but only paid IOPS tokens can be used per second.

- SA: Each queue window opens at 0 and has a fixed number of tokens(6:3:1).

- DA: Each queue window opens at 0:00 with a fixed number of tokens (6:3:1). Tokens will be redistributed at the end of each second based on usage.

- TWA: The initial number of tokens is 6:3:1, and the allocation is updated every second. The time window start moment is determined according to the number of tokens.

### Cache ###

Mixgraph modifies the cache size by modifying the cache_size parameter.
YCSB modifies the cache size by modifying the cachesize parameter in the db/rocksdb.cc/setoption() function.

The test script has not changed much.

### End ###
The remaining evaluation is sufficient to change the corresponding parameters. The description will not be continued here.
