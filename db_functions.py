import sqlite3


def put_abitur_into_db(id, sphere):
    con = sqlite3.connect('REA_DB.db')
    cur = con.cursor()

    cur.execute(f"INSERT INTO Users (id, Type, Sphere) VALUES ('{id}', 'abiturient', '{sphere}')")

    con.commit()


def put_student_into_db(id, faculty, branch):
    con = sqlite3.connect('REA_DB.db')
    cur = con.cursor()

    branch_id = cur.execute(f"SELECT id FROM Branches WHERE Faculty_id = "
                            f"(SELECT id FROM Faculties WHERE lower('{faculty}') = lower(Short_name)) "
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


def get_faculty(id):  # от id получаем всю инфу о факультете
    con = sqlite3.connect('REA_DB.db')
    cur = con.cursor()

    faculty_info = cur.execute(f"SELECT * FROM Faculties WHERE id = {id}").fetchall()[0]

    con.commit()

    return faculty_info


def get_branches(faculty_short_name):  # возвращает направления (список id)
    # без сортировки
    con = sqlite3.connect('REA_DB.db')
    cur = con.cursor()

    branches = cur.execute(f"SELECT Name FROM Branches "
                           f"WHERE  Faculty_id = "
                           f"(SELECT id FROM Faculties WHERE Short_name = '{faculty_short_name}')").fetchall()
    con.commit()

    branches = list([x[0] for x in branches])

    return branches


def get_brach_info(id):
    con = sqlite3.connect('REA_DB.db')
    cur = con.cursor()

    branch_info = cur.execute(f"SELECT * FROM Branches WHERE id = {id}").fetchall()[0]

    con.commit()

    return branch_info


def get_students(branch_id):  # возвращает список телеграм id студентов
    con = sqlite3.connect('REA_DB.db')
    cur = con.cursor()

    students = cur.execute(f"SELECT id FROM Users WHERE Branch_id = {branch_id}").fetchall()
    con.commit()

    students = list([x[0] for x in students])

    return students


def get_all_faculties():
    con = sqlite3.connect('REA_DB.db')
    cur = con.cursor()

    faculties = cur.execute(f"SELECT Short_name FROM Faculties").fetchall()
    con.commit()

    faculties = list([x[0] for x in faculties])
    return faculties


def get_all_spheres():
    con = sqlite3.connect('REA_DB.db')
    cur = con.cursor()

    spheres = cur.execute(f"SELECT DISTINCT Sphere FROM Branches").fetchall()
    con.commit()

    spheres = list([x[0] for x in spheres])
    return spheres


def user_in_db(id):
    con = sqlite3.connect('REA_DB.db')
    cur = con.cursor()
    result = cur.execute(f"SELECT * FROM Users WHERE id = '{id}'").fetchall()
    if result:
        return True
    return False
