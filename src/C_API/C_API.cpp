#include "C_API.h"

int setUpClients() {
    Py_Initialize();
    PyObject *sys_path;
    PyObject *path;
    sys_path = PySys_GetObject("path");
    //Use the commented line below to use absolute path -
    //path = PyString_FromString("/home/shubham/virtual-vision-simulator/src/");
    path = PyString_FromString("../../");
    if(PyList_Append(sys_path, path) < 0) {
      printf("Error in appending path\n");
    }
    PyObject *pName, *pModule, *pFunc;
    PyObject *pArgs, *pValue;
    pName = PyString_FromString("boss_client");
    pModule = PyImport_Import(pName);
    Py_DECREF(pName);
    if (pModule != NULL) {
        pFunc = PyObject_GetAttrString(pModule, "main");
        if (pFunc && PyCallable_Check(pFunc)) {
            pArgs = PyTuple_New(0);
            pValue = PyObject_CallObject(pFunc, pArgs);
            Py_DECREF(pArgs);
            if (pValue != NULL) {
                Py_DECREF(pValue);
            }
            else {
                Py_DECREF(pFunc);
                Py_DECREF(pModule);
                PyErr_Print();
                fprintf(stderr,"Call failed\n");
                return 1;
            }
        }
        else {
            if (PyErr_Occurred())
                PyErr_Print();
            fprintf(stderr, "Cannot find function \"%s\"\n", "pan");
        }
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
    }
    else {
        PyErr_Print();
        fprintf(stderr, "Failed to load \"%s\"\n", "boss_client.py");
        return 1;
    }
    printf("setUpClients has exitted\n");
    return 0;
}

//This function should always be called at the end before closing the simulator to free up the memory allocated to Python interpreter
void freeMemory() {
    Py_Finalize();
}

int pan(int camera_number, double angle, double speed) {
    printf("Panning camera %d to an angle of %f degrees with speed %f\n", camera_number, angle, speed);
    PyObject *pName, *pModule, *pFunc;
    PyObject *pArgs, *pValue;
    pName = PyString_FromString("boss_client");
    pModule = PyImport_Import(pName);
    Py_DECREF(pName);
    if (pModule != NULL) {
        pFunc = PyObject_GetAttrString(pModule, "pan");
        if (pFunc && PyCallable_Check(pFunc)) {
            pArgs = PyTuple_New(3);
	    pValue = PyInt_FromLong((long)camera_number);
            if (!pValue) {
		Py_DECREF(pArgs);
		Py_DECREF(pModule);
		fprintf(stderr, "Cannot convert argument\n");
		return 1;
            }
            PyTuple_SetItem(pArgs, 0, pValue);
	    pValue = PyFloat_FromDouble(angle);
            if (!pValue) {
		Py_DECREF(pArgs);
		Py_DECREF(pModule);
		fprintf(stderr, "Cannot convert argument\n");
		return 1;
            }
            PyTuple_SetItem(pArgs, 1, pValue);
	    pValue = PyFloat_FromDouble(speed);
            if (!pValue) {
		Py_DECREF(pArgs);
		Py_DECREF(pModule);
		fprintf(stderr, "Cannot convert argument\n");
		return 1;
            }
            PyTuple_SetItem(pArgs, 2, pValue);
            pValue = PyObject_CallObject(pFunc, pArgs);
            Py_DECREF(pArgs);
            if (pValue != NULL) {
                Py_DECREF(pValue);
            }
            else {
                Py_DECREF(pFunc);
                Py_DECREF(pModule);
                PyErr_Print();
                fprintf(stderr,"Call failed\n");
                return 1;
            }
        }
        else {
            if (PyErr_Occurred())
                PyErr_Print();
            fprintf(stderr, "Cannot find function \"%s\"\n", "pan");
        }
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
    }
    else {
        PyErr_Print();
        fprintf(stderr, "Failed to load \"%s\"\n", "boss_client.py");
        return 1;
    }
    return 0;
}

int tilt(int camera_number, double angle, double speed) {
    printf("Tilting camera %d to an angle of %f degrees with speed %f\n", camera_number, angle, speed);
    PyObject *pName, *pModule, *pFunc;
    PyObject *pArgs, *pValue;
    pName = PyString_FromString("boss_client");
    pModule = PyImport_Import(pName);
    Py_DECREF(pName);
    if (pModule != NULL) {
        pFunc = PyObject_GetAttrString(pModule, "tilt");
        if (pFunc && PyCallable_Check(pFunc)) {
            pArgs = PyTuple_New(3);
	    pValue = PyInt_FromLong((long)camera_number);
            if (!pValue) {
		Py_DECREF(pArgs);
		Py_DECREF(pModule);
		fprintf(stderr, "Cannot convert argument\n");
		return 1;
            }
            PyTuple_SetItem(pArgs, 0, pValue);
	    pValue = PyFloat_FromDouble(angle);
            if (!pValue) {
		Py_DECREF(pArgs);
		Py_DECREF(pModule);
		fprintf(stderr, "Cannot convert argument\n");
		return 1;
            }
            PyTuple_SetItem(pArgs, 1, pValue);
	    pValue = PyFloat_FromDouble(speed);
            if (!pValue) {
		Py_DECREF(pArgs);
		Py_DECREF(pModule);
		fprintf(stderr, "Cannot convert argument\n");
		return 1;
            }
            PyTuple_SetItem(pArgs, 2, pValue);
            pValue = PyObject_CallObject(pFunc, pArgs);
            Py_DECREF(pArgs);
            if (pValue != NULL) {
                Py_DECREF(pValue);
            }
            else {
                Py_DECREF(pFunc);
                Py_DECREF(pModule);
                PyErr_Print();
                fprintf(stderr,"Call failed\n");
                return 1;
            }
        }
        else {
            if (PyErr_Occurred())
                PyErr_Print();
            fprintf(stderr, "Cannot find function \"%s\"\n", "tilt");
        }
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
    }
    else {
        PyErr_Print();
        fprintf(stderr, "Failed to load \"%s\"\n", "boss_client.py");
        return 1;
    }
    return 0;
}

int zoom(int camera_number, double angle, double speed) {
    printf("Zooming camera %d to an angle of %f degrees with speed %f\n", camera_number, angle, speed);
    PyObject *pName, *pModule, *pFunc;
    PyObject *pArgs, *pValue;
    pName = PyString_FromString("boss_client");
    pModule = PyImport_Import(pName);
    Py_DECREF(pName);
    if (pModule != NULL) {
        pFunc = PyObject_GetAttrString(pModule, "zoom");
        if (pFunc && PyCallable_Check(pFunc)) {
            pArgs = PyTuple_New(3);
	    pValue = PyInt_FromLong((long)camera_number);
            if (!pValue) {
		Py_DECREF(pArgs);
		Py_DECREF(pModule);
		fprintf(stderr, "Cannot convert argument\n");
		return 1;
            }
            PyTuple_SetItem(pArgs, 0, pValue);
	    pValue = PyFloat_FromDouble(angle);
            if (!pValue) {
		Py_DECREF(pArgs);
		Py_DECREF(pModule);
		fprintf(stderr, "Cannot convert argument\n");
		return 1;
            }
            PyTuple_SetItem(pArgs, 1, pValue);
	    pValue = PyFloat_FromDouble(speed);
            if (!pValue) {
		Py_DECREF(pArgs);
		Py_DECREF(pModule);
		fprintf(stderr, "Cannot convert argument\n");
		return 1;
            }
            PyTuple_SetItem(pArgs, 2, pValue);
            pValue = PyObject_CallObject(pFunc, pArgs);
            Py_DECREF(pArgs);
            if (pValue != NULL) {
                Py_DECREF(pValue);
            }
            else {
                Py_DECREF(pFunc);
                Py_DECREF(pModule);
                PyErr_Print();
                fprintf(stderr,"Call failed\n");
                return 1;
            }
        }
        else {
            if (PyErr_Occurred())
                PyErr_Print();
            fprintf(stderr, "Cannot find function \"%s\"\n", "zoom");
        }
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
    }
    else {
        PyErr_Print();
        fprintf(stderr, "Failed to load \"%s\"\n", "boss_client.py");
        return 1;
    }
    return 0;
}

int getImage(int camera_number) {
    PyObject *pName, *pModule, *pFunc;
    PyObject *pArgs, *pValue;
    pName = PyString_FromString("boss_client");
    //PyGILState_STATE state = PyGILState_Ensure();
    pModule = PyImport_Import(pName);
    Py_DECREF(pName);
    if (pModule != NULL) {
        pFunc = PyObject_GetAttrString(pModule, "getImage");
        if (pFunc && PyCallable_Check(pFunc)) {
            pArgs = PyTuple_New(1);
	    pValue = PyInt_FromLong((long)camera_number);
            if (!pValue) {
		Py_DECREF(pArgs);
		Py_DECREF(pModule);
		fprintf(stderr, "Cannot convert argument\n");
		return 1;
            }
            PyTuple_SetItem(pArgs, 0, pValue);
            pValue = PyObject_CallObject(pFunc, pArgs);
            Py_DECREF(pArgs);
            if (pValue != NULL) {
                Py_DECREF(pValue);
            }
            else {
                Py_DECREF(pFunc);
                Py_DECREF(pModule);
                PyErr_Print();
                fprintf(stderr,"Call failed\n");
                return 1;
            }
        }
        else {
            if (PyErr_Occurred())
                PyErr_Print();
            fprintf(stderr, "Cannot find function \"%s\"\n", "getImage");
        }
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
    }
    else {
        PyErr_Print();
        fprintf(stderr, "Failed to load \"%s\"\n", "boss_client.py");
        return 1;
    }
    //PyGILState_Release(state);
    //freeMemory();
    return 0;
}

int waits() {
    PyObject *pName, *pModule, *pFunc;
    PyObject *pArgs, *pValue;
    pName = PyString_FromString("boss_client");
    //PyGILState_STATE state = PyGILState_Ensure();
    pModule = PyImport_Import(pName);
    Py_DECREF(pName);
    if (pModule != NULL) {
        pFunc = PyObject_GetAttrString(pModule, "wait");
        if (pFunc && PyCallable_Check(pFunc)) {
            pArgs = PyTuple_New(0);
            pValue = PyObject_CallObject(pFunc, pArgs);
            Py_DECREF(pArgs);
            if (pValue != NULL) {
                Py_DECREF(pValue);
            }
            else {
                Py_DECREF(pFunc);
                Py_DECREF(pModule);
                PyErr_Print();
                fprintf(stderr,"Call failed\n");
                return 1;
            }
        }
        else {
            if (PyErr_Occurred())
                PyErr_Print();
            fprintf(stderr, "Cannot find function \"%s\"\n", "getImage");
        }
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
    }
    else {
        PyErr_Print();
        fprintf(stderr, "Failed to load \"%s\"\n", "boss_client.py");
        return 1;
    }
    //PyGILState_Release(state);
    //freeMemory();
    return 0;
}