# goesaws


This module is based on Aaron Anderson's [nexradaws module](https://github.com/aarande/nexradaws) and allows you to query and download GOES-16 and GOES-17 Advanced Baseline Imager (ABI) imagery hosted on NOAA's GOES Amazon Web Services S3 storage from the command line.

Supports Python 3.6

### Dependencies
* Python 3.6
  * Boto3
  * botocore
  * pytz

### Example Usage
#### Advanced Baseline Imager (ABI) files
```shell
python goesaws.py --start '08-06-2019-15:00' --end '08-06-2019-15:11' -p 'CMIP' --sector 'M2' --chan '02' -dl -o 'download/files/here'
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

/download/files/here/OR_ABI-L2-CMIPM2-M6C13_G16_s20192181500281_e20192181500352_c20192181500415.nc
/download/files/here/OR_ABI-L2-CMIPM2-M6C13_G16_s20192181501281_e20192181501350_c20192181501406.nc
/download/files/here/OR_ABI-L2-CMIPM2-M6C13_G16_s20192181502281_e20192181502351_c20192181502433.nc
/download/files/here/OR_ABI-L2-CMIPM2-M6C13_G16_s20192181503281_e20192181503350_c20192181503409.nc
/download/files/here/OR_ABI-L2-CMIPM2-M6C13_G16_s20192181504281_e20192181504350_c20192181504435.nc
/download/files/here/OR_ABI-L2-CMIPM2-M6C13_G16_s20192181505281_e20192181505350_c20192181505408.nc
/download/files/here/OR_ABI-L2-CMIPM2-M6C13_G16_s20192181506281_e20192181506350_c20192181506412.nc
/download/files/here/OR_ABI-L2-CMIPM2-M6C13_G16_s20192181507281_e20192181507350_c20192181507426.nc
/download/files/here/OR_ABI-L2-CMIPM2-M6C13_G16_s20192181508281_e20192181508350_c20192181508422.nc
/download/files/here/OR_ABI-L2-CMIPM2-M6C13_G16_s20192181509281_e20192181509351_c20192181509417.nc
/download/files/here/OR_ABI-L2-CMIPM2-M6C13_G16_s20192181510281_e20192181510354_c20192181510415.nc
```
#### Geostationary Lightning Mapper (GLM) files
```shell
python goesaws.py -i 'glm' --start '09-01-2019-16:00' --end '09-01-2019-16:30' -dl -o 'path/to/download'
```

More usage examples can be found in ```goesaws.py```

### Command Line Arguments
- ```-c```, ```--chan``` (optional; required for ABI files)
  - ABI imagery channel.
    Default is None. Stored as args.channel
- ```-d```, ```--dl``` (optional; required to dowlnoad files)
  - File download flag
    Default is False. Stored as args.dl
- ```--end```
  - End datetime string. Format: MM-DD-YYYY-HH:MM (UTC)
    Stored at args.end
- ```-i```, ```--instr``` (optional)
  - Instrument to pull data from ('abi' or 'glm')
    Default is 'abi'. Stored as args.instr
- ```--kill_aws_struct``` (optional)
  - If passed (False), the files will be downloaded directly into the directory
    specified by out_dir. If not passed (True), the files will be downloaded
    to out_dir/year/day_of_year/hour
    Default is False. Stored as args.kill_aws_struct
- ```-o```, ```--out_dir``` (optional; required to dowlnoad files).
  - Directory to download files to
    Stored as args.out_dir
- ```-p```, ```--prod``` (optional; required for ABI files)
  - ABI imagery product
    Default is None. Stored as args.prod
- ```-s```, ```--sector``` (optional; required for ABI files).
  - ABI scan sector
    Default is None. Stored as args.sector
- ```--sat``` (optional)
  - Satellite to pull data from.
    Default is 'goes16'. Stored as args.sat
- ```--start```
  - Start datetime string. Format: MM-DD-YYYY-HH:MM (UTC).
    Stored at args.start
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
