# Add examples for every script, nice and clean
# Use this as main. FLY when coding!!
import os
from pprint import pprint

path_dir = r'C:\Users\ef4342\Pictures\work\DroneAppTest\EivindFlatlandsmo_DroneApp_Test'
path_images = [os.path.join(path_dir, image) for image in os.listdir(path_dir)]
image = path_images[0]

from ExifXmpRead.getExif import get_exif_json, get_exif_xml
# print(get_exif_json(image))
# print(get_exif_xml(image))

from ExifXmpRead.getXmp import get_xmp_json, get_xmp_xml
# print(get_xmp_json(image))
# print(get_xmp_xml(image))

from ExifXmpRead.getExifXmp import get_exif_xmp_json, get_exif_xmp_xml
# print(get_exif_xmp_json(image))
print(get_exif_xmp_xml(image))