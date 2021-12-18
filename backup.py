import pyodbc
import datetime
import pymongo
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

connSqlServer = pyodbc.connect(driver='{SQL Server Native Client 11.0}',
                               server='127.0.0.1,1433',
                               database='master',
                               uid='sa',pwd='your_password',
                               autocommit=True)

log_time = datetime.datetime.now().strftime("%d%m%y_%H%M%S")

log_name = f'programming-in-db_log_{log_time}'

backup = f"BACKUP LOG [programming-in-db] TO DISK= N'C:\kaniku_backup\{log_name}.bak'"
cursor = connSqlServer.cursor().execute(backup)

connSqlServer.close()  # close the connection

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["prod"]

mycol = mydb["log_name_mdb"]

mydict = {"log_name": log_name}

x = mycol.insert_one(mydict)

print(x.inserted_id)

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

upload_file_list = [f'/kaniku_backup/{log_name}.bak']
for upload_file in upload_file_list:
    gfile = drive.CreateFile({'parents': 
    [{'id': '1dB8qNwSgEtaivSl3aKc3de4ZBiynaCpn'}]})
    gfile.SetContentFile(upload_file)
    gfile.Upload() #Upload file

file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format('1dB8qNwSgEtaivSl3aKc3de4ZBiynaCpn')}).GetList()
for file in file_list:
    print('title: %s, id: %s' %(file['title'], file['id']))