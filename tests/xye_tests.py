import unittest
import nose
from os.path import join
from nose.tools import eq_
from StringIO import StringIO
import numpy as np

from xye import XYEDataset


class DatasetLoadingTest(unittest.TestCase):
    def setUp(self):
        self.basedir = join('tests', 'testdata')

    def simple_xye_load_test(self):
        filename = join(self.basedir, 'test1.xye')
        data = XYEDataset._load_xye_data(filename)
        eq_(data.shape, (3,3))
        eq_(data[1,1], 20000.0)

    def xye_load_test(self):
        filename = join(self.basedir,
                        'si640c_low_temp_cal_p1_scan0.000000_adv0_0000.xye')
        data = XYEDataset._load_xye_data(filename)
        eq_(data.shape, (20458,3))

    def xy_load_test(self):
        filename = join(self.basedir,
                        'si640c_low_temp_cal_p1_scan0.000000_adv0_0000.xy')
        data = XYEDataset._load_xye_data(filename)
        eq_(data.shape, (20458,3))
        self.assertTrue(np.allclose(data[:10,2], np.zeros((10,1))))

    def xye_save_test(self):
        filename = join(self.basedir,
                        'si640c_low_temp_cal_p1_scan0.000000_adv0_0000.xye')
        dataset = XYEDataset.from_file(filename)
        f = StringIO()
        dataset.save(f)

        f.seek(0)
        data = XYEDataset._load_xye_data(f)
        eq_(data.shape, (20458, 3))

    def xye_copy_test(self):
        filename = join(self.basedir,
                        'si640c_low_temp_cal_p1_scan0.000000_adv0_0000.xye')
        dataset = XYEDataset.from_file(filename)
        copied_dataset = dataset.copy()
        self.assertTrue(np.allclose(dataset.data, copied_dataset.data))



if __name__ == '__main__':
    nose.main()
