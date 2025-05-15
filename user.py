import hashlib
import sqlite3
import base64

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self._id = self.set_id()

    # Why is this set ID? Its verifying the password you dummy
    def set_id(self):
        conn = sqlite3.connect("passwords.db")
        cur = conn.cursor()

        try:
            u = cur.execute(f"SELECT * FROM users where username='{self.username}';")
            u = u.fetchone()
            conn.close()
            if self.password == u[2]:
                return u[0]
            else:
                return -777
        except Exception as e:
            conn.close()
            return -777

    def generate_key(self):
        if len(self.password) % 2 == 0 and all(c in "0123456789abcdefABCDEF" for c in self.password):
            key_bytes = bytes.fromhex(self.password)
            base64_key = base64.urlsafe_b64encode(key_bytes)
        else:
            base64_key = self.password.encode("utf-8")
        
        padding_needed = len(base64_key) % 4
        if padding_needed != 0:
            base64_key += b"=" * (4-padding_needed)

        return base64_key



    def __str__(self):
        return f"{self.username}: hashed_password -> {self.password}"
