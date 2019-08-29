from datetime import datetime
from unittest import TestCase

import pytz  # Unneeded?

import goesaws

class TestGoesAwsFile(TestCase):
    def setUp(self):
        query = goesaws.GoesAwsInterface()
        self.test_scan = query.get_avail_images('goes16', 'ABI-L1b-RadM', '5-23-2019-21', 'M2', '13')

    def test_scan_time(self):
        self.assertEqual(self.test_scan.scan_time, '05-23-2019-21:00')

    def test_filename(self):
        self.assertEqual(self.test_scan.filename, 'OR_ABI-L1b-RadM2-M6C13_G16_s20191432100129_e20191432100199_c20191432100234.nc')

    def test_shortname(self):
        self.assertEqual(self.test_scan.shortname, 'RadM2-M6C13 05-23-2019-21:00')
