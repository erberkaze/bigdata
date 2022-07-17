import tkinter as tk
from tkinter.filedialog import askopenfilename
import time

import pymongo #install dnspython

import os
import gridfs
import io
from PIL import Image
import pymongo #install dnspython

import os
import gridfs
import io
import psycopg2


from tkinter import *

print("Lütfen sistemi başlatmak için 1 giriniz: ")

x = int(input())

if(x == 1):

    print("Şimdi sizden yükleyeceğiniz dosyayı seçmenizi isteyeceğiz.")
    print("----------------------------------------------------------")
    time.sleep(3)

    filename = askopenfilename()
    print("MongoDB'ye yüklenecek kaynak -> " + filename)
    print("\t\t\t\t\tOnaylıyor musunuz?")
    y = input()
    if(y == "evet" or "Evet" or "Yes" or "yes"):
        print("----------------------------------------------------------")
        print("File Mongo'ya yüklenmeye başlamıştır...")

        client = pymongo.MongoClient(
            "mongodb+srv://erberkaze:a6e810da@atlascluster.mgqjf.mongodb.net/?retryWrites=true&w=majority")
        db = client["database"]
        collection = db["fs.files"]

        fs = gridfs.GridFS(db)
        with open(f"{filename}", "rb") as imageFile:
            str = imageFile.read()
        fs = gridfs.GridFS(db)
        fs.put(str, filename= filename)
        print("Dosya yüklenmiştir.")
        print("----------------------------------------------------------")
        print("Dosya sırasıyla train'e ve benzerlik testine sokulacaktır.")
        print("----------------------------------------------------------")
        print("Sonuç: ")

        hostname = 'localhost'
        database = 'postgres'
        username = 'postgres'
        pwd = 'a6e810da'
        port_id = 5432

        conn = None
        cur = None

        try:

            conn = psycopg2.connect(

                host=hostname,
                dbname=database,
                user=username,
                password=pwd,
                port=port_id
            )
            cur = conn.cursor()

            query = """
            
                    SELECT *
                    from type0
                    where photoname = 'SELAMM'
                    union
                    SELECT *
                    from type1
                    where photoname = 'SELAMM'
                    union
                    SELECT *
                    from type2
                    where photoname = 'SELAMM'
                    union
                    SELECT *
                    from type3
                    where photoname = 'SELAMM'
                    union
                    SELECT *
                    from type4
                    where photoname = 'SELAMM'
                    
            """


            cur.execute(query)

            records = cur.fetchall()

            if(records[0][1] == 0):
                print("HASTA DEĞİLSİNİZ GEÇMİŞ OLSUN!")
            elif (records[0][1] == 1):
                print("HASTALIK BAŞLANGICI OLABİLİR DOKTORA GÖRÜNÜN!")
            elif (records[0][1] == 2):
                print("ERKEN AŞAMA HASTASI OLMA İHTİMALİNİZ VAR DOKTORA GÖRÜNÜN!")
            elif (records[0][1] == 3):
                print("NORMAL-İLERİ DÜZEY HASTA OLMA İHTİMALİNİZ ÇOK YÜKSEK DOKTORA GÖRÜNÜN!")
            elif (records[0][1] == 4):
                print("İLERİ DÜZEY - ACİL HASTA OLMA İHTİMALİNİZ ÇOK YÜKSEK DOKTORA GÖRÜNÜN!")
            else:
                print("ERRRROOOOOOOOOORRRRRRRR!!!!")

            print(records)



        except Exception as error:
            print(error)

        finally:
            if (cur != None):
                cur.close()

            if (conn != None):
                conn.close()
