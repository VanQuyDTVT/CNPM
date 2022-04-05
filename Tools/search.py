import sqlite3
import numpy as np


def search(keyword):
    con = sqlite3.connect('./data.db')
    cur = con.cursor()
    result = []

    if keyword == "-view-stock":
        for row in cur.execute("SELECT * FROM Products ORDER BY amount"):
            result += row

    if keyword == "-all":
        for row in cur.execute("SELECT * FROM Products ORDER BY name"):
            result += row

    for row in cur.execute("SELECT * FROM Products WHERE name LIKE '%"+keyword+"%'"):
        result += row

    result = np.array(result)
    result = result.reshape(-1, 5)

    return result


def history(keyword):
    con = sqlite3.connect('./data.db')
    cur = con.cursor()
    result = []

    if keyword == "-view-history":
        for row in cur.execute("SELECT * FROM History ORDER BY id"):
            result += row

    elif keyword == "-shift-working":
        for row in cur.execute("SELECT * FROM History WHERE out_case LIKE '0'"):
            result += row

    elif keyword == "-shift-working-day":
        from datetime import datetime
        now = datetime.now()
        date = now.date()
        for row in cur.execute("SELECT * FROM History WHERE date LIKE '"+str(date)+"'"):
            result += row

    elif keyword == "-shift-working-month":
        from datetime import datetime
        now = datetime.now()
        date = now.date()
        if len(str(date.month)) == 1:
            mm = "0" + str(date.month)
        else:
            mm = str(date.month)

        for row in cur.execute("SELECT * FROM History WHERE date LIKE '"+str(date.year)+"-"+str(mm)+"-%'"):
            result += row

    else:
        for row in cur.execute("SELECT * FROM History WHERE name LIKE '%"+keyword+"%'"):
            result += row

    result = np.array(result)
    result = result.reshape(-1, 13)

    return result



# search('c')