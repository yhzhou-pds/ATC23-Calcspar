
init: init.c
	gcc -o init -D_GNU_SOURCE init.c

test3: observe_each_io.cpp ConsumerProducerQueue.h
	g++ -std=c++11 -o test3 -D_GNU_SOURCE observe_each_io.cpp ConsumerProducerQueue.h -lpthread -laio

clean:
	rm init test3
