#include <pthread.h>
#include <stdio.h>
#include <semaphore.h>
#include <iostream>
using namespace std;

struct uni {
	int a;
	int b;
};

void* print(void *args) {
	uni* d = (uni*)args;
	d->a++;
	d->b++;
	if (d->a != d->b) printf("%d %d\n", d->a, d->b);
	return NULL;
}
int main(void) {
	uni* ccc, cc;
	ccc = &cc;
	cc.a = 0;
	cc.b = 0;
	pthread_t a, b, c, d, e, f;
	for (int i = 0; i < 10; i++) {
		pthread_create(&a, NULL, &print, (void*)ccc);
		pthread_create(&b, NULL, &print, (void*)ccc);
		pthread_create(&c, NULL, &print, (void*)ccc);
		pthread_create(&d, NULL, &print, (void*)ccc);
		pthread_create(&e, NULL, &print, (void*)ccc);
		pthread_create(&f, NULL, &print, (void*)ccc);
		printf("%c", '\n');
	}
	pthread_exit(NULL);
	cc.a = 0;
	cc.b = 0;
	printf("%c", '\n');
	for (int i = 0; i < 36; i++) {
		ccc->a++;
		printf("%d ", ccc->a);
		ccc->b++;
		printf("%d ", ccc->b);
	}
	
	system("pause");
}