/*[clinic input]
preserve
[clinic start generated code]*/

PyDoc_STRVAR(miller_rabin_miller_rabin_deterministic32__doc__,
"miller_rabin_deterministic32($module, n, /)\n"
"--\n"
"\n"
"Perform deterministic Miller-Rabin primality test on the 32-bit unsigned int.");

#define MILLER_RABIN_MILLER_RABIN_DETERMINISTIC32_METHODDEF    \
    {"miller_rabin_deterministic32", (PyCFunction)miller_rabin_miller_rabin_deterministic32, METH_O, miller_rabin_miller_rabin_deterministic32__doc__},

static int
miller_rabin_miller_rabin_deterministic32_impl(PyObject *module,
                                               PyLongObject *n);

static PyObject *
miller_rabin_miller_rabin_deterministic32(PyObject *module, PyLongObject *n)
{
    PyObject *return_value = NULL;
    int _return_value;

    _return_value = miller_rabin_miller_rabin_deterministic32_impl(module, n);
    if ((_return_value == -1) && PyErr_Occurred()) {
        goto exit;
    }
    return_value = PyBool_FromLong((long)_return_value);

exit:
    return return_value;
}

PyDoc_STRVAR(miller_rabin_miller_rabin_deterministic64__doc__,
"miller_rabin_deterministic64($module, n, /)\n"
"--\n"
"\n"
"Perform deterministic Miller-Rabin primality test on the 64-bit unsigned int.");

#define MILLER_RABIN_MILLER_RABIN_DETERMINISTIC64_METHODDEF    \
    {"miller_rabin_deterministic64", (PyCFunction)miller_rabin_miller_rabin_deterministic64, METH_O, miller_rabin_miller_rabin_deterministic64__doc__},

static int
miller_rabin_miller_rabin_deterministic64_impl(PyObject *module,
                                               PyLongObject *n);

static PyObject *
miller_rabin_miller_rabin_deterministic64(PyObject *module, PyLongObject *n)
{
    PyObject *return_value = NULL;
    int _return_value;

    _return_value = miller_rabin_miller_rabin_deterministic64_impl(module, n);
    if ((_return_value == -1) && PyErr_Occurred()) {
        goto exit;
    }
    return_value = PyBool_FromLong((long)_return_value);

exit:
    return return_value;
}

PyDoc_STRVAR(miller_rabin_miller_rabin__doc__,
"miller_rabin($module, n, k=10, /)\n"
"--\n"
"\n"
"Perform Miller-Rabin primality test on the arbitrary precision int.\n"
"\n"
"A deterministic variant is auto-selected if n fits into 64-bit unsigned;\n"
"otherwise, the probablistic variant is used, and k determines the number of\n"
"test rounds to perform.");

#define MILLER_RABIN_MILLER_RABIN_METHODDEF    \
    {"miller_rabin", (PyCFunction)miller_rabin_miller_rabin, METH_VARARGS, miller_rabin_miller_rabin__doc__},

static int
miller_rabin_miller_rabin_impl(PyObject *module, PyLongObject *n, int k);

static PyObject *
miller_rabin_miller_rabin(PyObject *module, PyObject *args)
{
    PyObject *return_value = NULL;
    PyLongObject *n;
    int k = 10;
    int _return_value;

    if (!PyArg_ParseTuple(args, "O|i:miller_rabin",
        &n, &k)) {
        goto exit;
    }
    _return_value = miller_rabin_miller_rabin_impl(module, n, k);
    if ((_return_value == -1) && PyErr_Occurred()) {
        goto exit;
    }
    return_value = PyBool_FromLong((long)_return_value);

exit:
    return return_value;
}
/*[clinic end generated code: output=16d77986226ddc46 input=a9049054013a1b77]*/
