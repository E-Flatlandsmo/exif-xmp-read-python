#! python3
# XMP read https://stackoverflow.com/questions/6822693/read-image-xmp-data-in-python 

import os
import json
import xml.etree.ElementTree as ET

class XmpFromPicture:
    """ Retrun xmp data as string and json.
    21.03.2020 - Tested and works with DJI Matrice, DJI Mavic Pro, DJI Phantom 4, Richo Theta V.
    input: path_to_picture
    output: string, json """

    def __init__(self, path_picture):
        self.path_picture = path_picture

    def GetXmpString(self):
        """ Return xmp metadata as string. Reads the file in binary format.
        Using the find method to return the data between namespace <x:xmpmeta and </x:xmpmeta. """
        with open(self.path_picture, mode = 'rb') as open_bytes:
            data = open_bytes.read()
            xmp_start = data.find(b'<x:xmpmeta')
            xmp_end = data.find(b'</x:xmpmeta')
            xmp_bin = data[xmp_start:xmp_end+12]
            xmp_str = xmp_bin.decode('utf-8')
            return xmp_str 
    
    def GetXmpJson(self, raw=True):
        """ Return JSON as string.
        input: raw=True, This raws away the namespaces. None or false, it will keep the namespaces. 
        Tested on: DJI Matrice, DJI Mavic Pro, Phantom 4, Richo Theta V, Insta 360 Pro, pictures from fotoweb.
        According to w3schools an attribute cannot store multiple values. Strips these from DJI Mavic and Phantom: .
            xmlns:tiff="http://ns.adobe.com/tiff/1.0/"
            xmlns:exif="http://ns.adobe.com/exif/1.0/"
            xmlns:xmp="http://ns.adobe.com/xap/1.0/"
            xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/"
            xmlns:dc="http://purl.org/dc/elements/1.1/"
            xmlns:crs="http://ns.adobe.com/camera-raw-settings/1.0/"
            xmlns:drone-dji="http://www.dji.com/drone-dji/1.0/" """
        try:
            xmp_str = self.GetXmpString()
            root = ET.fromstring(xmp_str)
            tot_dict = dict()
            if raw == True:
                tot_dict  = dict()
                for element in root.iter():
                    inner_dict_1 = {element.tag:element.text}
                    inner_dict_2 = element.attrib
                    tot_dict = {**tot_dict, **inner_dict_1, **inner_dict_2}
                return json.dumps(tot_dict, indent=4)
            else:
                tot_dict  = dict()
                for element in root.iter():
                    tag_stripped = element.tag.split('}')[1]
                    inner_dict_1 = {tag_stripped:element.text}
                    inner_dict_2 = dict()
                    for keys, values in element.attrib.items():
                        keys = keys.split('}')[1]
                        inner_dict_2 = {**inner_dict_2, **{keys:values}}
                    tot_dict = {**tot_dict, **inner_dict_1, **inner_dict_2}
                return json.dumps(tot_dict, indent=4)
        except:
            print(f'Xmp Error. File {self.path_picture}')

    def GetNumberOfTextElements(self):
        """ Return length of xml text elements. """
        xmp_str = self.GetXmpString()
        root = ET.fromstring(xmp_str)
        text = list()
        for element in root.iter():
            text = text + [element.text]
        return len(text)

    def WriteFileInBytes(self): #NOTE: Saved this function to the future. It might be gold to dig into this. 08.03.2020
        """ Return .txt as string in bytes. In this soup, all information of a picture might be stored. """
        with open(self.path_picture, mode = 'rb') as open_bytes:
            data = open_bytes.read()
        file, ext = os.path.splitext(self.path_picture) 
        filename = file.split('\\')[-1]
        with open(f"{filename}_Bytes.txt", "w") as write_bytes: #NOTE: maybe wb instead?
            write_bytes.write(data) 
        
