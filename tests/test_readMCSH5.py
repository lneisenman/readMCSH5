#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_readMCSH5
----------------------------------

Tests for `readMCSH5` module.
"""

import numpy as np
import pytest


from readMCSH5 import readMCSH5


class TestReadmcsh5(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_something(self):
        print('testing')
        fn1 = 'tests/DIV15 500-30 HD9-25 5sd baseline0001.h5'
        fn2 = 'tests/DIV15 500-30 HD9-25 5sd baseline0001_lne.h5'
        mea1 = readMCSH5.MCSh5MEA(fn1)
        mea2 = readMCSH5.H5MEA(fn2)
        for i in range(60):
            np.testing.assert_allclose(mea1[i], mea2[i])

        assert mea1.dur == mea2.dur

    @classmethod
    def teardown_class(cls):
        pass
