# What is niio?

**niio** is a Python package for quickly loading in common neuroimaging data.  It's a class of methods that act as wrappers for common input formats like those offered by the **scipy**, **nibabel**, **h5py** **pickle** libraries.  
Current functionality includes **loading**, **saving**, and **converting between** various formats.

While the above libraries work fine, I wanted a way to access the data without needing to remember / write out specifically what attributes and methods would specifically return the data.  As an example, with **nibabel**, for **Gifti** formattd data:

```python
import nibabel as nb
func_file = '../data/func.gii'
func = nb.load(func_file)

# get access to the data array
func_data = nb.darrays[0].data

# and if func_file has multiple data arrays...
for i in np.arange(num_darrays):
        func_data = nb.load(darrays[i]).data
```

I wanted a convenient way just to get all the data at once.

# How to use?

```bash
git clone https://github.com/kristianeschenburg/niio.git
cd .
pip install .
```

# Example usage:

We begin by loading in the necessary modules.  As named, **loaded** is used for loading data, **write** is used for saving data, and **convert** is used for converting between file formats.

```python
from niio import loaded, write, convert
```

### Matlab files
Let's start by loading in a conventional Matlab *.mat* file.

```python
ex1 = loaded.load('../data/matrix.mat')
print(ex1.shape)
```

We see that **ex1** is a (5,10) matrix.  However, what we can't see immediately, is that ```matrix.mat``` contains two arrays, named *mat1* and *mat2*.  If we know what our specific arrays are called, we can load each one by name:

```python
ex1 = loaded.load('../data/matrix.mat', dataset='mat1')
ex2 = loaded.load('../data/matrix.mat', dataset='mat2')
print(ex1.shape)
print(ex2.shape)
```

Generally, we'll only save one array per .mat file, so this is more for convenience.

### Gifti Files

```python
func = loaded.load('../data/func.gii')
print(func), print(func.shape)
```

And if you know which data array you might be interested in:

```python
func = loaded.load('../data/func.gii',dataset=1)
print(func), print(func.shape)
```