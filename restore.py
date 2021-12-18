import pyodbc
import pymongo
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format('1dB8qNwSgEtaivSl3aKc3de4ZBiynaCpn')}).GetList()

for file1 in file_list:
    if file1['title'] == 'Log':
        folder_id = '1dB8qNwSgEtaivSl3aKc3de4ZBiynaCpn'

for i, file1 in enumerate(sorted(file_list, key = lambda x: x['title']), start=1):
    print('Downloading {} from GDrive ({}/{})'.format(file1['title'], i, len(file_list)))
    file1.GetContentFile(file1['title'])

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["prod"]

mycol = mydb["log_name_mdb"]

get_one = mycol.find_one()

get_value = get_one.get('log_name')

connSqlServer = pyodbc.connect(driver='{SQL Server Native Client 11.0}',
                               server='127.0.0.1,1432',
                               database='master',
                               uid='sa',pwd='your_password',
                               autocommit=True)

restore = f"RESTORE LOG [programming-in-db] FROM  DISK = N'C:\get_tbd\{get_value}.bak' WITH  STANDBY = 'C:\Program Files\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQL\DATA\programming-in-db_rollback_undo.bak'"
cursor = connSqlServer.cursor()
cursor.execute(restore)
while cursor.nextset():
    pass

cursor.close()  # close the connection