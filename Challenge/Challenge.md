

## RocksDB performance on EBS-io2

Figure 6 shows our test using the db_bench tool of rocksdb (version 6.4.6), and the results are output through the command line.

First, mount the io2 storage volume.

Then, compile rocksdb
``` shell
    cd Challenge
    cd rocksdb-io 
    mkdir build && cd build
    cmake .. -DCMAKE_BUILD_TYPE=Release 
    make db_bench -j8
``` 

Finally, execute the command line for testing.

Please change the data storage path to io2 storage volume. To avoid the impact of logs, consider putting the logs in the rest of storage volumes, such as local storage volumes.

``` shell
    ## write  
    sudo ./db_bench --benchmarks="fillrandom,levelstats,stats" -perf_level=5 \
    -compression_type=none -histogram=1 --statistics \
    -threads=10 -max_background_jobs=8 -subcompactions=1 \
    -compression_type=none \
    -write_buffer_size=$((8*1024*1024)) \
    -level_compaction_dynamic_level_bytes=1 \
    -target_file_size_base=$((8*1024*1024)) \
    -key_size=16 -value_size=256 -bloom_bits=10 \
    -keys_per_prefix=0 \
    -seek_nexts=100 \
    -use_direct_io_for_flush_and_compaction=1 -use_direct_reads=1 \
    --db=path of io2 \
    -wal_dir=path of local nvme ssd or memory \
    -num=10000000

    ## Read. Because of the limited IOPS of io2 storage volumes, you need to set num smaller to shorten the test time.
    sudo ./db_bench --benchmarks="readrandom,levelstats,stats" -perf_level=5 \
    -compression_type=none -histogram=1 --statistics \
    -threads=10 -max_background_jobs=8 -subcompactions=1 \
    -write_buffer_size=$((8*1024*1024)) \
    -level_compaction_dynamic_level_bytes=1 \
    -target_file_size_base=$((8*1024*1024)) \
    -key_size=16 -value_size=256 -bloom_bits=10 \
    -keys_per_prefix=0 \
    -seek_nexts=100 \
    -use_direct_io_for_flush_and_compaction=1 -use_direct_reads=1 \
    --db=path of io2 \
    -wal_dir=path of local nvme ssd or memory \
    -use_direct_reads=1 \
    -num=100000
```

The read and write throughput (IOPS) is output when the execution is completed


## Challenge #1 #3 #4:

We added information statistics inside the RocksDB code to get information about IOPS, average latency and corresponding different latency of RocksDB read requests within each second.

First, compile rocksdb
``` shell 
    # If you have already compiled db_bench using our rocksdb, you can skip the first four steps
    cd Challenge
    cd rocksdb-io  
    mkdir build && cd build
    cmake .. -DCMAKE_BUILD_TYPE=Release 
    make rocksdb -j8
``` 

Then, testing with ycsb with integrated mixgraph workload features.

```shell
    cd Challenge/YCSB-C
    # Modify the path of rocksdb in the Makefile file
    # ROCKSDB_INCLUDE=/home/ubuntu/zyh/problem/rocksdb-io/include
    # ROCKSDB_LIBRARY=/home/ubuntu/zyh/problem/rocksdb-io/build/librocksdb.a
    # ROCKSDB_LIB=/home/ubuntu/zyh/problem/rocksdb-io/build
    make all
    # Note, please modify the data path
    sudo ./test7.sh
```

Three log files will be obtained after the execution is completed, namely Monitor.log (logging rocksdb internal IO), QPS.log (logging workload QPS) and statistics.log (logging request latency).

You can use the script *dataclean1.py* to process these files to generate the drawing data. Use the source code in the figure folder for drawing.

Figure 10 shows the impact of write, we used half read and half write, if you do not see the impact in the short term, you can try to run a little longer, or adjust the ratio of read and write (Note: to ensure that the average value of IOPS read operations as far as possible equal to paid IOPS)

## Challenge #2:

We monitor to obtain read IO information for each layer based on the information related to the read file. 

Here the Bloom filter is set to 10bit. 
If the Bloom filter is turned off, you can see more severe read amplification.


## Challenge #5:

The detailed information inside rocksdb is not needed for the performance and cost challenges, so it can be tested directly using the mixgraph tool.

Use the same script below to run on a different configuration of io2.

``` shell
    ## write  
    sudo ./db_bench --benchmarks="fillrandom,levelstats,stats" -perf_level=5 \
    -compression_type=none -histogram=1 --statistics \
    -threads=10 -max_background_jobs=8 -subcompactions=1 \
    -compression_type=none \
    -write_buffer_size=$((8*1024*1024)) \
    -level_compaction_dynamic_level_bytes=1 \
    -target_file_size_base=$((8*1024*1024)) \
    -key_size=16 -value_size=256 -bloom_bits=10 \
    -keys_per_prefix=0 \
    -seek_nexts=100 \
    -use_direct_io_for_flush_and_compaction=1 -use_direct_reads=1 \
    --db=path of io2 \
    -wal_dir=path of local nvme ssd or memory \
    -num=10000000

    ## Read. Because of the limited IOPS of io2 storage volumes, you need to set num smaller to shorten the test time.
sudo ./db_bench --benchmarks="mixgraph,levelstats,stats" \
    -use_direct_io_for_flush_and_compaction=true \
    -use_direct_reads=true \
    -threads=10 \
    -write_buffer_size=$((8*1024*1024)) \
    -max_background_flushes=4 \
    -max_background_compactions=4 -subcompactions=1 \
    -histogram=1 --statistics \
    -compression_type=none \
    -key_size=16 -value_size=256 \
    -key_dist_a=0.002312 -key_dist_b=0.3467 \
    -keyrange_dist_a=5.18 \
    -keyrange_dist_b=-2.917 \
    -keyrange_dist_c=0.0164 \
    -keyrange_dist_d=-0.08082 \
    -keyrange_num=30 \
    -mix_get_ratio=1 -mix_put_ratio=0 -mix_seek_ratio=0 \
    -sine_mix_rate_interval_milliseconds=50 \
    -sine_a=500 -sine_b=0.035 -sine_c=4.17 -sine_d=1000 \
    –perf_level=2 -sine_mix_rate_noise=0.3 \
    -reads=3000000 -num=10000000 \
    --report_interval_seconds=1 \
    -report_file="./report.log" \
    -stats_interval_seconds=1 \
    -bloom_bits=10 \
    -target_file_size_base=$((8*1024*1024)) \
    -sine_mix_rate=true \
    --db=path of io2 \
    -wal_dir=path of local nvme ssd or memory \
    -use_existing_db=true   
```