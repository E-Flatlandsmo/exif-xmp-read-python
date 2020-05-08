import json
from ExifXmpRead.GetXmp import XmpFromPicture
from ExifXmpRead.GetExif import ExifFromPicture

class ExifXmpFromPicture:
    """ Class for extracting both Exif and Xmp metdata from pictures and merging the data.
    27.03.2020: Supports only JSON. """
    
    def __init__(self, path_picture):
        self.path_picture = path_picture

    def GetExifXmpJson(self):
        """ Return JSON as string, one picture at a time. 
        Combines exif data and xmp data by merging GetExifJson() and GetXmpJson().
        Error handling: Return None if xmp or exif does not exist. Translated to null in json.dumps(obj) """
        
        exif_instance = ExifFromPicture(self.path_picture)
        get_exif = exif_instance.GetExifJson()
        try:
            exif_json = json.loads(get_exif)
        except: 
            exif_json = None

        xmp_instance = XmpFromPicture(self.path_picture)
        get_xmp = xmp_instance.GetXmpJson(raw=True) #NOTE: How to handle this in GetExifXMP?
        try:
            xmp_json = json.loads(get_xmp)
        except: 
            xmp_json = None
        
        exif_xmp_dict = {
                    "Filename": self.path_picture.split('\\')[-1],
                    "Exif": exif_json,
                    "Xmp": xmp_json, 
                    }
        return json.dumps(exif_xmp_dict, indent=4) 
        