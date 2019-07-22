import os
import re
import sys
from datetime import timedelta, datetime

import boto3
import errno
import pytz
import six
from botocore.handlers import disable_signing
import concurrent.futures

from awsgoesfile import AwsGoesFile
from downloadresults import DownloadResults
from localgoesfile import LocalGoesFile


"""
Ex:

import goesawsinterface

conn = goesawsinterface.GoesAWSInterface()

years = conn.get_avail_years('goes16', 'ABI-L1b-RadC')

imgs = conn.get_avail_images('goes16', 'ABI-L1b-RadM', '5-23-2019-21', 'M2', '13')

"""

class GoesAWSInterface(object):
    """
    Instantiate an instance of this class to get a connection to the GOES AWS bucket.
    This class provides methods to query for various metadata of the AWS bucket as well
    as download files.
    >>> import goesaws
    >>> conn = goesaws.GoesAwsInterface()
    """
    def __init__(self):
        super(GoesAWSInterface, self).__init__()
        self._year_re = re.compile(r'/(\d{4})/')
        self._day_re = re.compile(r'/\d{4}/(\d{3})/')
        self._hour_re = re.compile(r'/\d{4}/\d{3}/(\d{2})/')
        self._scan_m_re = re.compile(r'(\w{3,4}M\d-M\dC\d{2})_G\d{2}_s\d{7}(\d{4})\d{3}')
        self._scan_c_re = re.compile(r'(\w{4,5}-M\dC\d{2})_G\d{2}_s\d{7}(\d{4})\d{3}')
        self._s3conn = boto3.resource('s3')
        self._s3conn.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)
        self._bucket_16 = self._s3conn.Bucket('noaa-goes16')
        self._bucket_17 = self._s3conn.Bucket('noaa-goes17')



    def get_avail_products(self, satellite):
        """
        Gets a list of available products (Rad, CMIP, MCMIP) for a satellite

        Parameters
        ----------
        satellite : str
            The satellite to fetch available products for.
            Valid: 'goes16' & 'goes17'

        Returns
        -------
        prods : list of str
            List of available products
        """
        prods = []

        resp = self._get_sat_bucket(satellite, '')

        for x in resp.get('CommonPrefixes'):
            prods.append(list(x.values())[0][:-1])

        return prods



    def get_avail_years(self, satellite, product, sector):
        """
        Gets the years for which data is available for a given satellite & product

        Parameters
        ----------
        satellite : str
            The satellite to fetch available products for.
            Valid: 'goes16' & 'goes17'
        product : str
            Imagery product to retrieve available data for

        Returns
        -------
        years : list of str
            List containing the years for which data is available for the given
            satellite and product
        """
        years = []

        prefix = self._build_prefix(product=product, sector=sector)
        resp = self._get_sat_bucket(satellite, prefix)

        for each in resp.get('CommonPrefixes'):
            match = self._year_re.search(each['Prefix'])
            if (match is not None):
                years.append(match.group(1))

        return years



    def get_avail_months(self, satellite, product, year):
        """
        Gets the months for which data is available for a given satellite, product,
        and year

        Parameters
        ----------
        satellite : str
            The satellite to fetch available products for.
            Valid: 'goes16' & 'goes17'
        product : str
            Imagery product to retrieve available data for
        year : str or int
            Year to fetch the available months for

        Returns
        -------
        months : list of int
            List of months for which data is available
        """

        days = self.get_avail_days(satellite, product, year)
        months = self._decode_julian_day(year, days, 'm')

        return months



    def get_avail_days(self, satellite, product, sector, year):
        """
        Retrieves the days of the given year for which data is available for the
        given satellite and product

        Parameters
        ----------
        satellite : str
            The satellite to fetch available products for.
            Valid: 'goes16' & 'goes17'
        product : str
            Imagery product to retrieve available data for
        year : str or int
            Year to fetch the available months for

        Returns
        -------
        days : set of str
        """
        days = []

        prefix = self._build_prefix(product=product, sector=sector, year=year)
        resp = self._get_sat_bucket(satellite, prefix)

        for each in resp.get('CommonPrefixes'):
            match = self._day_re.search(each['Prefix'])
            if (match is not None):
                days.append(match.group(1))

        return days



    def get_avail_hours(self, satellite, product, sector, date):
        """
        Gets the hours that data is available for a given satellite, product,
        and date

        Parameters
        ----------
        satellite : str
            The satellite to fetch available products for.
            Valid: 'goes16' & 'goes17'
        product : str
            Imagery product to retrieve available data for
        date : str
            Date of the data. Format: MM-DD-YYYY

        Returns
        -------
        hours : list of int
            Hours for which data is available, in UTC format
        """
        hours = []

        year = date[-4:]
        jul_day = datetime.strptime(date, '%m-%d-%Y').timetuple().tm_yday

        prefix = self._build_prefix(product=product, sector=sector, year=year, julian_day=jul_day)
        resp = self._get_sat_bucket(satellite, prefix)

        for each in resp.get('CommonPrefixes'):
            match = self._hour_re.search(each['Prefix'])
            if (match is not None):
                hours.append(match.group(1))

        return hours



    def get_avail_images(self, satellite, product, date, sector, channel):
        """

        Parameters
        ----------
        satellite : str
            The satellite to fetch available products for.
            Valid: 'goes16' & 'goes17'
        product : str
            Imagery product to retrieve available data for
        date : str
            Date & time of the data. Format: MM-DD-YYYY-HH
        sector : str
            Satellite scan sector. M1 = mesoscale 1, M2 = mesoscale 2, C = CONUS
        channel : int
            ABI channel

        Returns
        -------
        images : list of AwsGoesFile objects
            AwsGoesFile objects representing available data files
        """
        images = []

        if (sector == 'C'):
            scan_re = self._scan_c_re
        else:
            scan_re = self._scan_m_re

        if (not isinstance(date, datetime)):
            date = datetime.strptime(date, '%m-%d-%Y-%H')

        year = date.year
        hour = date.hour
        jul_day = date.timetuple().tm_yday

        prefix = self._build_prefix(product=product, year=year, julian_day=jul_day, hour=hour, sector=sector)
        resp = self._get_sat_bucket(satellite, prefix)

        for each in list(resp['Contents']):

            match = scan_re.search(each['Key'])
            if (match is not None):
                if (sector in match.group(1) and channel in match.group(1)):
                    time = match.group(2)
                    dt = datetime.strptime(str(year) + ' ' + str(jul_day) + ' ' + time, '%Y %j %H%M')
                    dt = dt.strftime('%m-%d-%Y-%H:%M')
                    images.append(AwsGoesFile(each['Key'], match.group(1) + ' ' + dt, dt))

        return images



    def get_avail_images_in_range(self, satellite, product, start, end, sector, channel):
        """

        Parameters
        ----------
        satellite : str
            The satellite to fetch available products for.
            Valid: 'goes16' & 'goes17'
        product : str
            Imagery product to retrieve available data for
        start : str
            Start date & time of the data. Format: MM-DD-YYYY-HH:MM
        end : str
            End date & time of the data. Format: MM-DD-YYYY-HH:MM
        sector : str
            Satellite scan sector. M1 = mesoscale 1, M2 = mesoscale 2, C = CONUS
        channel : int
            ABI channel

        Returns
        -------
        images : list of AwsGoesFile objects
            AwsGoesFile objects representing available data files between the start
            and end date & times, inclusive
        """
        images = []
        added = []

        start_dt = datetime.strptime(start, '%m-%d-%Y-%H:%M')
        end_dt = datetime.strptime(end, '%m-%d-%Y-%H:%M')

        prev_hour = start_dt.hour
        first = True

        for day in self._datetime_range(start_dt, end_dt):
            curr_hour = day.hour

            if (prev_hour != curr_hour):
                first = True

            if (first):
                first = False
                avail_imgs = self.get_avail_images(satellite, product, day, sector, channel)

                for img in avail_imgs:
                    if ((self._build_channel_format(channel) in img.shortfname) and (sector in img.shortfname)):
                        if (self._is_within_range(start_dt, end_dt, datetime.strptime(img.scan_time, '%m-%d-%Y-%H:%M'))):
                            if (img.shortfname not in added):
                                added.append(img.shortfname)
                                images.append(img)
            prev_hour = curr_hour
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
            future_download = {executor.submit(self._download,goesfile,basepath,keep_aws_folders,satellite): goesfile for goesfile in awsgoesfiles}

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



    def _build_prefix(self, product=None, year=None, julian_day=None, hour=None, sector=None):
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
        prefix = ''
        prod2 = False

        if product is not None:
            if (sector is None):
                raise ValueError('Sector cannont be None')
            else:
                prefix += product
                prefix += sector[0]
                prefix += '/'
        if year is not None:
            prefix += self._build_year_format(year)
        if julian_day is not None:
            prefix += self._build_day_format(julian_day)
        if hour is not None:
            prefix += self._build_hour_format(hour)
        if (product is not None) and (hour is not None):
            prefix += 'OR_' + product
            prod2 = True
        if (sector is not None) and (prod2):
            prefix += sector

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

        Returns
        -------
        boolean
        """
        if value >= start and value <= end:
            return True
        else:
            return False



    def _parse_partial_fname(self, satellite, product, sector, channel, date):
        """
        Constructs a partial filename for a GOES ABI file

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
        date : datetime object apparently

        Returns
        -------
        fname : str
            Partial filename of ABI file
        """
        if (date.year > 2018):
            mode = 'M6'
        else:
            mode = 'M3'

        year = str(date.year)
        day = str(date.timetuple().tm_yday)
        hour = str(date.hour)
        minute = str(date.minute)

        fname = 'ABI-L2-' + product + '/' + year + '/' + day
        fname += '/OR_ABI-L2-' + product + sector + '-' + mode
        fname += self._build_channel_format(channel) + '_G' + satellite[-2:] + '_'
        fname += 's' + year + day + hour + minute

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
                    print('Error: Invalid satellite')
                    sys.exit(0)

                s3.download_file(bucket, awsgoesfile.key, filepath)
                return LocalGoesFile(awsgoesfile, filepath)
            except:
                message = 'Download failed for {}'.format(awsgoesfile.shortfname)
                raise GoesAwsDownloadError(message, awsgoesfile)
        else:
            return LocalGoesFile(awsgoesfile, filepath)



class GoesAwsDownloadError(Exception):
    def __init__(self, message, awsgoesfile):
        super(GoesAwsDownloadError, self).__init__(message)
        self.awsgoesfile = awsgoesfile
