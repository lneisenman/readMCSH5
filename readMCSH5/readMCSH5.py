# -*- coding: utf-8 -*-

import h5py
import numpy as np

import h5shelve


class MEA():
    """ This class implements a dictionary of numpy arrays that can be indexed
    by a string composed of the row and column number of the corresponding MEA
    or by an integer index between zero and 59. It also has a field ('dur')for
    the duration of the data collection.
    """

    def __init__(self):

        self._ordered_keys = ['12', '13', '14', '15', '16', '17',
                              '21', '22', '23', '24', '25', '26', '27', '28',
                              '31', '32', '33', '34', '35', '36', '37', '38',
                              '41', '42', '43', '44', '45', '46', '47', '48',
                              '51', '52', '53', '54', '55', '56', '57', '58',
                              '61', '62', '63', '64', '65', '66', '67', '68',
                              '71', '72', '73', '74', '75', '76', '77', '78',
                              '82', '83', '84', '85', '86', '87']

        self.dur = 0
        self.spike_times = {}
        for key in self._ordered_keys:
            self.spike_times[key] = np.zeros(0)

    def __len__(self):
        return len(self.spike_times)

    def __getitem__(self, key):
        if key in self.spike_times.keys():
            return self.spike_times[key]
        elif (isinstance(key, int)) and (0 <= key < 60):
            return self.spike_times[self._ordered_keys[key]]
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key in self.spike_times.keys():
            self.spike_times[key] = value
        elif (isinstance(key, int)) and (0 <= key < 60):
            self.spike_times[self._ordered_keys[key]] = value
        else:
            raise KeyError

    def __iter__(self):
        for key in self._ordered_keys:
            yield self.spike_times[key]

    def iterkeys(self):
        return iter(self.keys())

    def keys(self):
        return self.spike_times.keys()

    def __contains__(self, item):
        return (item in self.spike_times.keys())


class MCSh5MEA(MEA):
    ''' This class returns a MEA that is created from an HDF5 file created
        by the MCS data conversion utility'''

    def __init__(self, file_name):
        super().__init__()
        with h5py.File(file_name) as db:
            ts_stream = db['Data']['Recording_0']['TimeStampStream']['Stream_0']
            for i in range(60):
                tse = 'TimeStampEntity_' + str(i)
                loc = str(ts_stream['InfoTimeStamp'][i][-1], 'utf-8')
                if tse in ts_stream:
                    self[loc] = np.asarray(ts_stream[tse].value[0],
                                           dtype=np.float)/10e5

            self.dur = db['Data']['Recording_0'].attrs['Duration']/10e5


class H5MEA(MEA):
    ''' THis class returns a MEA that is created from a custom HDF5 file '''

    def __init__(self, file_name):
        super().__init__()
        with h5shelve.open(file_name, 'r') as hfile:
            for key in hfile:
                if key == 'dur':
                    self.dur = hfile['dur']
                else:
                    self.spike_times[key] = hfile[key]
