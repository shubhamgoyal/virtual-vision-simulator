#include <pthread.h>
#include "C_API.h"

pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;
int condition;
pthread_cond_t cond1;

struct pan_thread_args {
    int camera_number;
    double angle;
    double speed;
};

void *pan_wrapper(void *arg) {
    struct pan_thread_args args = *((struct pan_thread_args *)arg);
    int camera_number = args.camera_number;
    double angle = args.angle;
    double speed = args.speed;
    pan(camera_number, angle, speed);
}
void *setUpClients_wrapper(void *arg) {
    setUpClients();
}

void *wait_wrapper(void *arg) {
    while(1) {
      pthread_mutex_lock(&m);
      while (!condition) {
	  pthread_cond_wait(&cond1, &m);
      }
      waits();
      pthread_mutex_unlock(&m);
    }
}

int main(int argc, char **argv) {
  
    condition = 1;
    pthread_cond_init(&cond1, NULL);
  
    pthread_t thread1;
    pthread_create(&thread1, NULL, setUpClients_wrapper, NULL);
    
    int input;
    std::cin >> input;
    
    pthread_t thread2;
    pthread_create(&thread2, NULL, wait_wrapper, NULL);
    
    int angle = 10;
    while(1) {
	//Your code here
	std::cin >> input;
	
	condition = 0;
	pthread_mutex_lock(&m);
	while (condition) {
	    pthread_cond_wait(&cond1, &m); 
	}
	for(int i = 1; i <= 6; i++) {
	    getImage(i);
	}
	condition = 1;
	pthread_mutex_unlock(&m);
	pthread_cond_signal(&cond1);
	
	//Your code here
	std::cin >> input;
	
	condition = 0;
	pthread_mutex_lock(&m);
	while (condition) {
	    pthread_cond_wait(&cond1, &m); 
	}
	angle = angle + 10;
	for(int i = 3; i <= 6; i++) {
	    pan(i, angle, 100);
	    tilt(i, angle, 100);
	    zoom(i, angle, 100);
	}
	condition = 1;
	pthread_mutex_unlock(&m);
	pthread_cond_signal(&cond1);
	
	//Your code here
	std::cin >> input;
    }
}