import json
from ExifXmpRead.getExif import get_exif_json, get_exif_xml
from ExifXmpRead.getXmp import get_xmp_json, get_xmp_xml

#    Extracts exif and xmp metdata from Images and merging it into a JSON.
#    12.08.2020: Supports only merging of JSONs, not XML.

def get_exif_xmp_json(path_image):
    """ Return JSON as string, one Image at a time. 
    Combines exif data and xmp data by merging GetExifJson() and GetXmpJson().
    Error handling: Return None if xmp or exif does not exist. Translated to null in json.dumps(obj) """

    try:
        exif_json = json.loads(get_exif_json(path_image))
    except: 
        exif_json = None

    try:
        xmp_json = json.loads(get_xmp_json(path_image))
    except: 
        xmp_json = None
    
    exif_xmp_dict = {
                "Filename": path_image.split('\\')[-1],
                "Exif": exif_json,
                "Xmp": xmp_json, 
                }

    return json.dumps(exif_xmp_dict, indent=4) 
