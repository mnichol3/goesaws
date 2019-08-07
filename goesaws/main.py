import goesawsinterface

# Path to the directory that you want to save the files in
local_abi_path = '/media/mnichol3/pmeyers1/MattNicholson/abi'

# Create a connection object
conn = goesawsinterface.GoesAWSInterface()

# Returns a list of AwsGoesFile objects representing AWS
                                               # product      # start date       # end date     # sector  # channel
imgs = conn.get_avail_images_in_range('goes16', 'ABI-L2-CMIP', '8-6-2019-15:00', '8-6-2019-15:10', 'M2', '13')
for img in imgs:
    print('{} --> {}'.format(img.scan_time, img.filename))

result = conn.download('goes16', imgs, local_abi_path, keep_aws_folders=False, threads=6)
for x in result._successfiles:
    print(x.filepath)
