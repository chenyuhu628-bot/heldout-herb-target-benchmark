# Reproduction environment

The frozen score export in this release was executed with:

    Python 3.12.13
    PyTorch 2.6.0+cu124
    torch-geometric 2.8.0
    NumPy 2.4.6
    pandas 3.0.3
    scikit-learn 1.9.0
    SciPy 1.17.1
    NetworkX 3.6.1

For an NVIDIA CUDA 12.4 environment, install:

    python -m pip install -r environment/requirements_cuda_reproduce.txt

For CPU-only validation, install:

    python -m pip install -r environment/requirements_cpu_reproduce.txt

The archived exported scores and reported metrics are the reference result. A new computation on a different device or backend should be checked against the historical reference at the tolerance specified by the export command. It is expected to preserve ranking metrics and satisfy the listed 1e-6 comparisons under the validated environment; a different numerical stack can introduce small floating-point differences.
