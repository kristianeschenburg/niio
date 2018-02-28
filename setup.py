from setuptools import setup

setup(name='niio',
      version='0.1',
      description='Small package for quickly loading nueorimaging data types.',
      url='https://github.com/kristianeschenburg/niio',
      author='Kristian M. Eschenburg',
      author_email='keschenb@uw.edu',
      license='MIT',
      packages=['niio'],
      install_requires=['numpy','nibabel',
      'os','csv','h5py','pickle'],
      zip_safe=False)
