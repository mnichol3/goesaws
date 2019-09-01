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



    ############################ get_avail_years ############################

    # Test invalid satellite
    def test_get_avail_years1(self):
        with self.assertRaises(Exception) as context:
                years = self.conn.get_avail_years('wrong', 'also wrong')
                self.assertTrue('Invalid satallite parameter' in context.exception)

        with self.assertRaises(Exception) as context:
                years = self.conn.get_avail_years('g16', 'also wrong')
                self.assertTrue('Invalid satallite parameter' in context.exception)



    # Test valid sat, invalid sensor param
    def test_get_avail_years2(self):
        with self.assertRaises(Exception) as context:
                years = self.conn.get_avail_years('goes16', 'wrong')
                self.assertTrue('Invalid sensor parameter' in context.exception)

        with self.assertRaises(Exception) as context:
                years = self.conn.get_avail_years('goes17', 'wrong')
                self.assertTrue('Invalid sensor parameter' in context.exception)



    # Test missing sector/product params
    def test_get_avail_years3(self):
        years = self.conn.get_avail_years('goes16', 'abi')
        self.assertEqual(len(years), 0)
        self.assertEqual(years, [])

        with self.assertRaises(Exception) as context:
            years = self.conn.get_avail_years('goes16', 'abi', product='ABI-L1b-RadF')
            self.assertTrue('Sector cannot be None' in context.exception)

        years = self.conn.get_avail_years('goes16', 'abi', sector='C')
        self.assertEqual(len(years), 0)
        self.assertEqual(years, [])

        with self.assertRaises(Exception) as context:
            years = self.conn.get_avail_years('goes16', 'abi', product='ABI-L2-CMIP', sector='M3')
            self.assertTrue('Invalid sector parameter' in context.exception)



    # Test valid params
    def test_get_avail_years4(self):
        years = self.conn.get_avail_years('goes16', 'abi', product='ABI-L1b-RadC', sector='C')
        self.assertEqual(len(years), 4)
        self.assertEqual(years, ['2000', '2017', '2018', '2019'])

        years = self.conn.get_avail_years('goes16', 'abi', product='ABI-L2-CMIPC', sector='C')
        self.assertEqual(len(years), 4)
        self.assertEqual(years, ['2000', '2017', '2018', '2019'])

        years = self.conn.get_avail_years('goes16', 'abi', product='ABI-L2-CMIP', sector='M1')
        self.assertEqual(len(years), 4)
        self.assertEqual(years, ['2000', '2017', '2018', '2019'])

        years = self.conn.get_avail_years('goes16', 'abi', product='ABI-L2-CMIP', sector='M2')
        self.assertEqual(len(years), 4)
        self.assertEqual(years, ['2000', '2017', '2018', '2019'])



    ############################ get_avail_months ############################




if __name__ == '__main__':
    unittest.main()
