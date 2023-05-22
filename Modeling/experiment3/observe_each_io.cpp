#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <assert.h> 
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <time.h>
#include <pthread.h>
#include <atomic>
#include <fstream>
#include <vector>
#include <iostream>
#include <libaio.h>
#include <mutex>
#include <condition_variable>
#include "ConsumerProducerQueue.h"
#include <climits>

#define MAX_COUNT 65536

std::atomic<long> pointer(0);
std::vector<long> read_order;
std::vector<long> time_long;

// Note: all pos in sector unless before passed in read/write
int SECTOR_SIZE = 512;
int STRIDE_SIZE = SECTOR_SIZE * 1;      // chunk size actually
int num_ios = 20000;
int completed_ios = 0;

int D = 0;
int j = 0;
int d = 0;
int rate_iops=1000;
int fd = 0;
io_context_t ctx_;
 
std::condition_variable cond;
std::mutex mutex;
int queue_depth = 0;
int max_qd = 16;
ConsumerProducerQueue<long> job_queue;
int pattern = 7;
int dev_size=10;

struct io_event events[MAX_COUNT];
struct timespec timeout;
char * read_buf;

int send=1;

#define handle_error_en(en, msg) \
           do { errno = en; perror(msg); exit(EXIT_FAILURE); } while (0)

long zyh_start_time;
std::ofstream fout; // 输出日志

long Gettime(){
    struct timeval now;
    gettimeofday(&now, NULL);
    return now.tv_sec * 1000000 + now.tv_usec;
}

struct zyh {
   struct iocb iocb_;
   int num;
   long start;
};

struct time_zyh{
    long into_queue = -1;
    long start_time = -1;
    long end_time = -1;
    long submit = -1;
    long subover = -1;
    int ret_num = 0;
}time_zyh[200000];

long start_time_io = -1;
long end_time_io = -1;


void *eachThread(void *vargp) 
{
    // consumer	
    int id = *(int*)vargp;
     // pin main thread to somewhere
     int s, j;
     cpu_set_t cpuset;
     pthread_t thread;

     thread = pthread_self();

     /* Set affinity mask to include CPUs 0 to 4 */
     CPU_ZERO(&cpuset);
     CPU_SET((id+1)%4, &cpuset);

     s = pthread_setaffinity_np(thread, sizeof(cpu_set_t), &cpuset);
     if (s != 0)
       handle_error_en(s, "pthread_setaffinity_np");

     /* Check the actual affinity mask assigned to the thread */
     s = pthread_getaffinity_np(thread, sizeof(cpu_set_t), &cpuset);
     if (s != 0)
         handle_error_en(s, "pthread_getaffinity_np");

     printf("Set returned by pthread_getaffinity_np() contained:\n");
     for (j = 0; j < CPU_SETSIZE; j++)
         if (CPU_ISSET(j, &cpuset))
             printf("    CPU %d\n", j);
    
    long pos;    // in unit of sector
    printf("Thread %d ready to run \n", id);
    
    int sz;
    long zyh_time;
    long avg_time;
    int zyh_count = 0;
    int i=0;
    // RateLimiter r = new RateLimiter(1000);
    for ( ; ;) {
	    // Consumer wait the queue depth control
        job_queue.consume(pos);
        if (pos == -1) {
            break;
	    }

        if(pos == -2) {
            zyh_time = Gettime();
            avg_time = zyh_time;
            zyh_start_time = zyh_time; 
            continue;
        }

        if(pos == -3) {
            zyh_time = Gettime()-zyh_time;
            printf("thread send time is %ld \n",zyh_time);
            continue;
        }
        i++;
	    while(send==0) ;
        send = 0;
        time_zyh[i].start_time=Gettime();

        struct zyh *z = (struct zyh *)malloc(sizeof(struct zyh));
        struct iocb *p = &(z->iocb_);
        z->start = Gettime();
        z->num = i; 
        io_prep_pread(p, fd, read_buf, STRIDE_SIZE, pos); 
        p->data = (void *) read_buf;

        long slat_time = Gettime();
        if (io_submit(ctx_, 1, &p) != 1) {
            io_destroy(ctx_);
            std::cout << "io submit error" << std::endl;
            exit(1);
        }  
        time_zyh[i].subover=Gettime();
        time_zyh[i].submit=time_zyh[i].subover-slat_time;
        zyh_count++; 
    }
    std::cout << "Thread " << id << " issued all IOs" << std::endl;
    return NULL; 
} 


void *getThread(void *vargp) 
{
    // consumer	
    int id = *(int*)vargp; 
     // pin main thread to somewhere
     int s, j;
     cpu_set_t cpuset;
     pthread_t thread;

     thread = pthread_self();

     /* Set affinity mask to include CPUs 0 to 4 */
     CPU_ZERO(&cpuset);
     CPU_SET((id+1)%4, &cpuset);

     s = pthread_setaffinity_np(thread, sizeof(cpu_set_t), &cpuset);
     if (s != 0)
       handle_error_en(s, "pthread_setaffinity_np");

     /* Check the actual affinity mask assigned to the thread */
     s = pthread_getaffinity_np(thread, sizeof(cpu_set_t), &cpuset);
     if (s != 0)
         handle_error_en(s, "pthread_getaffinity_np");

     printf("Set returned by pthread_getaffinity_np() contained:\n");
     for (j = 0; j < CPU_SETSIZE; j++)
         if (CPU_ISSET(j, &cpuset))
             printf("    CPU %d\n", j);
    
    read_buf = (char *) malloc(sizeof(char) * (STRIDE_SIZE + SECTOR_SIZE));
    int ret = posix_memalign((void **)&read_buf, SECTOR_SIZE, STRIDE_SIZE + SECTOR_SIZE);

    timeout.tv_sec = 0;
    timeout.tv_nsec = 100;

    int i=0;
    int return_seq=0;
    int seq_return=1;
    for (i = num_ios;i>0;) {  
        int ret = io_getevents(ctx_, 0, 1, events, &timeout); // 每次只收1个。
        if (ret < 0) {
            std::cout << "Getevents Error" << std::endl; 
            exit(1);
        } 
	    if (ret > 0) { 
            return_seq++;
            i -= ret;
            send = 1;
        }
        long end_time_io = Gettime();

        for(int z=0;z < ret;z++){
            struct zyh * zh = (struct zyh *) events[z].obj;
            time_zyh[zh->num].end_time= end_time_io;
            time_zyh[zh->num].ret_num=return_seq;
        }
    } 
    return NULL; 
} 

void generate_read_trace(char type) {

     if (type == 'r') {
	    std::cout << "To read randomly" << std::endl;
        srand(time(0));
	    for (int i = 0; i < num_ios; i++)  
            read_order.push_back((long)((rand() %(dev_size*1024*1024*2/d)))*STRIDE_SIZE);
     } else if (type == 's') {
	    std::cout << "To read sequentially with offset " << D << std::endl;
        for (int i = 0; i < num_ios; i++) { 
            read_order.push_back((long)((i*STRIDE_SIZE)) % ((long)dev_size*1024*1024*1024));
	    }
     } else if (type == 'j') {
	    std::cout << "To read stridely with stride: " << D << std::endl;
        for (int i = 0; i < num_ios; i++)
             read_order.push_back(((long)(i+0)*(STRIDE_SIZE + D*SECTOR_SIZE))%((long)dev_size*1024*1024*1024));
     } 
     else {
        std::cout << "Wrong choice of workloads, should be seq/random" << std::endl;
	    exit(1);
     }

     return;
}

int main(int argc, char* * argv) {
     // pin main thread to somewhere
     int s, j;
     cpu_set_t cpuset;
     pthread_t thread;

     thread = pthread_self();

     /* Set affinity mask to include CPUs 0 to 3 */
     CPU_ZERO(&cpuset);     // CPU 集合结构体初始化
     CPU_SET(0, &cpuset);   // 将CPU 0 添加到集合

     s = pthread_setaffinity_np(thread, sizeof(cpu_set_t), &cpuset); // 
     if (s != 0)
       handle_error_en(s, "pthread_setaffinity_np");

     /* Check the actual affinity mask assigned to the thread */
     s = pthread_getaffinity_np(thread, sizeof(cpu_set_t), &cpuset);
     if (s != 0)
         handle_error_en(s, "pthread_getaffinity_np");

     printf("Set returned by pthread_getaffinity_np() contained:\n");
     for (j = 0; j < CPU_SETSIZE; j++)
         if (CPU_ISSET(j, &cpuset))
             printf("    CPU %d\n", j);
     
     printf("===== Multi-thread libaio to Specified Device =====\n");

     // identify chunk size
    if (argc < 5) {
         printf("Wrong parameters: test3 dev_name d(io_size d/2 KB) read_type(random/seq/jump) dev_size\n");
         return 1;
    }


     D = 8;    //offset between two reads, in unit of sector
     j = 1;
     d = atoi(argv[2]);        // request size, d * 1024
     dev_size=atoi(argv[4]);

     STRIDE_SIZE = SECTOR_SIZE * d;
 
     max_qd = 300000; 
     
     job_queue.set_max(max_qd); 

     // open raw block device
     fd = open(argv[1], O_RDONLY | O_DIRECT);      // O_DIRECT
     if (fd < 0) {
         printf("Raw Device Open failed\n");
         return 1;
     } 


    // context to do async IO 
    memset(&ctx_, 0, sizeof(ctx_));
    if (io_setup(MAX_COUNT, &ctx_) != 0) {
        std::cout << "io_context_t set failed" << std::endl;
        exit(1);
    }
    // generate read trace
    generate_read_trace(argv[3][0]);
    
     
     // start the number of threads
    pthread_t * thread_pool = (pthread_t *)malloc(sizeof(pthread_t) * j);


    int *arg = (int *)malloc(sizeof(*arg));
    *arg = 0;
    pthread_create(&thread_pool[0], NULL, eachThread, (void *)arg);
 
    int *arg1 = (int *)malloc(sizeof(*arg1));
    *arg1=1;
    pthread_create(&thread_pool[1], NULL, getThread, (void *)arg1);

     sleep(1);
    
     //as a producer
     struct timeval start, end;
     gettimeofday(&start, NULL);

     long start_send = Gettime();
     job_queue.add(-2); // begin

     for(int i = 1; i <= num_ios; i++) { 
	    job_queue.add(read_order[i]);
        time_zyh[i].into_queue=Gettime(); 
// io2 100G 1000 IOPS 
        if(i<1000) {
            usleep(940);
        } else if(i<2600){
            usleep(560);
        } else if(i<3500){
            usleep(1060);
        } else if(i<4000){
            usleep(1930);
        } else if(i<6000) {
            usleep(435);
        } else {
            usleep(940);
        }

        if(i==15000) sleep(1); 
    }

    long end_send = Gettime() - start_send;
    // 表示已经完成发送。
    job_queue.add(-3); 

    printf("zyh send time is %ld\n",end_send);


    job_queue.add(-1);

     for (int i = 0; i < 2; i++) {
         pthread_join(thread_pool[i], NULL);
     }

    gettimeofday(&end, NULL);
    long time_us = ((end.tv_sec * 1000000 + end.tv_usec)
                  - (start.tv_sec * 1000000 + start.tv_usec));

     std::cout << "All IO finished " << STRIDE_SIZE << std::endl;
     printf("Time taken: %ld us, Bandwidth: %f MB/s \n", time_us, (float)((long)STRIDE_SIZE*num_ios)/1024/1024*1000000/time_us);
     // write log
     std::ofstream fout;
     fout.open("./iotest0.log",std::ios::out);
     fout << "num\tb_t\ts_t\tsm_t\tw_t\tu_t\te_t\tuser_t" << std::endl;
    
    for(int h=1;h<num_ios;h++){
        fout << h <<"\t"<< time_zyh[h].into_queue - zyh_start_time << "\t";
        fout << time_zyh[h].start_time - zyh_start_time << "\t" ;
        fout << time_zyh[h].submit << "\t" ;
        fout << time_zyh[h].end_time - time_zyh[h].subover << "\t";
        fout << time_zyh[h].end_time - time_zyh[h].start_time << "\t";
        fout << time_zyh[h].end_time - zyh_start_time << "\t";
        fout << time_zyh[h].end_time - time_zyh[h].into_queue << std::endl;
    }

    fout.close();
    free(read_buf);
    close(fd);
    return 0;
}
