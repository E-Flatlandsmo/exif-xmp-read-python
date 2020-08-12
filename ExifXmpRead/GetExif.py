# Version 2.0.2 | Updated 12.08.2020

# Return exif as xml or json. A lot of DRY 13.06.2020. Reads exif with piexif, 
# decodes, and cleans the data and converts it to more userfriendly datatypes and format."""

import piexif
import json
from ExifXmpRead.GPSConverter import convert_to_decimal_degrees, convert_to_meters_above_sealevel

problematic_exif = ["FileSource", "SceneType", "MakerNote", "XPComment", "UserComment", "ComponentsConfiguration", "XPKeywords"]  #NOTE: Cheap solution. A general solution would be better.


def _get_exif_raw(path_image):
    """ Return raw exif data as dict. Piexif is used. """
    try:
        exif_dict = piexif.load(path_image)
        exif_data = dict()
        for ifd in ("0th", "Exif", "GPS", "1st"):   # ifd = image file directory
            for tag in exif_dict[ifd]:
                exif_data[piexif.TAGS[ifd][tag]["name"]] = exif_dict[ifd][tag]
        return exif_data
    except:
        print(f'Exif Error. Unable to read Exif data from {path_image}')


def get_exif_json(path_image):
    """ Return exif as JSON. The elements are decoded from binary to str and GPS converted."""
    
    element = dict()
    for key, value in _get_exif_raw(path_image).items():
        
        if  key in ["GPSLatitude","GPSLongitude"]:
            decimal_degrees = convert_to_decimal_degrees(value)
            element[f'{key}_decimal_degrees'] = decimal_degrees
            continue
        if key == "GPSAltitude":               
            element[key] = convert_to_meters_above_sealevel(value)
            continue
        if key in problematic_exif:
            element[key] = "Removed by script GetExif."
            continue 
        if type(value) == bytes:
            element[key] = value.decode('utf-8').strip('\x00') #BUG: Fixed 13.06.2020! Confused space with char null. Tried to strip(' ')
        else:
            element[key] = value

    return json.dumps(element, indent=4)


def get_exif_xml(path_image):
    """ Return exif data on xml format. Contains all the exif data from _get_exif_all(). 
    Contain a lot of DRY - To be improved 13.06.2020
    param: None
    rtype: xml as string """
    
    elements = str()
    for key, value in _get_exif_raw(path_image).items():

        if key in ["GPSLatitude","GPSLongitude"]:
            coord = convert_to_decimal_degrees(value)
            element = f'<exif:{key}_decimal_degrees>{coord}</exif:{key}_decimal_degrees>\n'
            elements = elements + element
            continue
        if key == "GPSAltitude":               
            alt = convert_to_meters_above_sealevel(value) 
            element = f'<exif:{key}_meters>{alt}</exif:{key}_meters>\n'
            elements = elements + element
            continue
        if key in problematic_exif:
            element = f'<exif:{key}>{"Removed by GetExif"}</exif:{key}>\n'
            elements = elements + element
            continue 
        if type(value) == bytes:
            try:
                decoded_value = value.decode('utf-8').strip('\x00')
                element = f'<exif:{key}>{decoded_value}</exif:{key}>\n'
                elements = elements + element
            except:
                element = f'<exif:{key}>{"Unable to decode with utf-8"}</exif:{key}>\n'
                elements = elements + element
        else:
            element = f'<exif:{key}>{value}</exif:{key}>\n '
            elements = elements + element

    return elements

def get_google_maps_link(path_image):
    """ Return gmaps link as string. """
    json_str = get_exif_json(path_image)
    json_obj = json.loads(json_str)

    lat = json_obj["GPSLatitude_decimal_degrees"]
    lon = json_obj["GPSLongitude_decimal_degrees"]

    google_maps_link = f'https://www.google.com/maps?q={lat}N,{lon}E'
    return google_maps_link
