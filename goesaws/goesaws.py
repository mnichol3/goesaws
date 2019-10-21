"""
Author: Matt Nicholson

Command line wrapper for the GOESAws package

Example usage
-------------

> python goes_aws_dl.py --sat 'goes16' -i 'abi' --start '09-01-2019-00:00' --end '09-01-2019-00:15' -p 'CMIP' --sector 'C' --chan '02'
> python goes_aws_dl.py --start '09-01-2019-00:00' --end '09-01-2019-00:15' -p 'CMIP' --sector 'M1' --chan '02'
> python goes_aws_dl.py --start '09-01-2019-00:00' --end '09-01-2019-00:15' -p 'CMIP' --sector 'M1' --chan '02' -dl -o 'path/to/download'
> python goes_aws_dl.py --start '09-01-2019-00:00' --end '09-01-2019-00:15' -p 'MCMIP' --sector 'C' -dl -o 'path/to/download'
> python goes_aws_dl.py --start '09-01-2019-00:00' --end '09-01-2019-00:15' -p 'MCMIP' --sector 'C' -dl -o 'path/to/download' --kill_aws_struct

GLM:
> python goes_aws_dl.py -i 'glm' --start '09-01-2019-16:00' --end '09-01-2019-16:30'
> python goes_aws_dl.py -i 'glm' --start '09-01-2019-16:00' --end '09-01-2019-16:30' -dl -o 'path/to/download'
"""

import argparse

import goesawsinterface

parse_desc = """A Package to download GOES-R series (GOES-16 & -17) from NOAA's
Amazon Web Service (AWS) bucket.
"""

def create_arg_parser():
    """
    Command line argument parser

    Arguments
        -c, --chan; optional (required for ABI files)
            ABI imagery channel
            Default is None. Stored as args.channel
        -d, --dl; optional (required to dowlnoad files)
            File download flag
            Default is False. Stored as args.dl
        --end
            End datetime string. Format: MM-DD-YYYY-HH:MM (UTC)
            Stored at args.end
        -i, --instr; optional
            Instrument to pull data from ('abi' or 'glm')
            Default is 'abi'. Stored as args.instr
        --kill_aws_struct; optional
            If passed (False), the files will be downloaded directly into the directory
            specified by out_dir. If not passed (True), the files will be downloaded
            to out_dir/year/day_of_year/hour
            Default is False. Stored as args.kill_aws_struct
        -o, --out_dir; optional (required to dowlnoad files)
            Directory to download files to
            Stored as args.out_dir
        -p, --prod; optional (required for ABI files)
            ABI imagery product
            Default is None. Stored as args.prod
        -s, --sector; optional (required for ABI files)
            ABI scan sector
            Default is None. Stored as args.sector
        --sat; optional
            Satellite to pull data from.
            Default is 'goes16'. Stored as args.sat
        --start
            Start datetime string. Format: MM-DD-YYYY-HH:MM (UTC)
            Stored at args.start

    """
    parser = argparse.ArgumentParser(description=parse_desc)

    parser.add_argument('--sat', metavar='satellite', required=False,
                        dest='sat', default='goes16', action='store')

    parser.add_argument('-i', '--instr', metavar='instrument', required=False,
                        dest='instr', action='store', type=str, default='abi',
                        help='Instrument/sensor')

    parser.add_argument('-p', '--prod', metavar='product', required=False,
                        dest='prod', action='store', type=str, default=None,
                        help='ABI product, e.g., CMIP, MCMIP, ...')

    parser.add_argument('-c', '--chan', metavar='channel', required=False,
                        dest='channel', action='store', type=str, help='ABI Channel as a string',
                        default=None)

    parser.add_argument('-s', '--sector', metavar='scan sector', dest='sector',
                        action='store', type=str, default=None,
                        help='ABI scan sector, e.g., "C", "M1", "M2"')

    parser.add_argument('-o', '--output_dir', metavar='directory', dest='out_dir',
                        required=False, type=str, action='store', help='Directory to download files to')

    parser.add_argument('--start', metavar='start time', dest='start', required=True,
                        action='store', type=str, help='Start time')

    parser.add_argument('--end', metavar='end time', dest='end', required=True,
                        action='store', type=str, help='End time')

    parser.add_argument('-d', '--dl', dest='dl', default=False, action='store_true',
                        help='File download flag')

    parser.add_argument('--kill_aws_struct', dest='kill_aws_struct',
                        action='store_false', help='Keep AWS directory structure')

    return parser



def main():
    parser = create_arg_parser()
    args = parser.parse_args()

    conn = goesawsinterface.GoesAWSInterface()

    imgs = conn.get_avail_images_in_range(args.sat, args.instr, args.start, args.end,
                                          product=args.prod, sector=args.sector,
                                          channel=args.channel)

    for img in imgs:
        print('{} --> {}'.format(img.scan_time, img.filename))

    if (args.dl and args.out_dir):
        result = conn.download('goes16', imgs, args.out_dir, keep_aws_folders=args.kill_aws_struct,
                               threads=6)

        for x in result._successfiles:
            print(x.filepath)



if __name__ == '__main__':
    main()
