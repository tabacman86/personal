import os
import sys
import time
import shutil
import datetime

def main(folder):
	if not os.path.isdir(folder):
		print("Not a folder")
		exit (1)
	for file in os.listdir(folder):
		filefullpath = os.path.join(folder,file)
		date = datetime.datetime.fromtimestamp(float(os.path.getmtime(filefullpath))).strftime("%d-%m-%Y")
		if not os.path.exists(os.path.join(folder,date)):
			newfolder = os.path.join(folder,date)
			os.makedirs(newfolder)
		os.rename(filefullpath,os.path.join(newfolder,file))
	

if __name__ == "__main__":
	main(sys.argv[1])