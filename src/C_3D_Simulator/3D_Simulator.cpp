#include <iostream>
#include <Python.h>

int main(int argc, char **argv) {
    std::cout << "Please enter the absolute path to the configuration directory:\n";
    char config_dir_path[254];
    std::cin >> config_dir_path;
    std::cout << config_dir_path;
    char* arguments[3];
    arguments[0] = "3D_Simulator.py";
    arguments[1] = "-d";
    //Change the following line during release
    arguments[2] = "/home/shubham/virtual-vision-simulator/config/sample2";
    //arguments[2] = config_dir_path;
    Py_Initialize();
    PySys_SetArgv(3, arguments);
    PyObject *sys_path;
    PyObject *path;
    sys_path = PySys_GetObject("path");
    //Use the commented line below to use absolute path -
    //path = PyString_FromString("/home/shubham/virtual-vision-simulator/src/");
    path = PyString_FromString("../../");
    if(PyList_Append(sys_path, path) < 0) {
      printf("Error in appending path\n");
      return -1;
    }
    FILE* PythonScriptFile = fopen("../../3D_Simulator.py", "r");
    if(PythonScriptFile)
    {
	PyRun_SimpleFile(PythonScriptFile, "3D_Simulator.py");
	fclose(PythonScriptFile);
    }
    else {
	printf("I am not here");
    }
    Py_Finalize();
    return 0;
}