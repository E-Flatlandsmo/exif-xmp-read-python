image = path_to_image

# Extract exif 
from ExifXmpRead.getExif import get_exif_json, get_exif_xml
print(get_exif_json(image))
print(get_exif_xml(image))

# Extract xmp
from ExifXmpRead.getXmp import get_xmp_json, get_xmp_xml
print(get_xmp_json(image))
print(get_xmp_xml(image))

# Extract exif and xmp merged to a JSON
from ExifXmpRead.getExifXmp import get_exif_xmp_json, get_exif_xmp_xml
print(get_exif_xmp_json(image))
print(get_exif_xmp_xml(image))