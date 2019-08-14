# goesaws

THIS IS A WORK IN PROGRESS

This module is based on Aaron Anderson's [nexradaws module](https://github.com/aarande/nexradaws) and allows you to query and download GOES-16 and GOES-17 Advanced Baseline Imager (ABI) imagery hosted on NOAA's GOES Amazon Web Services S3 storage. 

Supports Python 3.6, untested on Python 2.7

### Dependencies
* Python 3.6
  * Boto3
  * botocore
  * pytz
  * six
  
### Example Usage
```python
import goesawsinterface

local_abi_path = 'download/files/here'

conn = goesawsinterface.GoesAWSInterface()

# Returns a list of AWSGoesFile objects with scan times occuring in the period of 8-6-2019-15:00z 
# to 8-6-2019-16:30z. 
imgs = conn.get_avail_images_in_range('goes16', 'ABI-L2-CMIP', '8-6-2019-15:00', '8-6-2019-15:10', 'M2', '13')

# Print the scan times and names of the AWSGoesFile objects
for img in imgs:
    print('{} --> {}'.format(img.scan_time, img.filename)

# Download the ABI files to the directory specified in 'local_abi_path'
result = conn.download('goes16', imgs, local_abi_path, keep_aws_folders=False, threads=6)

# Print the local paths & filenames of the successfully downloaded files
for x in results._successfiles:
    print(x.filepath)
```
Output:
```
08-06-2019-15:00 --> OR_ABI-L2-CMIPM2-M6C13_G16_s20192181500281_e20192181500352_c20192181500415.nc
08-06-2019-15:01 --> OR_ABI-L2-CMIPM2-M6C13_G16_s20192181501281_e20192181501350_c20192181501406.nc
08-06-2019-15:02 --> OR_ABI-L2-CMIPM2-M6C13_G16_s20192181502281_e20192181502351_c20192181502433.nc
08-06-2019-15:03 --> OR_ABI-L2-CMIPM2-M6C13_G16_s20192181503281_e20192181503350_c20192181503409.nc
08-06-2019-15:04 --> OR_ABI-L2-CMIPM2-M6C13_G16_s20192181504281_e20192181504350_c20192181504435.nc
08-06-2019-15:05 --> OR_ABI-L2-CMIPM2-M6C13_G16_s20192181505281_e20192181505350_c20192181505408.nc
08-06-2019-15:06 --> OR_ABI-L2-CMIPM2-M6C13_G16_s20192181506281_e20192181506350_c20192181506412.nc
08-06-2019-15:07 --> OR_ABI-L2-CMIPM2-M6C13_G16_s20192181507281_e20192181507350_c20192181507426.nc
08-06-2019-15:08 --> OR_ABI-L2-CMIPM2-M6C13_G16_s20192181508281_e20192181508350_c20192181508422.nc
08-06-2019-15:09 --> OR_ABI-L2-CMIPM2-M6C13_G16_s20192181509281_e20192181509351_c20192181509417.nc
08-06-2019-15:10 --> OR_ABI-L2-CMIPM2-M6C13_G16_s20192181510281_e20192181510354_c20192181510415.nc

Downloaded OR_ABI-L2-CMIPM2-M6C13_G16_s20192181500281_e20192181500352_c20192181500415.nc
Downloaded OR_ABI-L2-CMIPM2-M6C13_G16_s20192181503281_e20192181503350_c20192181503409.nc
Downloaded OR_ABI-L2-CMIPM2-M6C13_G16_s20192181501281_e20192181501350_c20192181501406.nc
Downloaded OR_ABI-L2-CMIPM2-M6C13_G16_s20192181502281_e20192181502351_c20192181502433.nc
Downloaded OR_ABI-L2-CMIPM2-M6C13_G16_s20192181504281_e20192181504350_c20192181504435.nc
Downloaded OR_ABI-L2-CMIPM2-M6C13_G16_s20192181505281_e20192181505350_c20192181505408.nc
Downloaded OR_ABI-L2-CMIPM2-M6C13_G16_s20192181508281_e20192181508350_c20192181508422.nc
Downloaded OR_ABI-L2-CMIPM2-M6C13_G16_s20192181506281_e20192181506350_c20192181506412.nc
Downloaded OR_ABI-L2-CMIPM2-M6C13_G16_s20192181507281_e20192181507350_c20192181507426.nc
Downloaded OR_ABI-L2-CMIPM2-M6C13_G16_s20192181509281_e20192181509351_c20192181509417.nc
Downloaded OR_ABI-L2-CMIPM2-M6C13_G16_s20192181510281_e20192181510354_c20192181510415.nc
11 out of 11 files downloaded...0 errors
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
