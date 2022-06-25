from ftplib import FTP
import shutil, os
from datetime import datetime

from CLIENT.client import BACKUP_LOGIN
ftp = FTP('172.20.20.35')
ftp.login('siege','siege')

folder = f'{datetime.now():%m_%d_%Y-%H_%M_%S}'
print(folder)
os.makedirs(folder)

files = ftp.nlst()

for file in files:
	ftp.retrbinary("RETR " + file ,open("BACKUP/" + BACKUP_LOGIN + "/" + folder + "/" + file, 'wb').write)

shutil.make_archive(folder, 'zip', folder)
shutil.rmtree(folder)
ftp.close()