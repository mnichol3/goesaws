import os
import re

from datetime import datetime


class AwsGoesFile(object):

    def __init__(self, key, shortfname, scan_time):
        super(AwsGoesFile, self).__init__()
        self.key = key
        self.shortfname = shortfname
        self.scan_time = scan_time
        self.awspath = None
        self.filename = None
        if self.key is not None:
            self._parse_key()



    def _parse_key(self):
        self.awspath, self.filename = os.path.split(self.key)



    def _create_filepath(self, basepath, keep_aws_structure):
        if keep_aws_structure:
            directorypath = os.path.join(basepath, self.awspath)
            filepath = os.path.join(directorypath, self.filename)
        else:
            directorypath = basepath
            filepath = os.path.join(basepath, self.filename)

        return directorypath,filepath




    def __repr__(self):
        return '<AwsGoesFile object - {}>'.format(self.shortfname)
