import sqlite3
import os
from Tools.Ultilities import get_last_id
import numpy as np


def test():
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM Member ORDER BY id'):
        print(row[0])

    last = cur.execute('SELECT * FROM Member last_insert_rowid')
    last = cur.getCount() - 1
    print(last)
    print(cur.moveToFirst())


def add_member(name, username, password, birthday, position, phone_number, identification):

    conn = sqlite3.connect('data.db')
    id = int(get_last_id(conn, "Member")) + 1

    query = "INSERT INTO Member (id,name,username,password,birthday,position,phonenumber,identification) " \
            "VALUES(" + str(id) + ",'" + str(name) + "','" + str(username) + "','" + str(password) + "','" + str(birthday) \
            + "','" + str(position) + "','" + str(phone_number) + "','" + str(identification) + "')"

    conn.execute(query)
    conn.commit()
    conn.close()


def login(input_username, input_password):
    conn = sqlite3.connect('data.db')
    query = "SELECT * FROM Member WHERE username = '" + str(input_username) + "'"
    cursor = conn.execute(query)
    exist = 0
    for row in cursor:
        if type(row) == tuple:
            if str(row[3]) == str(input_password):
                exist = 1
    if exist == 1:
        return 'true', row[0]
    else:
        return 'false', "None"


def find_id(index):
    conn = sqlite3.connect('data.db')
    query = "SELECT * FROM Member WHERE ID = " + str(index)
    cursor = conn.execute(query)
    for row in cursor:
        return row


def all_member():
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    result = []

    for row in cur.execute("SELECT * FROM Member ORDER BY position"):
        result += row

    result = np.array(result)
    result = result.reshape(-1, 9)

    return result


def insertOrUpdate(id, name):
    conn = sqlite3.connect('../data.db')

    query = "SELECT * FROM People WHERE ID=" + str(id)
    cursor = conn.execute(query)

    isRecordExist = 0

    for row in cursor:
        isRecordExist = 1
    if isRecordExist == 1:
        query = "UPDATE People SET Name='" + str(name) + "' WHERE ID=" + str(id)
    else:
        query = "INSERT INTO People(ID,Name) VALUES(" + str(id) + ",'" + str(name) + "')"
    conn.execute(query)
    conn.commit()
    conn.close()