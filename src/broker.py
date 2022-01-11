import sqlite3 as sql

"""
   ABOUT CREATION OF DB
"""

RUTA = '../DB/responses.db'

def createDB():
    conn = sql.connect(RUTA)
    conn.commit()
    conn.close()

def createTables():
    conn = sql.connect(RUTA)
    cursor = conn.cursor()
    cursor.execute(
        """ CREATE TABLE whoIs (
            search text,
            result text,
            number_search integer
            )"""
        )
    cursor.execute(
        """ CREATE TABLE urls (
            url text
            )"""
    )
    cursor.execute(
        """
            CREATE TABLE images (
                id integer PRIMARY KEY AUTOINCREMENT,
                image_name text,
                image blob
            )
        """
    )
    conn.commit()
    conn.close()

"""
    REGARDING PEOPLE
"""

def insertRow(search, result, number_search):
    conn = sql.connect(RUTA)
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO whoIs VALUES ('{search}','{result}',{number_search})")
    conn.commit()
    conn.close()

def readRows():
    conn = sql.connect(RUTA)
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM whoIs")
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos

def readOrderedPeople():
    conn = sql.connect(RUTA)
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM whoIs ORDER BY number_search DESC")
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos[0]

def updatePeople(search, number):
    print(search)
    conn = sql.connect(RUTA)
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE whoIs SET number_search = {number} WHERE search = '{search}'")
    conn.commit()
    conn.close()

"""
    REGARDING URLS
"""
def readURL():
    conn = sql.connect(RUTA)
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM urls")
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos

def insertURL(url):
    conn = sql.connect(RUTA)
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO urls VALUES ('{url}')")
    conn.commit()
    conn.close()

#insertURL('https://en.wikipedia.org/wiki/')
"""
    IMAGE STORAGE
"""

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertImage(name, photo):
    try:
        conn = sql.connect(RUTA)
        cursor = conn.cursor()
    
        sqlite_insert_blob_query = """ INSERT INTO images
                                  (image_name, image) VALUES (?, ?)"""

        empPhoto = convertToBinaryData(photo)
        # Convert data into tuple format
        data_tuple = (name, empPhoto)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        conn.commit()

        conn.close()

    except sql.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if conn:
            conn.close()
        

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)


def readImage(url=f'../random/'):
    try:
        conn = sql.connect(RUTA)
        cursor = conn.cursor()

        sql_fetch_blob_query = """SELECT * FROM images ORDER BY RANDOM() LIMIT 1;"""
        row = cursor.execute(sql_fetch_blob_query)
        
        for item in row:
            
            name = item[1]
            photo = item[2]

            photoPath = f"{url}" + name + ".jpg"

            writeTofile(photo, photoPath)


        cursor.close()
        return photoPath

    except sql.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if conn:
            conn.close()
"""
    AUXILIAR FUNCTION TO DELETE ROWS
"""

def delete():
    conn = sql.connect("../DB/responses.db")
    cursor = conn.cursor()
    cursor.execute(
        f"DELETE FROM urls WHERE url='https://en.wikipedia.org'")
    conn.commit()
    conn.close()

#delete()