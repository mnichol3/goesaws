from datetime import datetime
import unittest
import warnings

import pytz  # Unneeded?

import goesawsinterface


class TestGoesAwsInterface(unittest.TestCase):
    def setUp(self):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        self.conn = goesawsinterface.GoesAWSInterface()



    ########################### get_avail_products ###########################

    # Test invalid satellite param
    def test_get_avail_products1(self):
        with self.assertRaises(Exception) as context:
                prods = self.conn.get_avail_products('wrong', sensor=None)
                self.assertTrue('Invalid satallite parameter' in context.exception)

        with self.assertRaises(Exception) as context:
                prods = conn.get_avail_products('wrong', sensor='glm')
                self.assertTrue('Invalid satallite parameter' in context.exception)

        with self.assertRaises(Exception) as context:
                prods = self.conn.get_avail_products('g16', sensor=None)
                self.assertTrue('Invalid satallite parameter' in context.exception)



    # Test glm product
    def test_get_avail_products2(self):
        prods = self.conn.get_avail_products('goes16', sensor='glm')
        self.assertEqual(len(prods), 1)
        self.assertEqual(prods, ['GLM-L2-LCFA'])

        prods = self.conn.get_avail_products('goes17', sensor='glm')
        self.assertEqual(len(prods), 1)
        self.assertEqual(prods, ['GLM-L2-LCFA'])



    # Test abi products
    def test_get_avail_products2(self):
        abi_prods = ['ABI-L1b-RadC', 'ABI-L1b-RadF', 'ABI-L1b-RadM',
                     'ABI-L2-CMIPC', 'ABI-L2-CMIPF', 'ABI-L2-CMIPM',
                     'ABI-L2-FDCC', 'ABI-L2-FDCF', 'ABI-L2-MCMIPC',
                     'ABI-L2-MCMIPF', 'ABI-L2-MCMIPM']

        prods = self.conn.get_avail_products('goes16', sensor='abi')
        prods.sort()
        self.assertEqual(len(prods), 11)
        self.assertEqual(prods, abi_prods)

        prods = self.conn.get_avail_products('goes17', sensor='abi')
        prods.sort()
        self.assertEqual(len(prods), 11)
        self.assertEqual(prods, abi_prods)

    # def test_scan_time(self):
    #     self.assertEqual(self.test_scan.scan_time, '05-23-2019-21:00')
    #
    # def test_filename(self):
    #     self.assertEqual(self.test_scan.filename, 'OR_ABI-L1b-RadM2-M6C13_G16_s20191432100129_e20191432100199_c20191432100234.nc')
    #
    # def test_shortname(self):
    #     self.assertEqual(self.test_scan.shortname, 'RadM2-M6C13 05-23-2019-21:00')

if __name__ == '__main__':
    unittest.main()
