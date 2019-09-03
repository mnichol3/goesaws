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
    # Likely to fail if current day of year is not updated
    def test_get_avail_days2(self):
        valid_days = ['{:03}'.format(x) for x in range(1, 247)]
        days = self.conn.get_avail_days('goes16', 'abi', '2019',
                                            product='ABI-L2-CMIPC', sector='C')
        self.assertEqual(len(days), 246)
        self.assertEqual(days, valid_days)


        days = self.conn.get_avail_days('goes16', 'abi', '2019',
                                            product='ABI-L1b-RadM', sector='M1')
        self.assertEqual(len(days), 246)
        self.assertEqual(days, valid_days)


        days = self.conn.get_avail_days('goes16', 'abi', '2019',
                                            product='ABI-L2-CMIPM', sector='M1')
        self.assertEqual(len(days), 246)
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
    # Likely to fail if current day of year is not updated
    def test_get_avail_days4(self):
        valid_days = ['{:03}'.format(x) for x in range(1, 247)]

        days = self.conn.get_avail_days('goes16', 'glm', '2019')
        self.assertEqual(len(days), 246)
        self.assertEqual(days, valid_days)


        days = self.conn.get_avail_days('goes16', 'glm', '2019', product='GLM-L2-LCFA')
        self.assertEqual(len(days), 246)
        self.assertEqual(days, valid_days)



    ############################# get_avail_hours #############################

    # Test invalid satellite param
    def test_get_avail_hours1(self):

        with self.assertRaises(Exception) as context:
            hours = self.conn.get_avail_hours('wrong', 'abi', '05-23-2019', product=None, sector=None)
            self.assertTrue('Invalid satellite parameter' in context.exception)

        with self.assertRaises(Exception) as context:
            hours = self.conn.get_avail_hours('g16', 'abi', '05-23-2019', product=None, sector=None)
            self.assertTrue('Invalid satellite parameter' in context.exception)



    # Test invalid sensor param
    def test_get_avail_hours2(self):

        with self.assertRaises(Exception) as context:
            hours = self.conn.get_avail_hours('goes16', 'wrong', '05-23-2019', product=None, sector=None)
            self.assertTrue('Invalid sensor parameter' in context.exception)

        with self.assertRaises(Exception) as context:
            hours = self.conn.get_avail_hours('g16', 'abb', '05-23-2019', product=None, sector=None)
            self.assertTrue('Invalid sensor parameter' in context.exception)



    # Test invalid date parameter
    def test_get_avail_hours3(self):

        with self.assertRaises(Exception) as context:
            hours = self.conn.get_avail_hours('goes16', 'abi', '05232019', product=None, sector=None)
            self.assertTrue('does not match format' in context.exception)



    # Test missing product and/or sector params for ABI
    def test_get_avail_hours4(self):

        with self.assertRaises(Exception) as context:
            hours = self.conn.get_avail_hours('goes16', 'abi', '05-23-2019', product=None, sector=None)
            self.assertTrue('Invalid product and/or sector parameter' in context.exception)


        with self.assertRaises(Exception) as context:
            hours = self.conn.get_avail_hours('goes16', 'abi', '05-23-2019', product='ABI-L1b-RadC', sector=None)
            self.assertTrue('Invalid product and/or sector parameter' in context.exception)


        with self.assertRaises(Exception) as context:
            hours = self.conn.get_avail_hours('goes16', 'abi', '05-23-2019', product=None, sector='M1')
            self.assertTrue('Invalid product and/or sector parameter' in context.exception)



    # Test valid input for ABI for GOES-16 & -17
    def test_get_avail_hours5(self):
        valid_hours = ['{:02}'.format(x) for x in range(0, 24)]

        hours = self.conn.get_avail_hours('goes16', 'abi', '05-23-2019', product='ABI-L1b-RadC', sector='C')
        self.assertEqual(len(hours), 24)
        self.assertEqual(hours, valid_hours)


        hours = self.conn.get_avail_hours('goes16', 'abi', '05-23-2019', product='ABI-L2-CMIPC', sector='C')
        self.assertEqual(len(hours), 24)
        self.assertEqual(hours, valid_hours)


        hours = self.conn.get_avail_hours('goes16', 'abi', '05-23-2019', product='ABI-L2-CMIPM', sector='M1')
        self.assertEqual(len(hours), 24)
        self.assertEqual(hours, valid_hours)


        hours = self.conn.get_avail_hours('goes17', 'abi', '05-23-2019', product='ABI-L2-CMIPC', sector='C')
        self.assertEqual(len(hours), 24)
        self.assertEqual(hours, valid_hours)


        hours = self.conn.get_avail_hours('goes17', 'abi', '05-23-2019', product='ABI-L1b-RadC', sector='C')
        self.assertEqual(len(hours), 24)
        self.assertEqual(hours, valid_hours)


        hours = self.conn.get_avail_hours('goes17', 'abi', '05-23-2019', product='ABI-L1b-RadM', sector='M1')
        self.assertEqual(len(hours), 24)
        self.assertEqual(hours, valid_hours)



    # Test valid input for GLM for GOES-16 & -17
    def test_get_avail_hours6(self):
        valid_hours = ['{:02}'.format(x) for x in range(0, 24)]

        hours = self.conn.get_avail_hours('goes16', 'glm', '05-23-2019')
        self.assertEqual(len(hours), 24)
        self.assertEqual(hours, valid_hours)


        hours = self.conn.get_avail_hours('goes16', 'glm', '05-25-2019')
        self.assertEqual(len(hours), 24)
        self.assertEqual(hours, valid_hours)


        hours = self.conn.get_avail_hours('goes17', 'glm', '05-25-2019')
        self.assertEqual(len(hours), 24)
        self.assertEqual(hours, valid_hours)


        hours = self.conn.get_avail_hours('goes17', 'glm', '06-16-2019')
        self.assertEqual(len(hours), 24)
        self.assertEqual(hours, valid_hours)



    ############################# get_avail_images #############################


    # Test invalid satellite param
    def test_get_avail_images1(self):
        with self.assertRaises(Exception) as context:
            images = self.conn.get_avail_images('wrong', 'abi', '05-23-2019',
                                                product=None, sector=None, channel=None)
            self.assertTrue('Invalid satellite parameter' in context.exception)


        with self.assertRaises(Exception) as context:
            images = self.conn.get_avail_images('wrong', 'glm', '05-23-2019',
                                                product=None, sector=None, channel=None)
            self.assertTrue('Invalid satellite parameter' in context.exception)


        with self.assertRaises(Exception) as context:
            images = self.conn.get_avail_images('g16', 'abi', '05-23-2019',
                                                product=None, sector=None, channel=None)
            self.assertTrue('Invalid satellite parameter' in context.exception)


        with self.assertRaises(Exception) as context:
            images = self.conn.get_avail_images('g17', 'glm', '05-23-2019',
                                                product=None, sector=None, channel=None)
            self.assertTrue('Invalid satellite parameter' in context.exception)



    # Test invalid sensor param
    def test_get_avail_images2(self):
        with self.assertRaises(Exception) as context:
            images = self.conn.get_avail_images('goes16', 'wrong', '05-23-2019',
                                                product=None, sector=None, channel=None)
            self.assertTrue('Invalid sensor parameter' in context.exception)


        with self.assertRaises(Exception) as context:
            images = self.conn.get_avail_images('goes16', 'abb', '05-23-2019',
                                                product=None, sector=None, channel=None)
            self.assertTrue('Invalid sensor parameter' in context.exception)


        with self.assertRaises(Exception) as context:
            images = self.conn.get_avail_images('goes16', 'gim', '05-23-2019',
                                                product=None, sector=None, channel=None)
            self.assertTrue('Invalid sensor parameter' in context.exception)



    # Test invalid sector param for ABI
    def test_get_avail_images3(self):
        with self.assertRaises(Exception) as context:
            images = self.conn.get_avail_images('goes16', 'abi', '05-23-2019-12',
                                                product='ABI-L1b-RadC', sector=None,
                                                channel=None)
            self.assertTrue('Must provide sector parameter' in context.exception)


        with self.assertRaises(Exception) as context:
            images = self.conn.get_avail_images('goes16', 'abi', '05-23-2019-12',
                                                product='ABI-L1b-RadC', sector='M3',
                                                channel=None)
            self.assertTrue('Must provide sector parameter' in context.exception)



    # Test invalid product params
    def test_get_avail_images4(self):
        with self.assertRaises(Exception) as context:
            images = self.conn.get_avail_images('goes16', 'abi', '05-23-2019-12',
                                                product='ABI-L1-RadC', sector='C',
                                                channel='13')
            self.assertTrue('Invalid product parameter' in context.exception)


        with self.assertRaises(Exception) as context:
            images = self.conn.get_avail_images('goes16', 'abi', '05-23-2019-12',
                                                product='ABI-L1c-RadC', sector='C',
                                                channel='13')
            self.assertTrue('Invalid product parameter' in context.exception)


        with self.assertRaises(Exception) as context:
            images = self.conn.get_avail_images('goes16', 'abi', '05-23-2019-12',
                                                product='ABI-L2-RadC', sector='C',
                                                channel='13')
            self.assertTrue('Invalid product parameter' in context.exception)



    # Test valid params for ABI
    def test_get_avail_images5(self):
        scan_times_artificial = ['05-23-2019-12:01', '05-23-2019-12:06', '05-23-2019-12:11',
                                  '05-23-2019-12:16', '05-23-2019-12:21', '05-23-2019-12:26',
                                  '05-23-2019-12:31', '05-23-2019-12:36', '05-23-2019-12:41',
                                  '05-23-2019-12:46', '05-23-2019-12:51', '05-23-2019-12:56']

        images = self.conn.get_avail_images('goes16', 'abi', '05-23-2019-12',
                                            product='ABI-L1b-RadC', sector='C',
                                            channel='13')
        self.assertEqual(len(images), 12)

        scan_times_true = []
        for img in images:
            scan_times_true.append(img.scan_time)

        self.assertEqual(scan_times_true, scan_times_artificial)



    # Test valid params for ABI
    def test_get_avail_images6(self):
        start = datetime.strptime('05-23-2019-12:00', '%m-%d-%Y-%H:%M')
        end = datetime.strptime('05-23-2019-12:59', '%m-%d-%Y-%H:%M')
        scan_times_artificial = [datetime.strftime(x, '%m-%d-%Y-%H:%M') for x in self.conn._datetime_range(start, end)]

        images = self.conn.get_avail_images('goes16', 'abi', '05-23-2019-12',
                                            product='ABI-L1b-RadM', sector='M1',
                                            channel='13')
        self.assertEqual(len(images), 60)

        scan_times_true = []
        for img in images:
            scan_times_true.append(img.scan_time)

        self.assertEqual(scan_times_true, scan_times_artificial)



    # Test valid params for GLM
    def test_get_avail_images7(self):
        start = datetime.strptime('05-23-2019-12:00', '%m-%d-%Y-%H:%M')
        end = datetime.strptime('05-23-2019-12:59', '%m-%d-%Y-%H:%M')
        scan_times_artificial = []
        for t in self.conn._datetime_range(start, end):
            scan_times_artificial += [datetime.strftime(t, '%m-%d-%Y-%H:%M')] * 3

        images = self.conn.get_avail_images('goes16', 'glm', '05-23-2019-12')

        scan_times_true = []
        for img in images:
            scan_times_true.append(img.scan_time[:-3])

        self.assertEqual(len(images), 180)
        self.assertEqual(scan_times_true, scan_times_artificial)



    ######################### get_avail_images_in_range #########################

    ## Since get_avail_images_in_range calls get_avail_images, we can skip many
    ## of the error cases


    # Test invalid start/end params
    def test_get_avail_images_in_range1(self):
        with self.assertRaises(Exception) as context:
            images = self.conn.get_avail_images_in_range('goes16', 'abi',
                                                         '05232019-12', '05232019-13',
                                                         product=None,
                                                         sector=None, channel=None)
            self.assertTrue('does not match format' in context.exception)


        with self.assertRaises(Exception) as context:
            images = self.conn.get_avail_images_in_range('goes16', 'abi',
                                                         '05-23-2019-12',
                                                         '05-23-2019-13',
                                                         product=None,
                                                         sector=None, channel=None)
            self.assertTrue('does not match format' in context.exception)



    # Test invalid product param
    def test_get_avail_images_in_range2(self):

        with self.assertRaises(Exception) as context:
            images = self.conn.get_avail_images_in_range('goes16', 'abi',
                                                         '05-23-2019-12:00',
                                                         '05-23-2019-12:10',
                                                         product='wrong',
                                                         sector='M1', channel='3')
            self.assertTrue('Invalid product parameter' in context.exception)


        with self.assertRaises(Exception) as context:
            images = self.conn.get_avail_images_in_range('goes16', 'abi',
                                                         '05-23-2019-12:00',
                                                         '05-23-2019-12:10',
                                                         product='ABI-L1-RadM',
                                                         sector='M1', channel='3')
            self.assertTrue('Invalid product parameter' in context.exception)


        with self.assertRaises(Exception) as context:
            images = self.conn.get_avail_images_in_range('goes16', 'abi',
                                                         '05-23-2019-12:00',
                                                         '05-23-2019-12:10',
                                                         product='ABI-L2-CMIIPM',
                                                         sector='M1', channel='3')
            self.assertTrue('Invalid product parameter' in context.exception)



    # Test valid params for ABI
    def test_get_avail_images_in_range3(self):
        start = datetime.strptime('05-23-2019-12:00', '%m-%d-%Y-%H:%M')
        end = datetime.strptime('05-23-2019-12:10', '%m-%d-%Y-%H:%M')
        scan_times_artificial = [datetime.strftime(x, '%m-%d-%Y-%H:%M') for x in self.conn._datetime_range(start, end)]

        images = self.conn.get_avail_images_in_range('goes16', 'abi',
                                                     '05-23-2019-12:00',
                                                     '05-23-2019-12:10',
                                                     product='ABI-L2-CMIPM',
                                                     sector='M1', channel='3')

        scan_times_true = []
        for img in images:
            scan_times_true.append(img.scan_time)

        self.assertEqual(len(images), 11)
        self.assertEqual(scan_times_artificial, scan_times_true)



    # Test valid params for ABI
    def test_get_avail_images_in_range4(self):
        start = datetime.strptime('05-23-2019-12:00', '%m-%d-%Y-%H:%M')
        end = datetime.strptime('05-23-2019-12:59', '%m-%d-%Y-%H:%M')
        scan_times_artificial = [datetime.strftime(x, '%m-%d-%Y-%H:%M') for x in self.conn._datetime_range(start, end)]

        images = self.conn.get_avail_images_in_range('goes16', 'abi',
                                                     '05-23-2019-12:00',
                                                     '05-23-2019-12:59',
                                                     product='ABI-L2-CMIPM',
                                                     sector='M1', channel='3')

        scan_times_true = []
        for img in images:
            scan_times_true.append(img.scan_time)

        self.assertEqual(len(images), 60)
        self.assertEqual(scan_times_artificial, scan_times_true)



    # Test valid params for GLM
    # length = (3 * (t1 - t0 + 1)) + 1
    def test_get_avail_images_in_range5(self):
        start = datetime.strptime('05-23-2019-12:00', '%m-%d-%Y-%H:%M')
        end = datetime.strptime('05-23-2019-12:10', '%m-%d-%Y-%H:%M')
        scan_times_artificial = []
        for t in self.conn._datetime_range(start, end):
            scan_times_artificial += [datetime.strftime(t, '%m-%d-%Y-%H:%M')] * 3
        scan_times_artificial.append('05-23-2019-12:11')

        images = self.conn.get_avail_images_in_range('goes16', 'glm',
                                                     '05-23-2019-12:00',
                                                     '05-23-2019-12:10'
                                                     )

        scan_times_true = []
        for img in images:
            scan_times_true.append(img.scan_time[:-3])

        self.assertEqual(len(images),  self.conn._calc_num_glm_files(10))
        self.assertEqual(scan_times_artificial, scan_times_true)



    # Test valid params for GLM
    # length = (3 * (t1 - t0 + 1)) + 1
    def test_get_avail_images_in_range6(self):
        start = datetime.strptime('05-23-2019-12:00', '%m-%d-%Y-%H:%M')
        end = datetime.strptime('05-23-2019-12:59', '%m-%d-%Y-%H:%M')
        scan_times_artificial = []
        for t in self.conn._datetime_range(start, end):
            scan_times_artificial += [datetime.strftime(t, '%m-%d-%Y-%H:%M')] * 3
        scan_times_artificial.append('05-23-2019-13:00')

        images = self.conn.get_avail_images_in_range('goes16', 'glm',
                                                     '05-23-2019-12:00',
                                                     '05-23-2019-12:59'
                                                     )

        scan_times_true = []
        for img in images:
            scan_times_true.append(img.scan_time[:-3])

        self.assertEqual(len(images), self.conn._calc_num_glm_files(59))
        self.assertEqual(scan_times_artificial, scan_times_true)



    # Test valid params for GLM
    # length = (3 * (num_mins + 1)) + 1
    def test_get_avail_images_in_range7(self):
        start = datetime.strptime('05-23-2019-12:00', '%m-%d-%Y-%H:%M')
        end = datetime.strptime('05-23-2019-14:00', '%m-%d-%Y-%H:%M')
        scan_times_artificial = []
        for t in self.conn._datetime_range(start, end):
            scan_times_artificial += [datetime.strftime(t, '%m-%d-%Y-%H:%M')] * 3
        scan_times_artificial.append('05-23-2019-14:01')

        images = self.conn.get_avail_images_in_range('goes16', 'glm',
                                                     '05-23-2019-12:00',
                                                     '05-23-2019-14:00'
                                                     )

        scan_times_true = []
        for img in images:
            scan_times_true.append(img.scan_time[:-3])

        self.assertEqual(len(images), self.conn._calc_num_glm_files(120))
        self.assertEqual(scan_times_artificial, scan_times_true)






    def test_validate_product1(self):
        output = self.conn._validate_product('ABI-L1b-RadC')
        self.assertTrue(output)

        output = self.conn._validate_product('ABI-L1b-Rad')
        self.assertTrue(output)

        output = self.conn._validate_product('ABI-L2-CMIPM')
        self.assertTrue(output)

        output = self.conn._validate_product('ABI-L2-CMIPC')
        self.assertTrue(output)

        output = self.conn._validate_product('ABI-L2-CMIP')
        self.assertTrue(output)

        output = self.conn._validate_product('GLM-L2-LCFA')
        self.assertTrue(output)


if __name__ == '__main__':
    unittest.main()
