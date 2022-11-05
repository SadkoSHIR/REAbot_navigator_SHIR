import sqlite3

class Database:
    def __int__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            self.cursor.execute(INSERT INTO 'Users' (id) VALUE (?),(user_id,))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'Usets' WHERE 'id' = ?", (user_id)).fatchall()
            return bool(len(result))