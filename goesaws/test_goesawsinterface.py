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

    # Test invalid satellite param
    def test_get_avail_months1(self):
        with self.assertRaises(Exception) as context:
                months = self.conn.get_avail_months('wrong', 'also wrong')
                self.assertTrue('Invalid satallite parameter' in context.exception)

        with self.assertRaises(Exception) as context:
                months = self.conn.get_avail_months('g16', 'also wrong')
                self.assertTrue('Invalid satallite parameter' in context.exception)



    # Test valid satellite, invalid sensor param
    def test_get_avail_months2(self):
        with self.assertRaises(Exception) as context:
                months = self.conn.get_avail_months('goes16', 'wrong')
                self.assertTrue('Invalid sensor parameter' in context.exception)

        with self.assertRaises(Exception) as context:
                months = self.conn.get_avail_months('goes17', 'wrong')
                self.assertTrue('Invalid sensor parameter' in context.exception)



    # Test missing year param
    def test_get_avail_months3(self):
        with self.assertRaises(Exception) as context:
            months = self.conn.get_avail_months('goes16', 'abi')
            self.assertTrue('missing 1 required positional argument' in context.exception)

        with self.assertRaises(Exception) as context:
            months = self.conn.get_avail_months('goes16', 'glm')
            self.assertTrue('missing 1 required positional argument' in context.exception)

        with self.assertRaises(Exception) as context:
            months = self.conn.get_avail_months('goes17', 'abi')
            self.assertTrue('missing 1 required positional argument' in context.exception)

        with self.assertRaises(Exception) as context:
            months = self.conn.get_avail_months('goes17', 'glm')
            self.assertTrue('missing 1 required positional argument' in context.exception)




    # Test missing product
    def test_get_avail_months4(self):
        with self.assertRaises(Exception) as context:
            months = self.conn.get_avail_months('goes16', 'abi', '2019')
            self.assertTrue('Missing sector parameter' in context.exception)

        with self.assertRaises(Exception) as context:
            months = self.conn.get_avail_months('goes16', 'abi', '2018')
            self.assertTrue('Missing sector parameter' in context.exception)

        with self.assertRaises(Exception) as context:
            months = self.conn.get_avail_months('goes16', 'abi', '2017')
            self.assertTrue('Missing sector parameter' in context.exception)



    # Test invalid year param
    def test_get_avail_months5(self):
        with self.assertRaises(Exception) as context:
            months = self.conn.get_avail_months('goes16', 'abi', '2005',
                                                product='ABI-L1b-RadC', sector='C')
            self.assertTrue('AWS response is None' in context.exception)



    # Test valid params for abi
    def test_get_avail_months6(self):
        valid_months = [str(x) for x in range(1,13)]
        months = self.conn.get_avail_months('goes16', 'abi', '2018',
                                            product='ABI-L1b-RadC', sector='C')
        self.assertTrue(len(months), 12)
        self.assertTrue(months, valid_months)


        months = self.conn.get_avail_months('goes16', 'abi', '2018',
                                            product='ABI-L2-CMIPC', sector='C')
        self.assertTrue(len(months), 12)
        self.assertTrue(months, valid_months)


        months = self.conn.get_avail_months('goes16', 'abi', '2018',
                                            product='ABI-L2-CMIPM', sector='M1')
        self.assertTrue(len(months), 12)
        self.assertTrue(months, valid_months)


        months = self.conn.get_avail_months('goes16', 'abi', '2019',
                                            product='ABI-L2-CMIPM', sector='M1')
        self.assertTrue(len(months), 8)
        self.assertTrue(months, valid_months[:8])


        months = self.conn.get_avail_months('goes17', 'abi', '2019',
                                            product='ABI-L2-CMIPM', sector='M1')
        self.assertTrue(len(months), 8)
        self.assertTrue(months, valid_months[:8])



    # Test valid params for goes16 glm
    def test_get_avail_months7(self):
        valid_months = [str(x) for x in range(1,13)]
        months = self.conn.get_avail_months('goes16', 'glm', '2018')
        self.assertTrue(len(months), 12)
        self.assertTrue(months, valid_months)


        months = self.conn.get_avail_months('goes16', 'glm', '2018',
                                            product='GLM-L2-LCFA')
        self.assertTrue(len(months), 12)
        self.assertTrue(months, valid_months)


        months = self.conn.get_avail_months('goes16', 'glm', '2019',
                                            product='GLM-L2-LCFA')
        self.assertTrue(len(months), 8)
        self.assertTrue(months, valid_months[:8])



    # Test valid params for goes17 glm
    def test_get_avail_months8(self):
        valid_months = [str(x) for x in range(1,13)]

        months = self.conn.get_avail_months('goes17', 'glm', '2019',
                                            product='GLM-L2-LCFA')
        self.assertTrue(len(months), 8)
        self.assertTrue(months, valid_months[:8])



    ############################# get_avail_days #############################


    # get_avail_months calls get_avail_days, so we can skip much of the error case
    # tests

    # Test abi 2018
    def test_get_avail_days1(self):
        valid_days = ['{:03}'.format(x) for x in range(1, 366)]
        days = self.conn.get_avail_days('goes16', 'abi', '2018',
                                            product='ABI-L2-CMIPM', sector='M1')
        self.assertEqual(len(days), 365)
        self.assertEqual(days, valid_days)


        days = self.conn.get_avail_days('goes16', 'abi', '2018',
                                            product='ABI-L2-CMIPC', sector='C')
        self.assertEqual(len(days), 365)
        self.assertEqual(days, valid_days)


        days = self.conn.get_avail_days('goes16', 'abi', '2018',
                                            product='ABI-L1b-RadM', sector='M1')
        self.assertEqual(len(days), 365)
        self.assertEqual(days, valid_days)


        days = self.conn.get_avail_days('goes16', 'abi', '2018',
                                            product='ABI-L2-CMIPM', sector='M1')
        self.assertEqual(len(days), 365)
        self.assertEqual(days, valid_days)



    # Test abi in 2019
    def test_get_avail_days2(self):
        valid_days = ['{:03}'.format(x) for x in range(1, 245)]
        days = self.conn.get_avail_days('goes16', 'abi', '2019',
                                            product='ABI-L2-CMIPC', sector='C')
        self.assertEqual(len(days), 244)
        self.assertEqual(days, valid_days)


        days = self.conn.get_avail_days('goes16', 'abi', '2019',
                                            product='ABI-L1b-RadM', sector='M1')
        self.assertEqual(len(days), 244)
        self.assertEqual(days, valid_days)


        days = self.conn.get_avail_days('goes16', 'abi', '2019',
                                            product='ABI-L2-CMIPM', sector='M1')
        self.assertEqual(len(days), 244)
        self.assertEqual(days, valid_days)



    # Test glm in 2018
    # Starts at 044 for some reason
    def test_get_avail_days3(self):
        valid_days = ['{:03}'.format(x) for x in range(44, 366)]

        days = self.conn.get_avail_days('goes16', 'glm', '2018')
        self.assertEqual(len(days), 322)
        self.assertEqual(days, valid_days)


        days = self.conn.get_avail_days('goes16', 'glm', '2018', product='GLM-L2-LCFA')
        self.assertEqual(len(days), 322)
        self.assertEqual(days, valid_days)



    # Test glm 2019
    def test_get_avail_days4(self):
        valid_days = ['{:03}'.format(x) for x in range(1, 245)]

        days = self.conn.get_avail_days('goes16', 'glm', '2019')
        self.assertEqual(len(days), 244)
        self.assertEqual(days, valid_days)


        days = self.conn.get_avail_days('goes16', 'glm', '2019', product='GLM-L2-LCFA')
        self.assertEqual(len(days), 244)
        self.assertEqual(days, valid_days)



    ############################# get_avail_hours #############################


    def test_get_avail_hours1(self):
        pass






if __name__ == '__main__':
    unittest.main()
