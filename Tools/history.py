import sqlite3
import numpy as np
from Tools.Ultilities import get_last_id


def add_history(id_bill, name, amount, price, discount, tax, seller, out_case=False, export=False, note=""):
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


def shift_case(id):
    conn = sqlite3.connect('data.db')

    query = "UPDATE History SET out_case=True WHERE ID=" + str(id)

    conn.execute(query)
    conn.commit()
    conn.close()
    return "Update successful"


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


def bill_in_time_custom(y_s, m_s, d_s, y_e, m_e, d_e, h_s=None, mn_s=None, h_e=None, mn_e=None):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    history_data = []

    for row in cur.execute("SELECT * FROM History ORDER BY id"):
        time_start = y_s * 31 * 12 + m_s * 31 + d_s
        time_end = y_e * 31 * 12 + m_e * 31 + d_e
        time_row = int(row[2][0:4]) * 31 * 12 + int(row[2][5:7]) * 31 + int(row[2][8:10])

        if (time_row >= time_start) and (time_row <= time_end):
            if h_s is None:
                history_data += row
            else:
                time_start = time_start * 3600 + int(h_s) * 60 + int(mn_s)
                time_end = time_end * 3600 + int(h_e) * 60 + int(mn_e)
                time_row = time_row * 3600 + int(row[1][0:2]) * 60 + int(row[1][3:5])

                if (time_row >= time_start) and (time_row <= time_end):
                    history_data += row

    history_data = np.array(history_data)
    history_data = history_data.reshape(-1, 13)

    return history_data


def search(keyword):
    con = sqlite3.connect('data.db')
    cur = con.cursor()
    result = []
    for row in cur.execute("SELECT * FROM History WHERE name LIKE '%" + keyword + "%'"):
        result += row

    return result
