import sqlite3 as sql

def createDB():
    conn = sql.connect("responses.db")
    conn.commit()
    conn.close()

def createTable():
    conn = sql.connect("responses.db")
    cursor = conn.cursor()
    cursor.execute(
        """ CREATE TABLE whoIs (
            search text,
            result text,
            number_search integer
            )"""
        )
    conn.commit()
    conn.close()

def insertRow(search, result, number_search):
    conn = sql.connect("responses.db")
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO whoIs VALUES ('{search}','{result}',{number_search})")
    conn.commit()
    conn.close()

def readRows():
    conn = sql.connect("responses.db")
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM whoIs")
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    print(datos)

if __name__ == "__main__":
    #createDB()
    #createTable()
    #insertRow("Bill Gates","William Henry Gates III (Seattle, Washington; 28 de octubre de 1955)," 
    #                "mejor conocido como Bill Gates (AFI: [bil gejts]), es un empresario, informático"
    #               "y filántropo estadounidense, conocido por haber creado y fundado junto con Paul Allen,"
    #               "la empresa Microsoft. De igual forma es conocido por haber creado, también con Paul Allen,"
    #               "el sistema operativo para computadoras Windows.", 1)
    readRows()