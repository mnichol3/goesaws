import goesawsinterface

conn = goesawsinterface.GoesAWSInterface()

#years = conn.get_avail_years('goes16', 'ABI-L1b-RadC')
#print(years)

imgs = conn.get_avail_images_in_range('goes16', 'ABI-L1b-RadM', '5-23-2019-21:00', '5-23-2019-22:30', 'M2', '13')
for img in imgs:
    print(img)
