from datetime import datetime
import unittest
import warnings
import sys

import pytz  # Unneeded?

sys.path.insert(1, '../goesaws')
import goesawsinterface


class TestGoesAwsInterface(unittest.TestCase):
    def setUp(self):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        self.conn = goesawsinterface.GoesAWSInterface()



    ########################### get_avail_products #############################

    def test_get_avail_products1(self):
        """
        Invalid satellite params raise exceptions
        """
        with self.assertRaises(Exception) as context:
                prods = self.conn.get_avail_products('wrong', sensor=None)
                self.assertTrue('Invalid satallite parameter' in context.exception)

        with self.assertRaises(Exception) as context:
                prods = conn.get_avail_products('wrong', sensor='glm')
                self.assertTrue('Invalid satallite parameter' in context.exception)

        with self.assertRaises(Exception) as context:
                prods = self.conn.get_avail_products('g16', sensor=None)
                self.assertTrue('Invalid satallite parameter' in context.exception)
    # --------------------------------------------------------------------------

    def test_get_avail_products2(self):
        """
        GLM products
        """
        prods = self.conn.get_avail_products('goes16', sensor='glm')
        self.assertEqual(len(prods), 1)
        self.assertEqual(prods, ['GLM-L2-LCFA'])

        prods = self.conn.get_avail_products('goes17', sensor='glm')
        self.assertEqual(len(prods), 1)
        self.assertEqual(prods, ['GLM-L2-LCFA'])
    # --------------------------------------------------------------------------

    def test_get_avail_products2(self):
        """
        ABI products
        """
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
    # --------------------------------------------------------------------------

    ############################ get_avail_years ###############################
    def test_get_avail_years1(self):
        """
        get_avail_years; invalid satellite parameter raises error
        """
        with self.assertRaises(Exception) as context:
                years = self.conn.get_avail_years('wrong', 'also wrong')
                self.assertTrue('Invalid satallite parameter' in context.exception)
        with self.assertRaises(Exception) as context:
                years = self.conn.get_avail_years('g16', 'also wrong')
                self.assertTrue('Invalid satallite parameter' in context.exception)
    # --------------------------------------------------------------------------

    def test_get_avail_years2(self):
        """
        get_avail_years; invalid sensor parameter raises error
        """
        with self.assertRaises(Exception) as context:
                years = self.conn.get_avail_years('goes16', 'wrong')
                self.assertTrue('Invalid sensor parameter' in context.exception)
        with self.assertRaises(Exception) as context:
                years = self.conn.get_avail_years('goes17', 'wrong')
                self.assertTrue('Invalid sensor parameter' in context.exception)
    # --------------------------------------------------------------------------

    def test_get_avail_years3(self):
        """
        get_avail_years; missing sector & product parameters
        """
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
    # --------------------------------------------------------------------------

    def test_get_avail_years4(self):
        """
        get_avail_years; valid params
        """
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
    # --------------------------------------------------------------------------

    ############################ get_avail_months ##############################
    def test_get_avail_months1(self):
        """
        get_avail_months; invalid satellite param raises error
        """
        with self.assertRaises(Exception) as context:
                months = self.conn.get_avail_months('wrong', 'also wrong')
                self.assertTrue('Invalid satallite parameter' in context.exception)
        with self.assertRaises(Exception) as context:
                months = self.conn.get_avail_months('g16', 'also wrong')
                self.assertTrue('Invalid satallite parameter' in context.exception)
    # --------------------------------------------------------------------------

    def test_get_avail_months2(self):
        """
        get_avail_months; valid satellite param and invalid sensor param
        """
        with self.assertRaises(Exception) as context:
                months = self.conn.get_avail_months('goes16', 'wrong')
                self.assertTrue('Invalid sensor parameter' in context.exception)
        with self.assertRaises(Exception) as context:
                months = self.conn.get_avail_months('goes17', 'wrong')
                self.assertTrue('Invalid sensor parameter' in context.exception)
    # --------------------------------------------------------------------------

    def test_get_avail_months3(self):
        """
        get_avail_months; missing year param raises error
        """
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
    # --------------------------------------------------------------------------

    def test_get_avail_months4(self):
        """
        get_avail_months; missing prodct param raises error
        """
        with self.assertRaises(Exception) as context:
            months = self.conn.get_avail_months('goes16', 'abi', '2019')
            self.assertTrue('Missing sector parameter' in context.exception)
        with self.assertRaises(Exception) as context:
            months = self.conn.get_avail_months('goes16', 'abi', '2018')
            self.assertTrue('Missing sector parameter' in context.exception)
        with self.assertRaises(Exception) as context:
            months = self.conn.get_avail_months('goes16', 'abi', '2017')
            self.assertTrue('Missing sector parameter' in context.exception)
    # --------------------------------------------------------------------------

    def test_get_avail_months5(self):
        """
        get_avail_months; invalid year param raises error
        """
        with self.assertRaises(Exception) as context:
            months = self.conn.get_avail_months('goes16', 'abi', '2005',
                                                product='ABI-L1b-RadC', sector='C')
            self.assertTrue('AWS response is None' in context.exception)
    # --------------------------------------------------------------------------

    def test_get_avail_months6(self):
        """
        get_avail_months; valid ABI cases
        """
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
    # --------------------------------------------------------------------------

    def test_get_avail_months7(self):
        """
        get_avail_months; valid GOES-16 GLM cases
        """
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
    # --------------------------------------------------------------------------

    def test_get_avail_months8(self):
        """
        get_avail_months; valid GOES-17 GLM cases
        """
        valid_months = [str(x) for x in range(1,13)]
        months = self.conn.get_avail_months('goes17', 'glm', '2019',
                                            product='GLM-L2-LCFA')
        self.assertTrue(len(months), 8)
        self.assertTrue(months, valid_months[:8])
    # --------------------------------------------------------------------------

    ############################# get_avail_days #############################

    def test_get_avail_days1(self):
        """
        get_avail_days; test ABI 2018 cases
        """
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
    # --------------------------------------------------------------------------

    def test_get_avail_days2(self):
        """
        get_avail_days; test ABI 2019 cases
        """
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
    # --------------------------------------------------------------------------

    def test_get_avail_days3(self):
        """
        get_avail_days; test GLM 2018 cases
        Starts at 044 for some reason
        """
        valid_days = ['{:03}'.format(x) for x in range(44, 366)]

        days = self.conn.get_avail_days('goes16', 'glm', '2018')
        self.assertEqual(len(days), 322)
        self.assertEqual(days, valid_days)

        days = self.conn.get_avail_days('goes16', 'glm', '2018', product='GLM-L2-LCFA')
        self.assertEqual(len(days), 322)
        self.assertEqual(days, valid_days)
    # --------------------------------------------------------------------------

    def test_get_avail_days4(self):
        """
        get_avail_days; test GLM 2019 cases
        """
        valid_days = ['{:03}'.format(x) for x in range(1, 247)]

        days = self.conn.get_avail_days('goes16', 'glm', '2019')
        self.assertEqual(len(days), 246)
        self.assertEqual(days, valid_days)

        days = self.conn.get_avail_days('goes16', 'glm', '2019', product='GLM-L2-LCFA')
        self.assertEqual(len(days), 246)
        self.assertEqual(days, valid_days)
    # --------------------------------------------------------------------------

    ############################# get_avail_hours #############################

    def test_get_avail_hours1(self):
        """
        get_avail_hours; invalid satellite param raises error
        """
        with self.assertRaises(Exception) as context:
            hours = self.conn.get_avail_hours('wrong', 'abi', '05-23-2019', product=None, sector=None)
            self.assertTrue('Invalid satellite parameter' in context.exception)

        with self.assertRaises(Exception) as context:
            hours = self.conn.get_avail_hours('g16', 'abi', '05-23-2019', product=None, sector=None)
            self.assertTrue('Invalid satellite parameter' in context.exception)
    # --------------------------------------------------------------------------

    def test_get_avail_hours2(self):
        """
        get_avail_hours; invalid sensor param raises error
        """
        with self.assertRaises(Exception) as context:
            hours = self.conn.get_avail_hours('goes16', 'wrong', '05-23-2019', product=None, sector=None)
            self.assertTrue('Invalid sensor parameter' in context.exception)

        with self.assertRaises(Exception) as context:
            hours = self.conn.get_avail_hours('g16', 'abb', '05-23-2019', product=None, sector=None)
            self.assertTrue('Invalid sensor parameter' in context.exception)
    # --------------------------------------------------------------------------

    def test_get_avail_hours3(self):
        """
        get_avail_hours; invalid date param raises error
        """
        with self.assertRaises(Exception) as context:
            hours = self.conn.get_avail_hours('goes16', 'abi', '05232019', product=None, sector=None)
            self.assertTrue('does not match format' in context.exception)
    # --------------------------------------------------------------------------

    # Test missing product and/or sector params for ABI
    def test_get_avail_hours4(self):
        """
        get_avail_hours; invalid/missing product and/or sector param for ABI raises error
        """
        with self.assertRaises(Exception) as context:
            hours = self.conn.get_avail_hours('goes16', 'abi', '05-23-2019', product=None, sector=None)
            self.assertTrue('Invalid product and/or sector parameter' in context.exception)


        with self.assertRaises(Exception) as context:
            hours = self.conn.get_avail_hours('goes16', 'abi', '05-23-2019', product='ABI-L1b-RadC', sector=None)
            self.assertTrue('Invalid product and/or sector parameter' in context.exception)


        with self.assertRaises(Exception) as context:
            hours = self.conn.get_avail_hours('goes16', 'abi', '05-23-2019', product=None, sector='M1')
            self.assertTrue('Invalid product and/or sector parameter' in context.exception)
    # --------------------------------------------------------------------------

    def test_get_avail_hours5(self):
        """
        get_avail_hours; valid cases for GOES-16 & GOES-17 ABI
        """
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
    # --------------------------------------------------------------------------

    def test_get_avail_hours6(self):
        """
        get_avail_hours; valid cases for GOES-16 & GOES-17 GLM
        """
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
    # --------------------------------------------------------------------------

    ############################# get_avail_images #############################

    def test_get_avail_images1(self):
        """
        get_avail_images; invalid satellite param raises error
        """
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
    # --------------------------------------------------------------------------

    def test_get_avail_images2(self):
        """
        get_avail_images; invalid sensor param raises error
        """
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
    # --------------------------------------------------------------------------

    def test_get_avail_images3(self):
        """
        get_avail_images; invalid sector param raises error
        """
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
    # --------------------------------------------------------------------------

    def test_get_avail_images4(self):
        """
        get_avail_images; invalid product param raises error
        """
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
    # --------------------------------------------------------------------------

    def test_get_avail_images5(self):
        """
        get_avail_images; valid GOES-16 ABI cases
        """
        scan_times_artificial = ['05-23-2019-12:01', '05-23-2019-12:06', '05-23-2019-12:11',
                                  '05-23-2019-12:16', '05-23-2019-12:21', '05-23-2019-12:26',
                                  '05-23-2019-12:31', '05-23-2019-12:36', '05-23-2019-12:41',
                                  '05-23-2019-12:46', '05-23-2019-12:51', '05-23-2019-12:56']

        images = self.conn.get_avail_images('goes16', 'abi', '05-23-2019-12',
                                            product='RadC', sector='C',
                                            channel='13')
        self.assertEqual(len(images), 12)
        scan_times_true = []
        for img in images:
            scan_times_true.append(img.scan_time)
        self.assertEqual(scan_times_true, scan_times_artificial)
    # --------------------------------------------------------------------------

    def test_get_avail_images6(self):
        """
        get_avail_images; valid GOES-16 ABI cases
        """
        start = datetime.strptime('05-23-2019-12:00', '%m-%d-%Y-%H:%M')
        end = datetime.strptime('05-23-2019-12:59', '%m-%d-%Y-%H:%M')
        scan_times_artificial = [datetime.strftime(x, '%m-%d-%Y-%H:%M') for x in self.conn._datetime_range(start, end)]

        images = self.conn.get_avail_images('goes16', 'abi', '05-23-2019-12',
                                            product='RadM', sector='M1',
                                            channel='13')
        self.assertEqual(len(images), 60)
        scan_times_true = []
        for img in images:
            scan_times_true.append(img.scan_time)
        self.assertEqual(scan_times_true, scan_times_artificial)
    # --------------------------------------------------------------------------

    def test_get_avail_images7(self):
        """
        get_avail_images; valid GOES-16 GLM cases
        """
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
    # --------------------------------------------------------------------------

    ######################### get_avail_images_in_range #########################

    def test_get_avail_images_in_range1(self):
        """
        get_avail_images_in_range; invalid start/end params raise errors
        """
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
    # --------------------------------------------------------------------------

    def test_get_avail_images_in_range2(self):
        """
        get_avail_images_in_range; invalid product param raises error
        """
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
    # --------------------------------------------------------------------------

    def test_get_avail_images_in_range3(self):
        """
        get_avail_images_in_range; valid GOES-16 ABI cases
        """
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
    # --------------------------------------------------------------------------

    def test_get_avail_images_in_range4(self):
        """
        get_avail_images_in_range; valid GOES-16 ABI cases
        """
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
    # --------------------------------------------------------------------------

    def test_get_avail_images_in_range5(self):
        """
        get_avail_images_in_range; valid GOES-16 GLM cases

        length = (3 * (t1 - t0 + 1)) + 1
        """
        start = datetime.strptime('05-23-2019-12:00', '%m-%d-%Y-%H:%M')
        end = datetime.strptime('05-23-2019-12:10', '%m-%d-%Y-%H:%M')
        scan_times_artificial = []
        for t in self.conn._datetime_range(start, end):
            scan_times_artificial += [datetime.strftime(t, '%m-%d-%Y-%H:%M')] * 3
        scan_times_artificial.append('05-23-2019-12:11')
        images = self.conn.get_avail_images_in_range('goes16', 'glm',
                                                     '05-23-2019-12:00',
                                                     '05-23-2019-12:10')
        scan_times_true = []
        for img in images:
            scan_times_true.append(img.scan_time[:-3])
        self.assertEqual(len(images),  self.conn._calc_num_glm_files(10))
        self.assertEqual(scan_times_artificial, scan_times_true)
    # --------------------------------------------------------------------------

    def test_get_avail_images_in_range6(self):
        """
        get_avail_images_in_range; valid GOES-16 GLM cases

        length = (3 * (t1 - t0 + 1)) + 1
        """
        start = datetime.strptime('05-23-2019-12:00', '%m-%d-%Y-%H:%M')
        end = datetime.strptime('05-23-2019-12:59', '%m-%d-%Y-%H:%M')
        scan_times_artificial = []
        for t in self.conn._datetime_range(start, end):
            scan_times_artificial += [datetime.strftime(t, '%m-%d-%Y-%H:%M')] * 3
        scan_times_artificial.append('05-23-2019-13:00')
        images = self.conn.get_avail_images_in_range('goes16', 'glm',
                                                     '05-23-2019-12:00',
                                                     '05-23-2019-12:59')
        scan_times_true = []
        for img in images:
            scan_times_true.append(img.scan_time[:-3])
        self.assertEqual(len(images), self.conn._calc_num_glm_files(59))
        self.assertEqual(scan_times_artificial, scan_times_true)
    # --------------------------------------------------------------------------

    def test_get_avail_images_in_range7(self):
        """
        get_avail_images_in_range; valid GOES-16 GLM cases

        length = (3 * (t1 - t0 + 1)) + 1
        """
        start = datetime.strptime('05-23-2019-12:00', '%m-%d-%Y-%H:%M')
        end = datetime.strptime('05-23-2019-14:00', '%m-%d-%Y-%H:%M')
        scan_times_artificial = []
        for t in self.conn._datetime_range(start, end):
            scan_times_artificial += [datetime.strftime(t, '%m-%d-%Y-%H:%M')] * 3
        scan_times_artificial.append('05-23-2019-14:01')
        images = self.conn.get_avail_images_in_range('goes16', 'glm',
                                                     '05-23-2019-12:00',
                                                     '05-23-2019-14:00')
        scan_times_true = []
        for img in images:
            scan_times_true.append(img.scan_time[:-3])
        self.assertEqual(len(images), self.conn._calc_num_glm_files(120))
        self.assertEqual(scan_times_artificial, scan_times_true)
    # --------------------------------------------------------------------------

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
    # --------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
