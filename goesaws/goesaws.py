"""
Command line wrapper for the GOESAws package

Author: Matt Nicholson
Last updated: 29 Feb 2020
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
        --start
            Start datetime string. Format: MM-DD-YYYY-HH:MM (UTC)
            Stored at args.start
        --end
            End datetime string. Format: MM-DD-YYYY-HH:MM (UTC)
            Stored at args.end
        -p, --prod
            Satellite, instrument, product, and sector to pull imagery from.
            Stored as args.prod
        -d, --dl; optional
            Path to the directory to download files to. Files will only be downloaded
            if this argument is given.
        --kill_aws_struct; optional
            If passed (False), the files will be downloaded directly into the directory
            specified by out_dir. If not passed (True), the files will be downloaded
            to out_dir/year/day_of_year/hour
            Default is False. Stored as args.kill_aws_struct
    """
    parser = argparse.ArgumentParser(description=parse_desc)

    parser.add_argument('-p', '--prod', metavar='product', required=False,
                        dest='prod', action='store', type=str, default=None,
                        help='Satellite, instrument, product, and sector. Ex: "G16-ABI-CMIP-03"')

    parser.add_argument('--start', metavar='start time', dest='start', required=True,
                        action='store', type=str, help='Start time')

    parser.add_argument('--end', metavar='end time', dest='end', required=True,
                        action='store', type=str, help='End time')

    parser.add_argument('-d', '--dl', dest='dl', default=None, action='store_true',
                        help='File download flag')

    parser.add_argument('--kill_aws_struct', dest='kill_aws_struct',
                        action='store_false', help='Keep AWS directory structure')
    return parser


def parse_prod_arg(arg_dict):
    """
    Extract the satellite, instrument, imagery product, and channel from the
    command line 'prod' argument.

    Ex: -p "G16-ABI-CMIP-M2-03"
        -p "G16-GLM"

    Params
    ------
    arg_dict : dict of str
        Parsed command line arguments

    Return
    -------
    dict of str
    """
    # Split on '-'
    # First element : satellite
    # Second element: instrument
    # Third element : imagery product
    # Fourth element: sector
    # Fifth element: channel
    new_args = {'start': args.start,
                'end'  : args.end,
                'download': args.dl,
                'kill_aws_struct': args.kill_aws_struct
                }
    splits = arg_dict.prod.split('-')
    sat   = splits[0].upper()
    instr = splits[1].upper()
    if (instr == 'GLM'):
        sector = ''
        prod   = ''
        chan   = ''
    else:
        prod   = splits[2].upper()
        sector = splits[3].upper()
        chan   = splits[4]
    arg_dict['sat']    = sat
    arg_dict['instr']  = instr
    arg_dict['prod']   = prod
    arg_dict['sector'] = sector
    arg_dict['chan']   = chan
    return arg_dict


def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    _args = parse_prod_arg(args)

    conn = goesawsinterface.GoesAWSInterface()

    imgs = conn.get_avail_images_in_range(_args['sat'], _args['instr'], _args['start'],
                                          _args['end'], product=_args['prod'],
                                          sector=args['sector'], channel=_args['chan'])

    for img in imgs:
        print('{} --> {}'.format(img.scan_time, img.filename))

    if (_args['download']):
        result = conn.download('goes16', imgs, _args['download'],
                               keep_aws_folders=_args['kill_aws_struct'], threads=6)
        for x in result._successfiles:
            print(x.filepath)



if __name__ == '__main__':
    main()
