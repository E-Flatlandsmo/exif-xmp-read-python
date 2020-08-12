import os
import csv
import json
from ExifXmpRead.GetExifXmp import ExifXmpFromPicture

# NOTE: 08.05.2020 - Only made for and tested pictures taken with DJI Phantom4 or DJI Mavic Pro.
# Expect Error if you try to use it for other pictures. This is due to different xmp format and namespace nameing.

# Script that diggs into exif and xmp metadata of a picture and 
# creates a csv file with filename, coordinates, gimbal info.  


def _get_csv_row(path_picture):
    """ Return list from one picture. Helper function. 
    input: path to one picture 
    >>> _get_csv_row(path_picture)
    >>> ["Filename", "GimbalYaw", "GimbalPitch", "Latitude", "Longitude"] """
    
    inst = ExifXmpFromPicture(path_picture)
    exif_xmp_str = inst.GetExifXmpJson()
    exif_xmp_json = json.loads(exif_xmp_str)
    filename = exif_xmp_json["Filename"]
    print(exif_xmp_str)
    
    try:
        gimbal_yaw_degree = float(exif_xmp_json["Xmp"]["{http://www.dji.com/drone-dji/1.0/}GimbalYawDegree"])
        gimbal_pitch_degree = float(exif_xmp_json["Xmp"]["{http://www.dji.com/drone-dji/1.0/}GimbalPitchDegree"])
        latitude = exif_xmp_json["Exif"]["GPSLatitude"][0]
        longitude = exif_xmp_json["Exif"]["GPSLongitude"][0]
        csv_row = [filename, path_picture, gimbal_yaw_degree, gimbal_pitch_degree, latitude, longitude]
        return csv_row
    except:
        raise


def write_csv(path_dir):
    """ Return .csv file.
    input: path to the directory where the pictures are located. """
    path_pictures = [os.path.join(path_dir, file_name) for file_name in os.listdir(path_dir)]
    header = ["Filename", "Bildesti", "GimbalYaw", "GimbalPitch", "Latitude", "Longitude"]
   
    with open("CsvFromPictures.csv", 'w', newline='') as write_obj:
        writer = csv.writer(write_obj)
        writer.writerow(header)

    errors = list()
    for path_picture in path_pictures:
        row = _get_csv_row(path_picture)
        if row != None:
            with open("CsvFromPictures.csv", 'a', newline='') as write_obj:
                writer = csv.writer(write_obj)
                writer.writerow(row)
        else: 
            errors.append(path_picture)
    print(f'You just created a csv file')
    print('Errors in the following files: ')
    print(errors)