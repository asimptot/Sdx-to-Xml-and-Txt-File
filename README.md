# SDX to XML and TXT

This script converts sdx file to txt file for Amazon Fire TVs. If you run the python script to convert the sdx file you should receive three files as output:
1.	sat_germany.txt - sorting file for satellite
2.	dvbc_scan_maps_cfg.xml - sorting file for cable
3.	dvbt_scan_maps_cfg.xml - sorting file for terrestrial 
See the exact information below.

*Usage:*
python SdxToALL.py XXX_Germany_OOO.sdx

After that, it will generate sat_germany.txt, sat_austria.txt, dvbt_scan_maps_cfg.xml and dvbc_scan_maps_cfg.xml automatically.
