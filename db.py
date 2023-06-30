import sqlite3


def create_db ():
    connection = sqlite3.connect('users.sql')
    cur = connection.cursor()
    cur.execute(
        f'CREATE TABLE IF NOT EXISTS users (id_user int AUTO_INCREMENT PRIMARY KEY, first_name varchar(50), '
        f'last_name varchar(50), user_id varchar(50), active int);')
    connection.commit()
    cur.close()
    connection.close()

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()


    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchmany(1)
            return bool(len(result))


    def add_user(self, first_name, last_name, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (first_name, last_name, user_id, active) VALUES (?,?,?,?)",
                                       (first_name, last_name, user_id, 1))

    def set_active(self, user_id, active):
        with self.connection:
            return self.cursor.execute("UPDATE users SET active = ? WHERE user_id = ?", (active, user_id))


    def get_user(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id, active  FROM users")


    def list_user(self):
        with self.connection:
            user_list = self.cursor.execute("SELECT * FROM users")
            info = ''
            for el in user_list:
                info += f'Имя: {el[1]}, Фамилия: {el[2]}, Чат ID: {el[3]}\n'
            return info


    def del_user(self, chat_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM users WHERE user_id = ?" (chat_id))
