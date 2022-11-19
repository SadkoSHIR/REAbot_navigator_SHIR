import sqlite3


def put_abitur_into_db(id, sphere, ege):
    con = sqlite3.connect('REA_DB.db')
    cur = con.cursor()

    ege = '8'.join(ege)

    cur.execute(f"INSERT INTO Users (id, Type, Sphere, EGE) VALUES ('{id}', 'abiturient', '{sphere}', '{ege}')")

    con.commit()
