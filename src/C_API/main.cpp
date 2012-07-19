#include <pthread.h>
#include "C_API.h"

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

int main(int argc, char **argv) {
    //pthread_t thread1;
    //pthread_create(&thread1, NULL, setUpClients_wrapper, NULL);
    setUpClients();
    //printf("I am here before the first cin.ignore()\n");
    //std::cin.ignore();
    //printf("I am here before the first pan\n");
    //pthread_t thread2;
    //struct pan_thread_args struct1;
    //struct1.camera_number = 5;
    //struct1.angle = 10;
    //struct1.speed = 20;
    //pthread_create(&thread2, NULL, pan_wrapper, &struct1);
    //pan(5, 10, 20);
    //printf("I am here before the second cin.ignore()\n");
    //std::cin.ignore();
    //std::cin.ignore();
    //printf("I am here before the second pan\n");
    getImage(1);
    /*pan(1, 10, 20);
    for(int i = 0; i < 10; i++) {
	printf("I reach the for loop iteration %d\n", i);
	for (int j = 0; j < 1000000; j++) {
	}
	getImage(1);
    }*/
    
    //std::cin.ignore();
    //std::cin.ignore();
    freeMemory();
}