import goesawsinterface

conn = goesawsinterface.GoesAWSInterface()

#years = conn.get_avail_years('goes16', 'ABI-L1b-RadC')
#print(years)

#imgs = conn.get_avail_images_in_range('goes16', 'ABI-L1b-Rad', '5-23-2019-21:00', '5-23-2019-22:30', 'M2', '13')
imgs = conn.get_avail_images_in_range('goes16', 'ABI-L2-CMIP', '5-23-2019-21:00', '5-23-2019-22:30', 'M2', '13')
#imgs = conn.get_avail_images_in_range('goes16', 'ABI-L2-CMIP', '5-23-2019-21:00', '5-23-2019-22:30', 'C', '13')
for img in imgs:
    print(img)

# years = conn.get_avail_years('goes16', 'ABI-L2-CMIP', 'C')
# for year in years:
#     print(year)
