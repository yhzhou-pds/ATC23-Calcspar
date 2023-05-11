# README For Calcspar #

### Cite our Calcspar paper (ATC '23): 

>>  Calcspar: A Contract-Aware LSM-Tree for Cloud Storage with Low Latency Spikes

**The preprint of the paper can be found [here](https://github.com/yhzhou-pds/paper/blob/main/atc23-paper580.pdf).**

## What is this repo about? ##
This repo open-sources our approach for Cloud Storage and evaluations (mainly some scripts). It is a full-fledged open-source version of Calcspar design.

Calcspar analyzes the impact of cloud block storage on LSM-Tree key-value storage system and proposes an optimization scheme.

Calcspar consists of three parts: the first is the testing and analysis of cloud block storage latency, the second is the analysis of the impact of cloud block storage latency on LSM-Tree key-value storage system, and the third is the Calcspar scheme and its implementation.

### Note ###
Please read all the README.md file and Challenge.md file first.

Contents \
    |====README.md\
    |\
    |====Modeling(Section 2 experiments)\
    |&emsp;&emsp;|\
    |&emsp;&emsp;|----README.md(Experiment script description and instruction)\
    |&emsp;&emsp;|----experiment1.sh\
    |&emsp;&emsp;|----experiment2.sh\
    |&emsp;&emsp;|----experiment3\
    |&emsp;&emsp;|----experiment4.sh\
    |\
    |====Challenge(Section 3 experiments)\
    |&emsp;&emsp;|\
    |&emsp;&emsp;|----Challenge.md(Experiment script description and instruction)\
    |&emsp;&emsp;|----YCSB-C (benchmark tool)\
    |&emsp;&emsp;|----rocksdb-io \
    |\
    |====Calcspar(Section 4 and 5)\
    |&emsp;&emsp;|\
    |&emsp;&emsp;|-----README.md (Brief code description and explanation of evaluation commands)\
    |&emsp;&emsp;|-----Source Code\
    |__________________
    

### Cloud Environment Configuration ###
AWS EC2: m5d.2xlarge, ap-northeast, (root volume: 30GB 100IOPS gp2)

## Modeling Cloud Storage Performance

To unwrap the hidden latency characteristics and understand
how the above contract model would affect the performance
of an LSM store, we first perform a series of experiments on
cloud storage volumes, then proposing a performance model.

In this repo, the four experiments are done incrementally, mainly through several scripts, examining and run experimentX.sh in the Modeling folder. 
Different types of EBS stores are also mounted for the experiments, and the specific EBS storage volumes that need to be configured for the experiments are described in the paper.

We also performed the same tests on others cloud storage volumes such as AliCloud, and achieved similar results.


## Modeling RocksDB Performance ##

This repo we implemented analyzes the unfriendliness of the cloud storage contract to IOPS and latency-sensitive tasks. 

Several challenges encountered when optimizing RocksDB read performance in cloud storage are highlighted in detail (which we verified with experiments). 

We fuse Facebook's latest benchmark Mixgraph into the ycsb-c testing tool, implementing a workload intensity similar to that of positive gen fluctuations and adding some informative statistical code to better sense where the problems lie.

## Calcspar ##

This repo contains the more mature Calcspar in general. the details of the tests can be found in the README under the folder.

## figure ##
The figure folder contains our test data and python drawing code.
