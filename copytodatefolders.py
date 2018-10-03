import os
import sys
import datetime

def main(folder):
	if not os.path.isdir(folder):
		print("Not a folder")
		exit (1)
	for file in os.listdir(folder):
		filefullpath = os.path.join(folder,file)
		date = datetime.datetime.fromtimestamp(float(os.path.getmtime(filefullpath))).strftime("%d-%m-%Y")
		if not os.path.exists(os.path.join(folder,date)):
			newfolder_base = os.path.join(folder,date)
			os.makedirs(newfolder_base)
		filename = str(file)
		if filename.endswith('.jpg'):
			try:
				newfolder = os.path.join(newfolder_base,'JPG')
				os.makedirs(newfolder)
			except:
				pass
		else:
			try:
				newfolder = os.path.join(newfolder_base, 'MOV')
				os.makedirs(newfolder)
			except:
				pass
		os.rename(filefullpath,os.path.join(newfolder,file))
	

if __name__ == "__main__":
	main(sys.argv[1])
