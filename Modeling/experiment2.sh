#!/bin/bash

## $1: devices name("/dev/neme2n1")
## $2: Send IO pressure

sudo fio -name=randread -filename=$1 \
    -direct=1 -rw=randread -ioengine=psync \
    -size=100G  -time_based=1 \
    -random_generator=tausworthe \
    -group_reporting \
    -bs=4k --norandommap \
    -percentile_list=1:5:10:20:30:40:50:60:70:80:90:95:99:99.5:99.99:100 \
    -rate_iops=$2 -numjobs=10 -iodepth=1 -runtime=60