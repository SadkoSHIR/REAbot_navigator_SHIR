import sqlite3


def put_abitur_into_db(id, sphere, ege):
    con = sqlite3.connect('REA_DB.db')
    cur = con.cursor()

    ege = '8'.join(ege)

    cur.execute(f"INSERT INTO Users (id, Type, Sphere, EGE) VALUES ('{id}', 'abiturient', '{sphere}', '{ege}')")

    con.commit()


def put_student_into_db(id, faculty, branch):
    con = sqlite3.connect('REA_DB.db')
    cur = con.cursor()

    branch_id = cur.execute(f"SELECT id FROM Branches WHERE Faculty_id = "
                            f"(SELECT id FROM Faculties WHERE lower('{faculty}') = lower(Name)) "
                            f"AND lower('{branch}') = lower(Branches.Name)").fetchone()[0]

    cur.execute(f"INSERT INTO Users (id, Type, Branch_id) VALUES ('{id}', 'student', '{branch_id}')")

    con.commit()


def get_recomendations(id):  # возвращает факультеты (список id)
    con = sqlite3.connect('REA_DB.db')
    cur = con.cursor()

    recomends = cur.execute(f"SELECT DISTINCT Faculties.id FROM Faculties, Branches "
                            f"WHERE Faculties.id = Branches.Faculty_id AND "
                            f"(SELECT Sphere FROM Users WHERE id = {id}) = Branches.Sphere").fetchall()
    con.commit()

    recomends = list([x[0] for x in recomends])

    return recomends
