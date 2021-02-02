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

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)
    
FOLDERS_LIST = os.listdir("./Google Photos")

all_list = [] 
current_folder = 0

print("{:02d}".format(1))
os.mkdir(f"./Google Photos/videos")

for FL in FOLDERS_LIST:
	
	fl_list = [] 
	all_files = os.listdir(f"./Google Photos/{FL}") 
	all_files_2 = [] 
	
	for a in all_files:
		split_vals = a.split(".") 
		if len(split_vals)>3: continue 
		if len(split_vals)<3: all_files_2.append(a) 
	

	all_files = list(grouper(50, all_files_2))
	all_files = [list(a) for a in all_files]
	all_files = [list(filter(lambda a: not a==None, a)) for a in all_files]
	
	files_to_do = sum([len(a) for a in all_files])
	i = 0
	
	for a in all_files: # for each group of 50 (or less)
		
		str_int = str(current_folder).zfill(3)
		os.mkdir(f"./Google Photos/photo_{str_int}")
		
		current_folder += 1
		
		
		for b in a:
			print(f"Formatting file {i}/{files_to_do}")
			try:
				json_data = json.load(open(f"./Google Photos/{FL}/{b}.json"))
				img = Image.open(f"./Google Photos/{FL}/{b}")
				exif_dict = piexif.load(f"./Google Photos/{FL}/{b}")
				
				created_date = json_data['photoTakenTime']['timestamp'] 
				created_date = dt.datetime.fromtimestamp(int(created_date))
				month, day = "{:02d}".format(created_date.month), "{:02d}".format(created_date.day)
				hour, minute, second = "{:02d}".format(created_date.hour), "{:02d}".format(created_date.minute), "{:02d}".format(created_date.second)
				created_date = f"{created_date.year}:{month}:{day} {hour}:{minute}:{second}"
				created_date = bytes(created_date, 'utf-8') 
				
				exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = created_date
				
				exif_bytes = piexif.dump(exif_dict)
				img.save(f"./Google Photos/photo_{str_int}/{b}", exif=exif_bytes)
					
			except PIL.UnidentifiedImageError as e:
				shutil.copy2(f"./Google Photos/{FL}/{b}", f"./Google Photos/videos/{b}") # move videos 
			
			except: 
				pass 
				
			i += 1
