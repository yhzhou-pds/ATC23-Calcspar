#pragma once

#include <vector>
#include <map>
#include <assert.h>
#include <stdlib.h>
#include <mutex>
#include <thread>

namespace rocksdb {

class Monitor {    
    bool inited=false;  
// 记录不同的IO
    FILE* log_;

    
    std::mutex io_lock_;

    // 获取静态实例
    static Monitor& _GetInst();    
    
    // 初始化
    void _Init();
    
    // 收集IO
    void _CollectIO(int type, int num = 1);

    std::thread* print_io_;  // 线程定时输出io次数
    bool print_io_stop;
    void _print();

    // 关闭
    void _Shutdown(); 

public: 
std::vector<int> io_;
    Monitor();
    // 初始化
    static void Init();
    // 收集IO
    static void CollectIO(int type, int num = 1);
    static void Shutdown();  
    static int GetHighUsed();  
    static int GetAll();  
    int left=0;   
    int all=0;

};

}