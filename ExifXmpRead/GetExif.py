import piexif
import json

class ExifFromPicture:
    """ Returns a JSON with exif metadata from picture. Enables to acquire specific exif data, 
    ex. date, latitude, longitude, etc.
    Returns "None" if the picture does not contain exif. """

    def __init__(self, path_picture):
        self.path_picture = path_picture
        self.exif_data = self._get_exif_all()

    def _get_exif_all(self):
        """ Return exif data as dict. Read everything. """
        try:
            exif_dict = piexif.load(self.path_picture)
            exif_data = dict()
            for ifd in ("0th", "Exif", "GPS", "1st"):   # ifd = image file directory
                for tag in exif_dict[ifd]:
                    exif_data[piexif.TAGS[ifd][tag]["name"]] = exif_dict[ifd][tag]
            return exif_data
        except:
            print(f'Exif Error. Unable to read Exif data from {self.path_picture}')

    def __convert_to_degrees(self, value):
        """Return decimal degrees as float. Helper function to convert the GPS coordinates stored in the EXIF.
        Parameter: 'GPSLongitude': ((6, 1), (8, 1), (409675, 10000))
                    where degrees = 6/1, minutes =  8/1, seconds = 409675/10000 """
        degrees = float(value[0][0]) / float(value[0][1]) 
        minutes = float(value[1][0]) / float(value[1][1]) 
        seconds = float(value[2][0]) / float(value[2][1])
        decimal_degrees =  degrees + (minutes / 60.0) + (seconds / 3600.0)
        return decimal_degrees

    def _GetTimeOriginal(self):
        """ Return Time Original as string."""
        time_original = self.exif_data['DateTimeOriginal'].decode('utf-8').split(' ')[1]
        return time_original

    def _GetDateOriginal(self):
        """ Return date as string. The date represents when the picture was captured. """
        date_original = self.exif_data['DateTimeOriginal'].decode('utf-8').split(' ')[0]
        return date_original

    def _GetLongitude(self):
        """ Return longitude as tuple. Decimal degrees = float. East = 'E'.
        >>> instance._GetLongitude()
        (5.6856583333333335, 'E', 'Decimal Degrees')
        """
        raw_longitude = self.exif_data["GPSLongitude"]
        ref_longitude = self.exif_data["GPSLongitudeRef"].decode('utf-8') 
        longitude = self.__convert_to_degrees(raw_longitude)
        return longitude, ref_longitude, str("Decimal Degrees")

    def _GetLatitude(self):
        """ Return latitude as tuple. Decimal degrees = Float. North = 'N'.
        >>> instance._GetLatitude()
        (60.96168333333333, 'N',  'Decimal Degrees')
        """
        raw_latitude = self.exif_data["GPSLatitude"]
        ref_latitude = self.exif_data["GPSLatitudeRef"].decode('utf-8')  
        latitude = self.__convert_to_degrees(raw_latitude)
        return latitude, ref_latitude, str("Decimal Degrees")

    def _GetAltitude(self):
        """ Return altitude in meters above sealevel.
        rtype: str """
        try:
            altitude = self.exif_data['GPSAltitude'][0]/exif_data['GPSAltitude'][1]
        except:
            altitude = "None"
        return altitude, str('meters Above Sea Level')

    def _GetMake(self):
        """ Return Make as a string. This has something to do with the camera type."""
        make = self.exif_data["Make"].decode('utf-8') # Decoding from binary to string
        return make

    def _GetModel(self):
        """ Retrun Model as a string. This is the camera model."""
        model = self.exif_data["Model"].decode('utf-8') # Decoding from binary to string
        model = "None"
        return model

    def _GetOrientation(self):
        """ Return orientation as an integer. Orientation describes how the picture is rotated."""
        orientation = self.exif_data["Orientation"]
        return orientation

    def _GetMapsGoogleLink(self):
        """ Return gmaps link as string. """
        maps_google_link = f'https://www.google.com/maps?q={self._GetLatitude()[0]}N,{self._GetLongitude()[0]}E'
        return maps_google_link

    def GetExifJson(self):
        """ Return JSON as string. Contains only some of the most used exif data. """
        try:
            neat_json = {
                        "Make" : self._GetMake(),
                        "Model" : self._GetModel(),
                        "DateOriginal" : self._GetDateOriginal(),
                        "TimeOriginal" : self._GetTimeOriginal(),
                        "GPSLatitude" : self._GetLatitude(),
                        "GPSLongitude" : self._GetLongitude(),
                        "GPSAltitude" : self._GetAltitude(),
                        "Orientation" : self._GetOrientation(),
                        "MapsGoogleLink | NOTE: NOT Exif" : self._GetMapsGoogleLink(), #NOTE: Not Exif data, but useful
                        }
            return json.dumps(neat_json)
        except:
            print(f'Exif Error. Hoy! You better understand why. File: {self.path_picture}')