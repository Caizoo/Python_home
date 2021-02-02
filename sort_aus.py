import os 
import shutil 
import itertools

files = os.listdir("./Aus") 

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)
    

files = list(grouper(50, files)) 
files = [list(filter(lambda a: not a==None, b)) for b in files]



for i in range(len(files)):
	str_folder = "./aus_" + "{:02d}".format(i)
	os.mkdir(str_folder) 
	
	for f in files[i]:
		shutil.copy2(f"./Aus/{f}", f"{str_folder}/{f}") 
	
