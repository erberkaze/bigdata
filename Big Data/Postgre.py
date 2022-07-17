import psycopg2
from PIL import Image, ImageStat
from PIL import ImageChops
import pandas as pd
import psycopg2

csv= pd.read_csv('D:/data/labels/trainLabels19.csv')
csv2= pd.read_csv('D:/data/labels/trainLabels15.csv')

lst = []
for i in csv["id_code"]:
    i = i + ".jpg"

    lst.append(i)

for l in csv2["image"]:
    l = l + ".jpg"
    lst.append(l)

from os import listdir
from os.path import isfile, join

path = "D:/projeeeee/Resimler"

k = [f for f in listdir(path) if isfile(join(path, f))]

hostname = 'localhost'
database = 'postgres'
username = 'postgres'
pwd = 'a6e810da'
port_id = 5432

conn = None
cur = None

try:
    conn = psycopg2.connect(

        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id
    )

    cur = conn.cursor() # operation'lar için

    create_script = ''' CREATE TABLE IF NOT EXISTS labeled2015 (
    
                        photoName    varchar(50) NOT NULL,
                        diseaseType  int
    )
    
    '''

    create_script2 = ''' CREATE TABLE IF NOT EXISTS labeled2019 (

                            photoName    varchar(50) NOT NULL,
                            diseaseType  int
    )

    '''
    create_script3 = ''' CREATE TABLE IF NOT EXISTS type0 (

                                photoName    varchar(50) NOT NULL,
                                diseaseType  int
        )

    '''
    create_script4 = ''' CREATE TABLE IF NOT EXISTS type1 (

                                    photoName    varchar(50) NOT NULL,
                                    diseaseType  int
            )

    '''
    create_script5 = ''' CREATE TABLE IF NOT EXISTS type2 (

                                        photoName    varchar(50) NOT NULL,
                                        diseaseType  int
                )

    '''
    create_script6 = ''' CREATE TABLE IF NOT EXISTS type3 (

                                    photoName    varchar(50) NOT NULL,
                                    diseaseType  int
            )

    '''
    create_script7 = ''' CREATE TABLE IF NOT EXISTS type4 (

                                        photoName    varchar(50) NOT NULL,
                                        diseaseType  int
                )

    '''

    create_script8 = ''' CREATE TABLE IF NOT EXISTS allLabeled (

                                            photoName    varchar(50) NOT NULL,
                                            diseaseType  int
                    )

    '''

    cur.execute(create_script)
    cur.execute(create_script2)
    cur.execute(create_script3)
    cur.execute(create_script4)
    cur.execute(create_script5)
    cur.execute(create_script6)
    cur.execute(create_script7)
    cur.execute(create_script8)


    insert_script = 'COPY labeled2019 FROM \'D:/data/labels/trainLabels19.csv\' DELIMITER \',\' CSV HEADER;'
    insert_script2 = 'COPY labeled2015 FROM \'D:/data/labels/trainLabels15.csv\' DELIMITER \',\' CSV HEADER;'

    insert_script3 = """
                    INSERT INTO type0 (photoName, diseaseType)
                    SELECT *
                    from labeled2015
                    where diseasetype = 0
                    union
                    SELECT *
                    from labeled2019
                    where diseasetype = 0
    """
    insert_script4 = """
                        INSERT INTO type1 (photoName, diseaseType)
                        SELECT *
                        from labeled2015
                        where diseasetype = 1
                        union
                        SELECT *
                        from labeled2019
                        where diseasetype = 1
    """
    insert_script5 = """
                        INSERT INTO type2 (photoName, diseaseType)
                        SELECT *
                        from labeled2015
                        where diseasetype = 2
                        union
                        SELECT *
                        from labeled2019
                        where diseasetype = 2
    """
    insert_script6 = """
                        INSERT INTO type3 (photoName, diseaseType)
                        SELECT *
                        from labeled2015
                        where diseasetype = 3
                        union
                        SELECT *
                        from labeled2019
                        where diseasetype = 3
    """
    insert_script7 = """
                            INSERT INTO type4 (photoName, diseaseType)
                            SELECT *
                            from labeled2015
                            where diseasetype = 4
                            union
                            SELECT *
                            from labeled2019
                            where diseasetype = 4
    """
    insert_script8 = """
                                INSERT INTO alllabeled (photoName, diseaseType)
                                SELECT * 
                                FROM labeled2019
                                UNION
                                SELECT * 
                                FROM labeled2015;
    """

    cur.execute(insert_script)
    cur.execute(insert_script2)
    cur.execute(insert_script3)
    cur.execute(insert_script4)
    cur.execute(insert_script5)
    cur.execute(insert_script6)
    cur.execute(insert_script7)
    cur.execute(insert_script8)

    conn.commit()

    insert_script9 = """
                                    SELECT
                                    Count(*)
                                    from
                                    alllabeled
    """
    cur.execute(insert_script9)

    insert_script10 = """
                    SELECT * 
                    from labeled2015 
                    union
                    SELECT * 
                    from labeled2019 
    """
    cur.execute(insert_script10)

    records = cur.fetchall()

    dct = {}

    for row in records:
        dct[row[0]] = row[1]

    dct_list = list(dct)

    for i in range(len(dct_list)):
        dct_list[i] = dct_list[i] + ".jpg"



    buf = []
    buf.append(["", 1])

    import os

    ct = 0
    myct = 0
    ct2 = 386
    ct3 = 0
    ct4 = 10
    print("%0")
    for i in k:

        im1 = Image.open(f"Resimler/{i}")
        for j in dct_list:
            myct = myct + 1
            if(myct > ct2):
                ct2 = ct2 + 386
                if(ct3 > ct4):
                    print("%" + str(ct4))
                    ct4 = ct4 + 10
                ct3 = ct3 + 1

            if (os.path.exists(f"D:/data/resized train 15/{j}")):

                im2 = Image.open(f"D:/data/resized train 15/{j}")

            elif (os.path.exists(f"D:/data/resized train 19/{j}")):

                im2 = Image.open(f"D:/data/resized train 19/{j}")

            else:
                print("Error!!!!!!!!!!!!!")

            diff = ImageChops.difference(im2, im1)

            stat = ImageStat.Stat(diff)
            diff_ratio = sum(stat.mean) / (len(stat.mean) * 255)
            if (diff_ratio < buf[ct][1]):
                buf[ct] = [j, diff_ratio]

        print(buf)
        break
    ct = ct + 1
    print("Bitti")

    sql_var = buf[0][0].replace('.jpg', '').replace('', '')


    sql_type = dct.get(sql_var)

    sql_var = "SELAMM"

    if(sql_type == 0):

        postgres_insert_query = """ INSERT INTO type0 (photoname, diseasetype) VALUES (%s,%s)"""
        record_to_insert = (sql_var, sql_type)

    elif(sql_type == 1):

        postgres_insert_query = """ INSERT INTO type1 (photoname, diseasetype) VALUES (%s,%s)"""
        record_to_insert = (sql_var, sql_type)

    elif(sql_type == 2):

        postgres_insert_query = """ INSERT INTO type2 (photoname, diseasetype) VALUES (%s,%s)"""
        record_to_insert = (sql_var, sql_type)

    elif(sql_type == 3):

        postgres_insert_query = """ INSERT INTO type3 (photoname, diseasetype) VALUES (%s,%s)"""
        record_to_insert = (sql_var, sql_type)

    elif(sql_type == 4):

        postgres_insert_query = """ INSERT INTO type4 (photoname, diseasetype) VALUES (%s,%s)"""
        record_to_insert = (sql_var, sql_type)

    else:
        print("ARE YOU SURE MAN COME ON!!!!")

    cur.execute(postgres_insert_query, record_to_insert)
    conn.commit()


    print("DONE!")
except Exception as error:
    print(error)

finally:
    if(cur != None):
        cur.close()

    if(conn != None):
        conn.close()
