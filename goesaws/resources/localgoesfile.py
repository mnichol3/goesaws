import os
from netCDF4 import Dataset


class LocalGoesFile(object):

    def __init__(self, awsgoesfile, localfilepath):
        super(LocalGoesFile, self).__init__()
        self.key = awsgoesfile.key
        self.shortfname = awsgoesfile.shortfname
        self.filename = awsgoesfile.filename
        self.scan_time = awsgoesfile.scan_time
        self.filepath = localfilepath


    def __repr__(self):
        return '<LocalGoesFile object - {}>'.format(self.filepath)
