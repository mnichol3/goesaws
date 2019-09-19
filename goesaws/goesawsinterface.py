"""
Author: Matt Nicholson

This file contains functions for the goesaws NOAA Amazon Web Services
object-oriented interface. It allows GOES-16 & -17 imagery files hosted on NOAA's
AWS bucket to be easily and quickly found, downloaded, and processed.

For example usage, see ReadMe
https://github.com/mnichol3/goesaws

For more information on NOAA's Amazon S3 bucket, see:
https://docs.opendata.aws/noaa-goes16/cics-readme.html

Notes
-----

* 16 Sep 2019
    - Valid ABI products:
        - Without sector suffix:
            'ABI-L1b-Rad', 'ABI-L2-CMIP', 'ABI-L2-FDC', 'ABI-L2-MCMIP'
        - With sector suffix:
            'ABI-L1b-RadC', 'ABI-L1b-RadF', 'ABI-L1b-RadM',
            'ABI-L2-CMIPC', 'ABI-L2-CMIPF', 'ABI-L2-CMIPM',
            'ABI-L2-FDCC', 'ABI-L2-FDCF', 'ABI-L2-MCMIPC',
            'ABI-L2-MCMIPF', 'ABI-L2-MCMIPM'
"""
import os
import re
import sys
from datetime import timedelta, datetime

import logging

import boto3
import errno
import pytz
import six
from botocore.handlers import disable_signing
import concurrent.futures

from awsgoesfile import AwsGoesFile
from downloadresults import DownloadResults
from localgoesfile import LocalGoesFile

class GoesAWSInterface(object):
    """
    Instantiate an instance of this class to get a connection to the GOES AWS bucket.
    This class provides methods to query for various metadata of the AWS bucket as well
    as download files.
    >>> import goesaws
    >>> conn = goesaws.GoesAwsInterface()
    """
    try:
        os.remove('error.log')
    except OSError:
        pass

    logging.basicConfig(filename='error.log', level=logging.INFO,
                        format='%(levelname)s: %(asctime)s: %(module)s.%(funcName)s, line %(lineno)d:\n\t%(message)s',
                        filemode='w')


    def __init__(self):
        super(GoesAWSInterface, self).__init__()
        self._year_re = re.compile(r'/(\d{4})/')
        self._day_re = re.compile(r'/\d{4}/(\d{3})/')
        self._hour_re = re.compile(r'/\d{4}/\d{3}/(\d{2})/')
        self._scan_m_re = re.compile(r'(\w{3,4}M\d-M\dC\d{2})_G\d{2}_s\d{7}(\d{4})\d{3}')
        self._scan_c_re = re.compile(r'(\w{4,5}-M\dC\d{2})_G\d{2}_s\d{7}(\d{4})\d{3}')
        self._scan_re_glm = re.compile(r'(OR_GLM-L2-LCFA)_G\d{2}_s\d{7}(\d{6})\d{1}')
        self._scan_re_mcmip_m = re.compile(r'(\w{3,4}M\d-M\d)_G\d{2}_s\d{7}(\d{4})\d{3}')
        self._scan_re_mcmip_c = re.compile(r'(\w{4,5}-M\d)_G\d{2}_s\d{7}(\d{4})\d{3}')
        self._s3conn = boto3.resource('s3')
        self._s3conn.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
        self._bucket_16 = self._s3conn.Bucket('noaa-goes16')
        self._bucket_17 = self._s3conn.Bucket('noaa-goes17')



    def get_avail_products(self, satellite, sensor=None):
        """
        Gets a list of available products (Rad, CMIP, MCMIP) for a satellite

        Parameters
        ----------
        satellite : str
            The satellite to fetch available products for.
            Valid: 'goes16' & 'goes17'
        sensor : str, optional
            Sensor that produced the data. Valid: 'abi' or 'glm'. Default = None

        Returns
        -------
        prods : list of str
            List of available products

        Notes
        -----
        - 29 AUG 2019
            - GLM L2 LCFA product hard-coded
        """
        prods = []

        if (sensor == 'glm'):
            # resp = self._get_sat_bucket(satellite, '')
            #
            # for x in resp.get('CommonPrefixes'):
            #     if ('GLM' in x['Prefix']):
            #         prods.append(x['Prefix'][:-1])
            prods.append('GLM-L2-LCFA')
        else:
            resp = self._get_sat_bucket(satellite, '')

            if (sensor == 'abi'):
                for x in resp.get('CommonPrefixes'):
                    if ('ABI' in x['Prefix']):
                        prods.append(x['Prefix'][:-1])
            elif (sensor is None):
                for x in resp.get('CommonPrefixes'):
                    prods.append(x['Prefix'][:-1])
            else:
                logger = logging.getLogger(__name__)
                logger.error("Invalid sensor parameter %s", sensor)
                raise ValueError("Invalid sensor parameter. Must be 'abi', 'glm', or None")

        return prods



    def get_avail_years(self, satellite, sensor, product=None, sector=None):
        """
        Gets the years for which data is available for a given satellite & product

        Parameters
        ----------
        satellite : str
            The satellite to fetch available products for.
            Valid: 'goes16' & 'goes17'
        sensor : str
            Sensor that produced the data. Valid: 'abi' or 'glm'
        product : str, optional
            Imagery product. Required when pulling ABI data. Default: None
        sector : str, optional
            Satellite scan sector. M1 = mesoscale 1, M2 = mesoscale 2, C = CONUS
            Required to pull ABI data. Default = None

        Returns
        -------
        years : list of str
            List containing the years for which data is available for the given
            satellite and product
        """
        years = []

        if (sensor == 'abi'):
            prefix = self._build_prefix_abi(product=product, sector=sector)
            # if (product is None or sector is None):
            #     print('Warning: product/sector parameter is NoneType')
        elif (sensor == 'glm'):
            prefix = self._build_prefix_glm()
        else:
            logger = logging.getLogger(__name__)
            logger.error("Invalid sensor parameter %s", sensor)
            raise ValueError("Invalid sensor parameter. Must be 'abi' or 'glm'")

        resp = self._get_sat_bucket(satellite, prefix)

        if (resp.get('CommonPrefixes') is None):
            logger = logging.getLogger(__name__)
            logger.error("AWS response is None. Product: {}, Sector: {}, Prefix: {}".format(
                    product, sector, prefix))
            raise TypeError('AWS response is None. Ensure product & sector params are valid')

        for each in resp.get('CommonPrefixes'):
            match = self._year_re.search(each['Prefix'])
            if (match is not None):
                years.append(match.group(1))

        return years



    def get_avail_months(self, satellite, sensor, year, product=None, sector=None):
        """
        Gets the months for which data is available for a given satellite, product,
        and year

        Parameters
        ----------
        satellite : str
            The satellite to fetch available products for.
            Valid: 'goes16' & 'goes17'
        sensor : str
            Sensor that produced the data. Valid: 'abi' or 'glm'
        year : str or int
            Year to fetch the available months for
        product : str, optional
            Imagery product. Required when pulling ABI data. Default: None
        sector : str, optional
            Satellite scan sector. M1 = mesoscale 1, M2 = mesoscale 2, C = CONUS
            Required to pull ABI data. Default = None

        Returns
        -------
        months : list of int
            List of months for which data is available
        """

        days = self.get_avail_days(satellite, sensor, year, product, sector)
        months = self._decode_julian_day(year, days, 'm')

        return months



    def get_avail_days(self, satellite, sensor, year, product=None, sector=None):
        """
        Retrieves the days of the given year for which data is available for the
        given satellite and product

        Parameters
        ----------
        satellite : str
            The satellite to fetch available products for.
            Valid: 'goes16' & 'goes17'
        sensor : str
            Sensor that produced the data. Valid: 'abi' or 'glm'
        year : str or int
            Year to fetch the available months for
        product : str, optional
            Imagery product. Required when pulling ABI data. Default: None
        sector : str, optional
            Satellite scan sector. M1 = mesoscale 1, M2 = mesoscale 2, C = CONUS
            Required to pull ABI data. Default = None

        Returns
        -------
        days : set of str
        """
        days = []

        if (sensor == 'abi'):
            if (sector == None):
                raise ValueError("Missing sector parameter")
            elif (product == None):
                raise ValueError("Missing product parameter")

            prefix = self._build_prefix_abi(product=product, sector=sector, year=year)

        elif (sensor == 'glm'):
            prefix = self._build_prefix_glm(year=year)
        else:
            logger = logging.getLogger(__name__)
            logger.error("Invalid sensor parameter %s", sensor)
            raise ValueError("Invalid sensor parameter. Must be 'abi' or 'glm'")

        resp = self._get_sat_bucket(satellite, prefix)

        if (resp.get('CommonPrefixes') is None):
            logger = logging.getLogger(__name__)
            logger.error("AWS response is None. Product: {}, Sector: {}".format(product, sector))
            raise TypeError('AWS response is None. Ensure product & sector params are valid')

        for each in resp.get('CommonPrefixes'):
            match = self._day_re.search(each['Prefix'])
            if (match is not None):
                days.append(match.group(1))

        return days



    def get_avail_hours(self, satellite, sensor, date, product=None, sector=None):
        """
        Gets the hours that data is available for a given satellite, product,
        and date

        Parameters
        ----------
        satellite : str
            The satellite to fetch available products for.
            Valid: 'goes16' & 'goes17'
        sensor : str
            Sensor that produced the data. Valid: 'abi' or 'glm'
        date : str
            Date of the desired imagery/data.
            Format: MM-DD-YYYY
        product : str, optional
            Imagery product. Required when pulling ABI data. Default: None
        sector : str, optional
            Satellite scan sector. M1 = mesoscale 1, M2 = mesoscale 2, C = CONUS
            Required to pull ABI data. Default = None

        Returns
        -------
        hours : list of int
            Hours for which data is available, in UTC format
        """
        hours = []

        year = date[-4:]
        jul_day = datetime.strptime(date, '%m-%d-%Y').timetuple().tm_yday

        if (sensor == 'abi'):
            if (product is None or sector is None):
                logger = logging.getLogger(__name__)
                logger.error("Invalid product and/or sector parameter (NoneType). Product: {}, Sector: {}".format(product, sector))
                raise ValueError("Invalid product and/or sector parameter (NoneType)")
            else:
                prefix = self._build_prefix_abi(product=product, sector=sector, year=year, julian_day=jul_day)
        elif (sensor == 'glm'):
            prefix = self._build_prefix_glm(year=year, julian_day=jul_day)
        else:
            logger = logging.getLogger(__name__)
            logger.error("Invalid sensor parameter %s", sensor)
            raise ValueError("Invalid sensor parameter. Must be 'abi' or 'glm'")

        resp = self._get_sat_bucket(satellite, prefix)

        if (resp.get('CommonPrefixes') is None):
            logger = logging.getLogger(__name__)
            logger.error("AWS response is None. Product: {}, Sector: {}".format(product, sector))
            raise TypeError('AWS response is None. Ensure product & sector params are valid')

        for each in resp.get('CommonPrefixes'):
            match = self._hour_re.search(each['Prefix'])
            if (match is not None):
                hours.append(match.group(1))

        return hours



    def get_avail_images(self, satellite, sensor, date, product=None, sector=None, channel=None):
        """

        Parameters
        ----------
        satellite : str
            The satellite to fetch available products for.
            Valid: 'goes16' & 'goes17'
        sensor : str
            Which sensor (ABI or GLM) to get data from
            Valid: 'abi' & 'glm'
        product : str, optional
            Imagery product to retrieve available data for. Required to pull ABI
            data
            Default = None
        date : str
            Date & time of the data. Format: MM-DD-YYYY-HH
        sector : str, optional
            Satellite scan sector. M1 = mesoscale 1, M2 = mesoscale 2, C = CONUS
            Required to pull ABI data. Default = None
        channel : int, optional
            ABI channel. Required to pull ABI data. Default = None

        Returns
        -------
        images : list of AwsGoesFile objects
            AwsGoesFile objects representing available data files
        """
        images = []
        abi_sector_dict = {'C': self._scan_c_re,
                           'M1': self._scan_m_re,
                           'M2': self._scan_m_re
        }
        mcmip_sector_dict = {'C': self._scan_re_mcmip_c,
                             'M1': self._scan_re_mcmip_m,
                             'M2': self._scan_re_mcmip_m}

        if (not isinstance(date, datetime)):
            date = datetime.strptime(date, '%m-%d-%Y-%H')

        if (sensor != 'glm' and not self._validate_product(product)):
            raise ValueError('Invalid product parameter')

        year = date.year
        hour = date.hour
        jul_day = date.timetuple().tm_yday

        if (sensor == 'abi'):
            trim_prod = self._trim_product_sector(product)
            try:
                # setting the scan_re variable also acts to validate the sector
                # parameter
                if (trim_prod == 'MCMIP'):
                    scan_re = mcmip_sector_dict[sector]
                else:
                    scan_re = abi_sector_dict[sector]
            except KeyError:
                logger = logging.getLogger(__name__)
                logger.error("Invalid sector parameter %s", sector)
                raise ValueError("Must provide sector parameter ('M1', 'M2', or 'C') when accessing ABI data")

            prefix = self._build_prefix_abi(product=product, year=year, julian_day=jul_day,
                                            hour=hour, sector=sector)

            resp = self._get_sat_bucket(satellite, prefix)

            if ('Contents' not in list(resp.keys())):
                logger = logging.getLogger(__name__)
                logger.error("KeyError: 'Contents' not in AWS response. Product: {}. Sector: {}. Channel: {}", product, sector, channel)
                raise KeyError("'Contents' not in AWS response")

            if (trim_prod == 'MCMIP'):
                for each in list(resp['Contents']):
                    match = scan_re.search(each['Key'])
                    if (match is not None):
                        if (sector in match.group(1)):
                            time = match.group(2)
                            dt = datetime.strptime('{} {} {}'.format(year, jul_day, time), '%Y %j %H%M')
                            dt = dt.strftime('%m-%d-%Y-%H:%M')
                            images.append(AwsGoesFile(each['Key'], '{} {}'.format(match.group(1), dt), dt))
            else:
                for each in list(resp['Contents']):
                    match = scan_re.search(each['Key'])
                    # print(each['Key'])
                    if (match is not None):
                        if (sector in match.group(1) and channel in match.group(1)):
                            time = match.group(2)
                            dt = datetime.strptime('{} {} {}'.format(year, jul_day, time), '%Y %j %H%M')
                            dt = dt.strftime('%m-%d-%Y-%H:%M')
                            images.append(AwsGoesFile(each['Key'], '{} {}'.format(match.group(1), dt), dt))

        elif (sensor == 'glm'):
            scan_re = self._scan_re_glm
            prefix = self._build_prefix_glm(year=year, julian_day=jul_day, hour=hour)

            resp = self._get_sat_bucket(satellite, prefix)

            if ('Contents' not in list(resp.keys())):
                logger = logging.getLogger(__name__)
                logger.error("KeyError: 'Contents' not in AWS response. Product: {}. Sector: {}. Channel: {}", product, sector, channel)
                raise KeyError("'Contents' not in AWS response")

            for each in list(resp['Contents']):

                match = scan_re.search(each['Key'])
                if (match is not None):
                        time = match.group(2)
                        dt = datetime.strptime('{} {} {}'.format(year, jul_day, time), '%Y %j %H%M%S')
                        dt = dt.strftime('%m-%d-%Y-%H:%M:%S')
                        images.append(AwsGoesFile(each['Key'], '{} {}'.format(match.group(1), dt), dt))

        else:
            logger = logging.getLogger(__name__)
            logger.error("Invalid sensor parameter %s", sensor)
            raise ValueError("Invalid sensor parameter, must be 'abi' or 'glm'")

        return images



    def get_avail_images_in_range(self, satellite, sensor, start, end, product=None,
            sector=None, channel=None):
        """

        Parameters
        ----------
        satellite : str
            The satellite to fetch available products for.
            Valid: 'goes16' & 'goes17'
        sensor : str
            Which sensor (ABI or GLM) to get data from
            Valid: 'abi' & 'glm'
        start : str
            Start date & time of the data. Format: MM-DD-YYYY-HH:MM
        end : str
            End date & time of the data. Format: MM-DD-YYYY-HH:MM
        product : str, optional
            Imagery product to retrieve available data for. Required to pull ABI
            data. Default = None
            Valid products: 'ABI-L2-CMIP', 'ABI-L1b-Rad'
        sector : str, optional
            Satellite scan sector. Required to pull ABI data. Default = None
            'M1' = mesoscale 1, 'M2' = mesoscale 2, 'C' = CONUS
        channel : int, optional
            ABI channel. Required to pull ABI data. Default = None

        Returns
        -------
        images : list of AwsGoesFile objects
            AwsGoesFile objects representing available data files between the start
            and end date & times, inclusive

        Notes
        -----
        * To get the most recent file from AWS, the 'end' time param can be set
          for a future time (ex: its currently 1230, end can be set to 1300)
        * To get only one file, 'start' & 'end' can both be set to the time
          of the desired file
        """
        images = []
        added = []

        start_dt = datetime.strptime(start, '%m-%d-%Y-%H:%M')
        end_dt = datetime.strptime(end, '%m-%d-%Y-%H:%M')

        prev_hour = start_dt.hour
        first = True

        if (sensor == 'abi'):

            for day in self._datetime_range(start_dt, end_dt):
                curr_hour = day.hour

                if (prev_hour != curr_hour):
                    first = True

                if (first):
                    first = False
                    # avail_imgs = self.get_avail_images(satellite, sensor, product, day,
                    #                                    sector, channel)
                    avail_imgs = self.get_avail_images(satellite, sensor, day,
                                                       product=product, sector=sector,
                                                       channel=channel)

                    for img in avail_imgs:
                        scan_dt = datetime.strptime(img.scan_time, '%m-%d-%Y-%H:%M')

                        if (self._is_within_range(start_dt, end_dt, scan_dt) == 0):
                            if (img.shortfname not in added):
                                added.append(img.shortfname)
                                images.append(img)
                        elif (self._is_within_range(start_dt, end_dt, scan_dt) == 1):
                            # If the current scan time has surpassed the end
                            # of the desired time span
                            break
                prev_hour = curr_hour

        elif (sensor == 'glm'):

            # Increment the end datetime by 1 minute as the three datafiles for
            # the original end minute technically occur after
            # Ex: end_dt = 21:30, 21:30:20 & 21:30:40 files wouldn't be included
            end_dt += timedelta(minutes=1)

            for day in self._datetime_range(start_dt, end_dt):
                curr_hour = day.hour

                if (prev_hour != curr_hour):
                    first = True

                if (first):
                    first = False
                    avail_imgs = self.get_avail_images(satellite, sensor, day)

                    for img in avail_imgs:
                        scan_dt = datetime.strptime(img.scan_time, '%m-%d-%Y-%H:%M:%S')
                        if (self._is_within_range(start_dt, end_dt, scan_dt) == 0):
                            if (img.shortfname not in added):
                                added.append(img.shortfname)
                                images.append(img)
                        elif (self._is_within_range(start_dt, end_dt, scan_dt) == 1):
                            # If the current scan time has surpassed the end
                            # of the desired time span
                            break
                prev_hour = curr_hour

            # Remove the last file since it contains data from beyond the desired
            # time spand     
            images = images[:-1]
        else:
            logger = logging.getLogger(__name__)
            logger.error("Invalid sensor parameter %s", sensor)
            raise ValueError("Invalid sensor parameter, must be 'abi' or 'glm'")

        return images



    def download(self, satellite, awsgoesfiles, basepath, keep_aws_folders=False, threads=6):
        """
        Downloads GOES data files from the AWS bucket

        Parameters
        ----------
        satellite : str
            The satellite to fetch available products for.
            Valid: 'goes16' & 'goes17'
        awsgoesfiles : list of AwsGoesFile objects
            AwsGoesFile objects to download
        basepath : str
            Path to download the data files to
        keep_aws_folders : bool, optional
            If True, the AWS bucket file structure will be implemented within
            the 'basepath' directory. Default is False
        threads : int, optional
            Number of threads used to download the files. Default is 6

        Returns
        -------
        downloadresults : list of LocalGoesFile objects
            List of LocalGoesFile objects that have been downloaded
        """

        if type(awsgoesfiles) == AwsGoesFile:
            awsgoesfiles = [awsgoesfiles]

        localfiles = []
        errors = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            future_download = {executor.submit(self._download,goesfile,basepath,keep_aws_folders,satellite):
                                            goesfile for goesfile in awsgoesfiles}

            for future in concurrent.futures.as_completed(future_download):
                try:
                    result = future.result()
                    localfiles.append(result)
                    six.print_("Downloaded {}".format(result.filename))
                except GoesAwsDownloadError:
                    error = future.exception()
                    errors.append(error.awsgoesfile)

        # Sort returned list of LocalGoesFile objects by the scan_time
        localfiles.sort(key=lambda x:x.scan_time)
        downloadresults = DownloadResults(localfiles,errors)
        six.print_('{} out of {} files downloaded...{} errors'.format(downloadresults.success_count,
                                                                      downloadresults.total,
                                                                      downloadresults.failed_count))
        return downloadresults



    def _build_prefix_abi(self, product=None, year=None, julian_day=None, hour=None, sector=None):
        """
        Constructs a prefix for the aws bucket

        Parameters
        ----------
        product : str, optional
        year : str or int, optional
        julian_day : str or int, optional
        hour : str or int, optional
        sector : str, optional

        Returns
        -------
        prefix : str
        """
        prod_prefix = {'RAD': 'ABI-L1b',
                       'CMIP': 'ABI-L2',
                       'FDC': 'ABI-L2',
                       'MCMIP': 'ABI-L2'}
        prefix = ''
        prod2 = False
        valid_sectors = ['C', 'M1', 'M2']

        if (sector is not None and sector not in valid_sectors):
            raise ValueError('Invalid sector parameter')

        if product is not None:
            if (sector is None):
                logger = logging.getLogger(__name__)
                logger.error("Invalid sensor parameter 'None'")
                raise ValueError('Sector cannont be None')
            else:
                # Trim sector off the end of the product string, if present
                # if (product[-1] in ['C', 'F', 'M']):
                #     product = product[:-1]
                product = self._trim_product_sector(product)

                prefix += '{}-{}{}/'.format(prod_prefix[product.upper()], product, sector[0])

        if year is not None:
            prefix += self._build_year_format(year)
        if julian_day is not None:
            prefix += self._build_day_format(julian_day)
        if hour is not None:
            prefix += self._build_hour_format(hour)
        if (product is not None) and (hour is not None):
            prefix += 'OR_{}-{}'.format(prod_prefix[product.upper()], product)
            prod2 = True
        if (sector is not None) and (prod2):
            prefix += sector

        return prefix



    def _build_prefix_glm(self, year=None, julian_day=None, hour=None):
        """
        Constructs a prefix for the aws bucket

        Parameters
        ----------
        year : str or int, optional
        julian_day : str or int, optional
        hour : str or int, optional

        Returns
        -------
        prefix : str
        """
        prefix = 'GLM-L2-LCFA/'

        if year is not None:
            prefix += self._build_year_format(year)
        if julian_day is not None:
            prefix += self._build_day_format(julian_day)
        if hour is not None:
            prefix += self._build_hour_format(hour)
            prefix += 'OR_GLM-L2-LCFA'

        return prefix



    def _build_year_format(self, year):
        """

        Parameters
        ----------
        year : int or str

        Returns
        -------
        year : str
            Includes trailing '/'
        """
        if (isinstance(year, int)):
            return '{:04}/'.format(year)
        elif (isinstance(year, str)):
            return '{}/'.format(year)
        else:
            logger = logging.getLogger(__name__)
            logger.error("Invalid year parameter type %s", type(year).__name__)
            raise TypeError('Year must be of type int or str')



    def _build_day_format(self, jd):
        """

        Parameters
        ----------
        jd : int or str

        Returns
        -------
        jd : str
            Includes trailing '/'

        """
        if isinstance(jd, int):
            return '{:03}/'.format(jd)
        elif isinstance(jd, str):
            return '{}/'.format(jd)
        else:
            logger = logging.getLogger(__name__)
            logger.error("Invalid month parameter type %s", type(month).__name__)
            raise TypeError('Month must be int or str type')



    def _build_hour_format(self, hour):
        """

        Parameters
        ----------
        hour : str or int

        Returns
        -------
        hour : str
            Includes trailing '/'
        """
        if isinstance(hour, int):
            return '{:02}/'.format(hour)
        elif isinstance(hour, str):
            return '{}/'.format(hour)
        else:
            logger = logging.getLogger(__name__)
            logger.error("Invalid hour parameter type %s", type(hour).__name__)
            raise TypeError('Hour must be int or str type')



    def _build_channel_format(self, channel):
        """

        Parameters
        ----------
        channel : str

        Returns
        -------
        channel : str
            Format: C<channel w/ padding 0 if applicable>
        """
        if not isinstance(channel, str):
            channel = str(channel)

        return 'C' + channel.zfill(2)



    def _get_sat_bucket(self, satellite, prefix):
        """

        Parameters
        ----------
        satellite : str
            Valid: 'goes16' & 'goes17'
        prefix : str

        Returns
        -------
        resp : dict
            boto3 bucket response

        Notes
        -----
        Important to note that list_objects() & list_objects_v2 only return up
        to 1000 keys. V2 returns a ContinuationToken that can be used to get
        the rest of the keys.

        See: https://alexwlchan.net/2017/07/listing-s3-keys

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects_v2
        """
        resp = None

        if (satellite == 'goes16'):
            resp = self._bucket_16.meta.client.list_objects_v2(Bucket='noaa-goes16', Prefix=prefix, Delimiter='/')
        elif (satellite == 'goes17'):
            resp = self._bucket_17.meta.client.list_objects_v2(Bucket='noaa-goes17', Prefix=prefix, Delimiter='/')
        else:
            logger = logging.getLogger(__name__)
            logger.error("Invalid satellite parameter type %s", satellite)
            raise ValueError("Invalid satallite parameter. Must be either 'goes16' or 'goes17'")

        return resp



    def _datetime_range(self, start, end):
        """
        Creates a range of datetime objects for the period defined by start & end
        """
        diff = (end + timedelta(minutes = 1)) - start

        for x in range(int(diff.total_seconds() / 60)):
            yield start + timedelta(minutes = x)



    def _is_within_range(self, start, end, value):
        """
        Checks to see if a value is within the range defined by start and end

        Parameters
        ----------
        start : datetime object
            Datetime that defines the beginning of the time period
        end : datetime object
            Datetime that defines the ending of the time period
        value : datetime object
            Datetime to evaluate

        Returns
        -------
        int
            -1 if value < start and value < end,
             0 if value >= start and value <= end,
             1 if value > start and value > end
        """
        # if value >= start and value <= end:
        #     return True
        # else:
        #     return False
        if (value < start and value < end):
            return -1
        elif (value >= start and value <= end):
            return 0
        elif (value > start and value > end):
            return 1



    def _parse_partial_fname_abi(self, satellite, product, sector, channel, date, prefix=True):
        """
        Constructs a partial filename for a GOES ABI file with a regular expression
        for the scan mode number.
        Ex: OR_ABI-L2-CMIPM1-M\dC13_G16_s20192591600

        Parameters
        ----------
        satellite : str
            Valid: 'goes16' & 'goes17'
        product : str
            Satellite product
        sector : str
            Satellite scan sector. M1 = mesoscale 1, M2 = mesoscale 2, C = CONUS
        channel : int
            ABI channel
        date : datetime object
        prefix : bool, optional
            Determines whether or not to include the AWS prefix which consists of
            the subdirectory paths. If False, only the filename will be returned.
            Default: True

        Returns
        -------
        fname : str
            Partial filename of ABI file
        """
        fname = ''
        prod_prefix = {'RAD': 'ABI-L1b',
                       'CMIP': 'ABI-L2',
                       'FDC': 'ABI-L2',
                       'MCMIP': 'ABI-L2'}

        year = str(date.year)
        day = str(date.timetuple().tm_yday).zfill(3)
        hour = str(date.hour).zfill(2)
        minute = str(date.minute).zfill(2)

        product = self._trim_product_sector(product)

        if (prefix):
            fname += '{}-{}/{}/{}/'.format(prod_prefix[product.upper()], product, year, day)

        fname += 'OR_{}-{}{}-M\d'.format(prod_prefix[product.upper()], product, sector)

        if (product == 'MCMIP'):
            fname += '_G{}_'.format(satellite[-2:])
        else:
            fname += '{}_G{}_'.format(self._build_channel_format(channel), satellite[-2:])
        fname += 's{}{}{}{}'.format(year, day, hour, minute)

        return fname



    def _parse_partial_fname_glm(self, satellite, date):
        """
        Constructs a partial filename for a GOES ABI file

        Parameters
        ----------
        satellite : str
            Valid: 'goes16' & 'goes17'
        date : datetime object apparently

        Returns
        -------
        fname : str
            Partial filename of GLM file
        """
        year = str(date.year)
        day = str(date.timetuple().tm_yday)
        hour = str(date.hour)
        minute = str(date.minute)

        fname = 'GLM-L2-LCFA/{}/{}/'.format(year, day)
        fname += 'OR_GLM-L2-LCFA_G{}_'.format(satellite[-2:])
        fname += 's{}{}{}{}'.format(year, day, hour, minute)

        return fname



    def _decode_julian_day(self, year, days, key):
        """
        Converts date from Julian day to month & day

        Parameters
        ----------
        year : str
        days : list of something idk
        key : str
            'm' is good here

        Returns
        -------
        a list of dates
        """
        dates = {}

        if not isinstance(year, str):
            year = str(year)

        for day in days:
            curr = datetime.strptime(year[2:] + day, '%y%j').date()

            if (curr.month in list(dates)):
                dates[curr.month].append(curr.day)
            else:
                dates[curr.month] = [curr.day]

        if (key == 'm'):
            return list(dates)
        else:
            return dates



    def _validate_product(self, product):
        # valid_prods = ['ABI-L1b-Rad', 'ABI-L2-CMIP', 'ABI-L2-FDC',
        #                'ABI-L2-MCMIP', 'GLM-L2-LCFA']
        valid_prods = ['RAD', 'CMIP', 'FDC', 'MCMIP']

        if (product.upper() in valid_prods or product[:-1].upper() in valid_prods):
            return True
        else:
            return False



    def _trim_product_sector(self, product):
        """
        Removes sector suffix from product string, if present
        """
        valid_prods = ['RAD', 'CMIP', 'FDC', 'MCMIP']

        # If ABI-L.. is included, remove it
        product = product.split('-')
        if (len(product) > 1):
            product = product[2]
        else:
            product = product[0]

        if (product.upper() in valid_prods):
            return product
        elif (product[:-1].upper() in valid_prods):
            return product[:-1]
        else:
            ValueError('Invalid Product')



    def _download(self, awsgoesfile, basepath, keep_aws_folders, satellite):
        """
        Download helper func. If the file already exists in the specified path,
        it is not re-downloaded.

        Parameters
        ----------
        awsgoesfile : An AwsGoesFile object
            AwsGoesFile related to the file to download
        basepath : str
            Path to download the file to
        keep_aws_folders : bool
            Whether or not to keep the AWS file structure
        satellite : str
            Satellite that created the data

        Returns
        -------
        LocalGoesFile object
        """

        dirpath, filepath = awsgoesfile._create_filepath(basepath, keep_aws_folders)

        try:
            os.makedirs(dirpath)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(dirpath):
                pass
            else:
                raise

        if (not os.path.exists(filepath)):
            try:
                s3 = boto3.client('s3')
                s3.meta.events.register('choose-signer.s3.*', disable_signing)
                if (satellite == 'goes16'):
                    bucket = 'noaa-goes16'
                elif (satellite == 'goes17'):
                    bucket = 'noaa-goes17'
                else:
                    logger = logging.getLogger(__name__)
                    logger.error("Invalid satellite parameter type %s", satellite)
                    raise ValueError("Invalid satellite parameter. Must be 'goes16' or 'goes17'")

                s3.download_file(bucket, awsgoesfile.key, filepath)
                return LocalGoesFile(awsgoesfile, filepath)
            except:
                message = 'Download failed for {}'.format(awsgoesfile.shortfname)
                logger = logging.getLogger(__name__)
                logger.error("Failed to download %s", awsgoesfile.shortfname)
                raise GoesAwsDownloadError(message, awsgoesfile)
        else:
            return LocalGoesFile(awsgoesfile, filepath)



    def _calc_num_glm_files(self, num_mins):
        num_files = (3 * (num_mins + 1)) + 1
        return num_files



class GoesAwsDownloadError(Exception):
    def __init__(self, message, awsgoesfile):
        super(GoesAwsDownloadError, self).__init__(message)
        self.awsgoesfile = awsgoesfile
