import goesawsinterface


satellite = 'goes16'
local_abi_path = '/media/mnichol3/pmeyers1/MattNicholson/abi'

conn = goesawsinterface.GoesAWSInterface()

#years = conn.get_avail_years('goes16', 'ABI-L1b-RadC')
#print(years)

#imgs = conn.get_avail_images_in_range('goes16', 'ABI-L1b-Rad', '5-23-2019-21:00', '5-23-2019-22:30', 'M2', '13')
imgs = conn.get_avail_images_in_range(satellite, 'ABI-L2-CMIP', '5-23-2019-21:00', '5-23-2019-21:05', 'M2', '13')
#imgs = conn.get_avail_images_in_range('goes16', 'ABI-L2-CMIP', '5-23-2019-21:00', '5-23-2019-22:30', 'C', '13')
for img in imgs:
    print(img.filename)

result = conn.download(satellite, imgs, local_abi_path, keep_aws_folders=False, threads=6)

# years = conn.get_avail_years('goes16', 'ABI-L2-CMIP', 'C')
# for year in years:
#     print(year)
