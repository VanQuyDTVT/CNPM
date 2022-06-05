
def get_last_id(conn, table):
    last_id = 0
    cur = conn.cursor()
    for row in cur.execute('SELECT * FROM ' + str(table) + ' ORDER BY id DESC LIMIT 1'):
        last_id = row[0]

    return last_id


def get_id_bill():
    from datetime import datetime
    import sqlite3

    conn = sqlite3.connect('data.db')
    cur = conn.cursor()

    now = datetime.now()
    date = now.date()
    if len(str(date.month)) == 1:
        mm = "0" + str(date.month)
    else:
        mm = str(date.month)

    if len(str(date.day)) == 1:
        dd = "0" + str(date.day)
    else:
        dd = str(date.day)

    number = 0

    id_bill = str(date.year) + str(mm) + str(dd)

    for row in cur.execute("SELECT * FROM History WHERE id_bill LIKE '" + id_bill + "%'"):
        number += 1

    if number == 0:
        id_bill = str(date.year) + str(mm) + str(dd) + str(number)
    else:
        for row in cur.execute('SELECT * FROM History ORDER BY id DESC'):
            if row[3] not in {"Import", "Export"}:
                if row[2] == str(date.year) + "-" + str(mm) + "-" + str(dd):
                    id_bill = int(row[3]) + 1
                    return id_bill
    number = 0
    id_bill = str(date.year) + str(mm) + str(dd) + str(number)
    return id_bill

