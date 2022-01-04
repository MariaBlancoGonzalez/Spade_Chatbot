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
    return datos

def readOrderedPeople():
    conn = sql.connect("responses.db")
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM whoIs ORDER BY number_search DESC")
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos[0]

def updatePeople(search, number):
    print(search)
    conn = sql.connect("responses.db")
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE whoIs SET number_search = {number} WHERE search = '{search}'")
    conn.commit()
    conn.close()
