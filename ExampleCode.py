# Example code snippets

# path_dir = r'put-in-path-to-dir-here'

### ----- PRINT EXIF AND XMP IN TERMINAL FROM ALL PICTURES IN A DIR -----
# import os
# from ExifXmpRead.GetExifXmp import ExifXmpFromPicture
# path_pictures = [os.path.join(path_dir, file_name) for file_name in os.listdir(path_dir)]
# for path_picture in path_pictures:
#     inst = ExifXmpFromPicture(path_picture)
#     exif_xmp_data = inst.GetExifXmpJson()
#     print(exif_xmp_data)


### ---- VERY USEFUL!!! PRINTS XMP RAW STRING RETRIEVED FROM PICTURE ----
import os
from ExifXmpRead.GetXmp import XmpFromPicture
path_pictures = [os.path.join(path_dir, file_name) for file_name in os.listdir(path_dir)]
for path_picture in path_pictures:
    inst_xmp = XmpFromPicture(path_picture)
    xmp_str = inst_xmp.GetXmpString()
    print(xmp_str)

### ----- CSV. Write CSV from pictures in dir. ------ 
# NOTE: Only made for DJI Mavic Pro & DJI Phantom 4 due to their metadata format and namespace nameing.
# from ConvertingFormats.CSV import GetCsv
# print(GetCsv.write_csv(path_dir))


