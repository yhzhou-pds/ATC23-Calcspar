import csv
import numpy as np
import pandas as pd 
sheet_name = "Monitor.log"
 
monitor = pd.read_csv("./Monitor.log",sep='\s+')
qps = pd.read_csv("./QPS.log",sep='\s+')
stat = pd.read_csv("./statistics.log",sep='\s+')

## clean index 
for index,row in qps.iterrows():
    if row['QPS'] == "QPS":
        qps = qps.drop(index)

qps=qps.reset_index(drop=True)      

for index,row in monitor.iterrows():
    if row['time'] == "time":
        monitor = monitor.drop(index)

monitor=monitor.reset_index(drop=True)

for index,row in stat.iterrows():
    if row['time'] == "time":
        stat = stat.drop(index)

stat=stat.reset_index(drop=True)
 
qps=qps.drop(['threadID'],axis=1)

qps['QPS']=qps['QPS'].apply(np.float64)
qps['time']=qps['time'].apply(np.int32)

qps=qps.groupby(by='time',as_index=False)['QPS'].sum()


fo = open("./iops_read.data", "w", encoding='utf-8')
lenindex=min(len(monitor['time']),len(qps['time']))
lenindex=min(lenindex,len(stat['time']))


print("time\tIO\tUr\tFw\tCr\tCw\tIOPS\tread\twrite\tmean\t25th\t50th\t75th\t99th\tQPS",file=fo)
i=0 
while i<lenindex:
    print(str(monitor['time'][i])+"\t",end="",file=fo)
    print(str(monitor['ALLIOPS'][i])+"\t",end="",file=fo)
    print(str(monitor['Ur'][i])+"\t",end="",file=fo)
    print(str(monitor['Fw'][i])+"\t",end="",file=fo)
    print(str(monitor['Cr'][i])+"\t",end="",file=fo)
    print(str(monitor['Cw'][i])+"\t",end="",file=fo)

    print(str(stat['IOPS'][i])+"\t",end="",file=fo)
    print(str(stat['read'][i])+"\t",end="",file=fo)
    print(str(stat['write'][i])+"\t",end="",file=fo)
    print(str(stat['mean'][i])+"\t",end="",file=fo)
    print(str(stat['25th'][i])+"\t",end="",file=fo)
    print(str(stat['50th'][i])+"\t",end="",file=fo)
    print(str(stat['75th'][i])+"\t",end="",file=fo)
    print(str(stat['99th'][i])+"\t",end="",file=fo)

    print(str(qps['QPS'][i])+"\t",end="\n",file=fo)

    i+=1
fo.close()

# print(pd_reader['time'])
# print(pd_reader['ALLIOPS'])

# print(pd_reader.loc[i])
# print("test")
# # print(pd_reader['time'].iloc[i])

# fo = open("./test.dat", "w", encoding='utf-8')
# print(pd_reader.loc[i],file=fo)
# fo.close()