# Keep this as a script, not classify it

def convert_to_decimal_degrees(value):
        """Return decimal degrees as float. Helper function to convert the GPS coordinates stored in the EXIF.
        Parameter: 'GPSLongitude': ((6, 1), (8, 1), (409675, 10000))
                    where degrees = 6/1, minutes =  8/1, seconds = 409675/10000 """
        degrees = float(value[0][0]) / float(value[0][1]) 
        minutes = float(value[1][0]) / float(value[1][1]) 
        seconds = float(value[2][0]) / float(value[2][1])
        decimal_degrees =  degrees + (minutes / 60.0) + (seconds / 3600.0)
        return decimal_degrees

def convert_to_meters_above_sealevel(value):
        """ Return meters above sealevel as int. """
        dividend = value[0]
        divisor = value[1]
        meters_above_sealevel = dividend / divisor  
        return meters_above_sealevel