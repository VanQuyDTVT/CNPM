import sqlite3
import os
from Ultilities import get_last_id


def add_product(name, retail_price, cost_price):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    exist = False
    for row in cur.execute("SELECT * FROM Products WHERE name LIKE '" + name + "'"):
        exist = True
    if exist:
        return name + " exist!!"

    id = int(get_last_id(conn, "Products")) + 1
    amount = 0

    query = "INSERT INTO Products (id,name,amount,retail_price,cost_price) VALUES(" + str(id) + ",'" + str(name) \
            + "','" + str(amount) + "','" + str(retail_price) + "','" + str(cost_price) + "')"

    conn.execute(query)
    conn.commit()
    conn.close()
    return "Add successful"


def sell(id, amount, sold):
    conn = sqlite3.connect('data.db')

    query = "UPDATE Products SET amount='" + str(int(amount) - int(sold)) + "' WHERE ID=" + str(id)

    conn.execute(query)
    conn.commit()
    conn.close()
    return "Update successful"


def import_product(id, amount, add):
    conn = sqlite3.connect('data.db')

    query = "UPDATE Products SET amount='" + str(int(amount) + int(add)) + "' WHERE ID=" + str(id)

    conn.execute(query)
    conn.commit()
    conn.close()
    return "Update successful"


def export_product(id, amount, add):
    conn = sqlite3.connect('data.db')

    query = "UPDATE Products SET amount='" + str(int(amount) - int(add)) + "' WHERE ID=" + str(id)

    conn.execute(query)
    conn.commit()
    conn.close()
    return "Update successful"


def change_information_product(id, type_change, value_change):
    conn = sqlite3.connect('data.db')

    query = "UPDATE Products SET " + type_change + "='" + str(value_change) + "' WHERE ID=" + str(id)

    conn.execute(query)
    conn.commit()
    conn.close()
    return "Update successful"


def search(keyword):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    result = []
    for row in cur.execute("SELECT * FROM Products WHERE name LIKE '%" + keyword + "%'"):
        result += row
    con.commit()
    con.close()
    return result