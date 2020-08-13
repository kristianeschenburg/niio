from niio import write
import numpy as np
import pandas

class ParcelImage(object):

    """

    Data structure containing data corresponding to a parcellation map.  This data can be any 
    scalar value.  The data structure scalar data can be accessed by indexing via parcel name.
    This structure can also write the parcel scalar values to a surface map.

    """

    def __init__(self, index_map, rows=32492, columns=1, hemisphere='L'):

        """
        Instantiate ParcelImage object.
        """

        V = np.concatenate([index_map[k] for k in index_map.keys()])
        V.sort()

        if not rows:
            rows = V.max() + 1
        
        self.index_map = index_map
        self.rows = rows
        self.columns = columns
        self.hemisphere = hemisphere
    

    def set_data(self, X):

        """
        Set ParcelImage sclar data.

        Parameters:
        - - - - -
        X: Pandas DataFrame
            Data corresponding to individual parcels.
            
            DataFrame indices must be the parcel names.
            i.e. the df.index values must be included in 
            index_map.keys()

        """

        assert isinstance(X, pandas.core.frame.DataFrame)

        _, p = X.shape
        data = np.zeros((self.rows, self.columns))*np.nan

        for region in X.index:

            ridx = self.index_map[region]
            data[ridx, :] = X.loc[region]

        self.data = data

    def get_data(self):

        """
        Get whole ParcelImage DataFrame
        """

        return self.data

    def get_parcel(self, roi):

        """
        Get scalar value for specific parcel.

        Parameters:
        - - - - -
        roi: string
            parcel name
        """

        return self.data.loc[roi]

    def write(self, outname):

        """
        Write ParcelImage to GIFTI file.

        Parameters:
        - - - - -
        outname: string
            output name
        """

        write.save(self.data, outname, self.hemisphere)
