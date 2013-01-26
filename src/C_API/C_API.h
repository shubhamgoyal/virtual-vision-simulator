#include <Python.h>
#include <iostream>

int setUpClients();//This should be the first function to be called
void freeMemory();//This function should always be called at the end before closing the simulator to free up the memory allocated to Python interpreter
int pan(int camera_number, double angle, double speed);
int tilt(int camera_number, double angle, double speed);
int zoom(int camera_number, double angle, double speed);
int getImage(int camera_number);
int waits();