import goesawsinterface

# Path to the directory that you want to save the files in
local_abi_path = '/media/mnichol3/pmeyers1/MattNicholson/abi'
local_data_path = '/media/mnichol3/tsb1/data/abi/dorian/inf'

# Create a connection object
conn = goesawsinterface.GoesAWSInterface()

# Returns a list of AwsGoesFile objects representing AWS
                                               # product      # start date       # end date     # sector  # channel
# imgs = conn.get_avail_images_in_range('goes16', 'ABI-L2-CMIP', '8-6-2019-15:00', '8-6-2019-15:10', 'M2', '13')
# imgs = conn.get_avail_images_in_range('goes16', 'abi', '09-01-2019-00:00', '09-06-2019-13:00', product='ABI-L2-CMIP', sector='M1', channel='13')
# imgs = conn.get_avail_images_in_range('goes16', 'abi', '09-01-2019-00:00', '09-06-2019-13:00', product='ABI-L1b-Rad', sector='M1', channel='02')
imgs = conn.get_avail_images_in_range('goes16', 'abi', '09-01-2019-13:00', '09-01-2019-13:10', product='Rad', sector='M1', channel='02')
# imgs = conn.get_avail_images_in_range('goes16', 'abi', '09-01-2019-13:00', '09-01-2019-13:10', product='MCMIP', sector='M1', channel=None)

for img in imgs:
    print('{} --> {}'.format(img.scan_time, img.filename))
    # print(img.shortfname)

# result = conn.download('goes16', imgs, local_data_path, keep_aws_folders=False, threads=6)
# for x in result._successfiles:
#     print(x.filepath)
