import unittest
import os.path as osp
import sys
if __name__ == '__main__':
    sys.path.insert(0, './../..')
from gpio import sysfspaths as sysfs

class PinPathsTestCases(unittest.TestCase):
    def test_export_path(self):
        path = sysfs.Paths.export_path()
        (export_directory,export_filename) = osp.split(path)
        self.assertEqual( export_directory, sysfs.Paths.gpio_path())
        self.assertEqual( export_filename, sysfs.Paths.export_file())
 
    def test_unexport_path(self):
        path = sysfs.Paths.unexport_path()
        (export_directory,export_filename) = osp.split(path)
        self.assertEqual( export_directory, sysfs.Paths.gpio_path())
        self.assertEqual( export_filename, sysfs.Paths.unexport_file())

    def test_pin_path(self):
        pinId = 1
        path = sysfs.Paths.pin_path(pinId)
        (export_directory,export_filename) = osp.split(path)
        self.assertEqual( export_directory, sysfs.Paths.gpio_path())
        self.assertEqual( export_filename, sysfs.Paths.pin_dir_base()+str(pinId))

    def test_direction_path(self):
        pinId = 4
        path = sysfs.Paths.direction_path(pinId)
        (export_directory,export_filename) = osp.split(path)
        self.assertEqual( export_directory, sysfs.Paths.gpio_path() + '/' + sysfs.Paths.pin_dir_base()+str(pinId))
        self.assertEqual( export_filename, sysfs.Paths.pin_direction_file())

    def test_edgemode_path(self):
        pinId = 23
        path = sysfs.Paths.edgemode_path(pinId)
        (export_directory,export_filename) = osp.split(path)
        self.assertEqual( export_directory, sysfs.Paths.gpio_path() + '/' + sysfs.Paths.pin_dir_base()+str(pinId))
        self.assertEqual( export_filename, sysfs.Paths.pin_edgemode_file())

    def test_value_path(self):
        pinId = 15
        path = sysfs.Paths.value_path(pinId)
        (export_directory,export_filename) = osp.split(path)
        self.assertEqual( export_directory, sysfs.Paths.gpio_path() + '/' + sysfs.Paths.pin_dir_base()+str(pinId))
        self.assertEqual( export_filename, sysfs.Paths.pin_value_file())

if __name__ == '__main__':
    unittest.main()
