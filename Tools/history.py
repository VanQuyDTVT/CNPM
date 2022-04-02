import sqlite3
import numpy as np
from Tools.Ultilities import get_last_id


def add_history(id_bill, name, amount, price, discount, tax, seller, out_case=False, export=False, note=""):
    from Tools import history
    from datetime import datetime

    conn = sqlite3.connect('data.db')
    # cur = conn.cursor()
    id = get_last_id(conn, "History") + 1

    now = datetime.now()
    date = now.date()
    time = now.time()
    # if len(str(date.month)) == 1:
    #     mm = "0" + str(date.month)
    # else:
    #     mm = str(date.month)
    #
    # if len(str(date.day)) == 1:
    #     dd = "0" + str(date.day)
    # else:
    #     dd = str(date.day)

    # number = len(history.bill_in_date(str(date)))

    # id_bill = str(date.year) + str(mm) + str(dd) + str(number)

    query = "INSERT INTO History (id, time, date, id_bill, name, amount, " \
            "price, discount, tax, seller, out_case, export, note) " \
            "VALUES(" + str(id) + ",'" + str(time) + "','" + str(date) + "','" + str(id_bill) + "','" + str(name) + \
            "','" + str(amount) + "','" + str(price) + "','" + str(discount) + "','" + str(tax) + "','" + str(seller) \
            + "'," + str(out_case) + "," + str(export) + ",'" + note + "')"

    conn.execute(query)
    conn.commit()
    conn.close()
    return "Add successful"


def detail_bill(id_bill):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    result = []
    for row in cur.execute("SELECT * FROM History WHERE id_bill LIKE '" + id_bill + "'"):
        result += row

    result = np.array(result)
    result = result.reshape(-1, 13)

    return result


def detail_bill(id_bill):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    result = []
    for row in cur.execute("SELECT * FROM History WHERE id_bill LIKE '" + id_bill + "'"):
        result += row

    result = np.array(result)
    result = result.reshape(-1, 13)

    return result


def bill_in_date(date):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    result = []
    for row in cur.execute("SELECT * FROM History WHERE date LIKE '" + date + "'"):
        result += row

    result = np.array(result)
    result = result.reshape(-1, 13)

    return result


def bill_in_case():
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    result = []
    for row in cur.execute("SELECT * FROM History WHERE out_case LIKE 'FALSE'"):
        result += row

    result = np.array(result)
    result = result.reshape(-1, 13)

    return result

# def bill_in_year():


def search(keyword):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    result = []
    for row in cur.execute("SELECT * FROM History WHERE name LIKE '%" + keyword + "%'"):
        result += row

    return result
