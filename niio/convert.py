from niio import loaded, write
import numpy as np
import scipy.io as sio

def mat2func(in_mat, out_func, hemisphere):

    """
    Method to quickly convert between Matlab .mat and Gifti .func.gii files.

    Parameters:
    - - - - -
    in_mat: str
        Matlab .mat file to convert
    out_func: str
        Gifti .func.gii to create
    """

    mat = loaded.load(in_mat)
    mat = mat.squeeze()
    write.save(mat, out_func, hemisphere)


def func2mat(in_func, out_mat):
    """
    Method to quickly convert between Matlab .mat and Gifti .func.gii files.

    Parameters:
    - - - - -
    in_func: str
        Gifti .func.gii or .label.gii file to convert
    out_mat: str
        Matlab .mat file to generate
    """

    func = loaded.load(in_func)
    func = func.squeeze()

    mat = {'data': func}
    sio.savemat(out_mat, mat)
