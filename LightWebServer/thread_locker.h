#pragma once

#include <pthread.h>
#include <stdio.h>

#ifndef THREAD_LOCKER
#define THREAD_LOCKER


class sem_control {
	/*
	* 提供信号量的控制机制，解决共享量的同时访问问题
	*/

};
class locker {
	/*
	* 基于互斥锁的锁定机制，解决进程关键代码执行异步的问题
	*/
};
class cond_adjust {
	/*
	* 基于条件变量的线程机制，让线程在进行抢占时按照一定的规律进行抢占，减少CPU资源占用
	*/
};
#endif
