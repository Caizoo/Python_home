import os 
import itertools
import shutil  
import PIL
import piexif
import piexif.helper
from PIL import Image
import json
import exifread
import datetime as dt 


FOLDERS_LIST = os.listdir("./All Photos")
totals = 0
for FL in FOLDERS_LIST:
	split_vals = FL.split(".")
	if len(split_vals)>2: continue
	
	try:
		json_data = json.load(open(f"./All Photos/{FL}.json"))
		img = Image.open(f"./All Photos/{FL}")
		exif_dict = piexif.load(f"./All Photos/{FL}")
		
		created_date = json_data['photoTakenTime']['timestamp'] 
		created_date = dt.datetime.fromtimestamp(int(created_date))
		month, day = "{:02d}".format(created_date.month), "{:02d}".format(created_date.day)
		hour, minute, second = "{:02d}".format(created_date.hour), "{:02d}".format(created_date.minute), "{:02d}".format(created_date.second)
		created_date = f"{created_date.year}:{month}:{day} {hour}:{minute}:{second}"
		created_date = bytes(created_date, 'utf-8') 
		
		exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = created_date
		
		exif_bytes = piexif.dump(exif_dict)
		img.save(f"./All Photos 2/{FL}", exif=exif_bytes)
			
	except: shutil.copy2(f"./All Photos/{FL}", f"./All Photos 2/{FL}") # move videos 
