import hashlib
import sqlite3

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self._id = self.set_id()


    def set_id(self):
        conn = sqlite3.connect("passwords.db")
        cur = conn.cursor()

        try:
            u = cur.execute(f"SELECT * FROM users where username='{self.username}';")
            u = u.fetchone()
            conn.close()
            print(f"u0 = {u[0]}\nu1 = {u[1]}\nu2 = {u[2]}\n")
            if self.password == u[2]:
                return u[0]
            else:
                return -777
        except Exception as e:
            conn.close()
            return -777

    def __str__(self):
        return f"{self.username}: hashed_password -> {self.password}"