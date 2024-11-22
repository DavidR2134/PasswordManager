from user import User
import sqlite3
import getpass
import os
import pyfiglet
from cryptography.fernet import Fernet
import base64
from datetime import datetime

db = "passwords.db"

def create_database(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()    
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL);")
    cur.execute("CREATE TABLE IF NOT EXISTS password(id INTEGER PRIMARY KEY AUTOINCREMENT, company_name TEXT NOT NULL, password BLOB NOT NULL, last_updated TEXT NOT NULL, userID INTEGER, CONSTRAINT fk_users FOREIGN KEY (userID) REFERENCES users(id));")
    conn.commit()
    conn.close()

    print("DB Created.")

def create_user(user):
    conn = sqlite3.connect("passwords.db")
    cur = conn.cursor()

    try:
        data = cur.execute(f"SELECT * FROM users WHERE username='{user.username}';")
        if len(data.fetchall()) == 0:
            cur.execute(f"INSERT INTO users(username, password) values ('{user.username}', '{user.password}');")
            conn.commit()
        else:
            print("Username is taken.")
    except Exception as e:
        print(f"Error: {e}")
    
    conn.close()

def login():
    u = input("Username: ")
    p = getpass.getpass("Password: ")

    user = User(u,p)

    if user._id != -777:
        return user
    else:
        clear()
        print("Invalid Username or Password")
        return False

def clear():
    os.system('clear')

def print_menu(isLoggedIn):
    t = pyfiglet.figlet_format("Password Manager")
    clear()
    if isLoggedIn == False:
        print(t)
        print("\tby David Rogers\n")
        print("1) Login")
        print("2) Create User")
        print("3) Quit")
    else:
        print(t)
        print("\tby David Rogers\n")
        print("1) Show Passwords")
        print("2) Add Password")
        print("3) Update Password")
        print("4) Delete Password")
        print("5) Logout")

def fetch_passwords(user):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    try:
        data = cur.execute(f"SELECT company_name as company, password, last_updated FROM password WHERE userID={user._id}")
        data = data.fetchall()

        show_passwords(data, user)
        conn.close()
    except Exception as e:
        print(e)

def show_passwords(data, user):
    key = user.generate_key()
    cipher = Fernet(key)

    print("+" + "-" * len(f"| {data[0][0]} | {cipher.decrypt(data[0][1]).decode()} | {data[0][2]} |") + "+")
    for i in range(len(data)):
        print(f"| {data[i][0]} | {cipher.decrypt(data[i][1]).decode()} | {data[i][2]} |" )
    print("+" + "-" * len(f"| {data[0][0]} | {cipher.decrypt(data[0][1]).decode()} | {data[0][2]} |") + "+")

def add_password(user):
    key = user.generate_key()
    cipher = Fernet(key)
    company_name = input("Please enter a company: ")
    passwd = cipher.encrypt(getpass.getpass("Please enter the password: ").encode())

    conn = sqlite3.connect(db)
    cur = conn.cursor()

    try:
        cur.execute(f"""INSERT INTO password(company_name, password, last_updated, userID) 
                    VALUES(?,?,?,?);""", (company_name, passwd, str(datetime.now()), user._id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        conn.close()    



def delete_password(user):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    company_name = input("Please enter the company associated with the password you'd like to delete: ")

    try:
        cur.execute(f"DELETE FROM password WHERE company_name='{company_name}' AND userID={user._id}")
        conn.commit()
        print(f"{company_name} has been deleted.")
    except Exception as e:
        print(f"{company_name} could not be deleted:")
        print(e)

    
    conn.close()
    

def update_password(user):
    # UPDATE password SET password={new_password} WHERE company_name='{company_name}' AND userID={user._id};
    key = user.generate_key()
    cipher = Fernet(key)
    company_name = input("Please enter a company: ")
    new_passwd = cipher.encrypt(getpass.getpass("Please enter the new password: ").encode())

    conn = sqlite3.connect(db)
    cur = conn.cursor()

    try:
        cur.execute(f"""UPDATE password SET password=?, last_updated=? where company_name=? AND userID=?;""", (new_passwd, str(datetime.now()), company_name, user._id))
        conn.commit()
        print("Password has been updated successfully!")
        conn.close()
    except Exception as e:
        print("UNABLE TO UPDATE:")
        print(e)
        conn.close()  


def main():
    user = None
    try:
        test = open("passwords.db", 'rb')
    except:
        create_database(db)


    isLoggedIn = False
    while True:
        print_menu(isLoggedIn)
        choice = int(input("> "))

        if not isLoggedIn:
            if choice == 1:
                clear()
                user = login()
                if user != False:
                    isLoggedIn = True
            elif choice == 2:
                clear()
                u = input("Please enter a username: ")
                p = getpass.getpass("Please enter a password: ")
                p2 = getpass.getpass("Please confirm password: ")

                if p == p2:
                    user = User(u, p)
                    create_user(user)
                    input()
                else:
                    print("Passwords do not match.")
                    input("Press enter to continue...")
                    print_menu(isLoggedIn)
            elif choice == 3:
                clear()
                print("Quitting...")
                break
        else:
            if choice == 1:
                clear()
                fetch_passwords(user)
                input("Please press enter to coninue...")   
            elif choice == 2:
                clear()
                add_password(user)
                input("Please press enter to coninue...")
            elif choice == 3:
                clear()
                update_password(user)
                input("Please press enter to coninue...")
            elif choice == 4:
                clear()
                delete_password(user)
                input("Please press enter to coninue...")
            elif choice == 5:
                isLoggedIn = False


if __name__ == "__main__":
    main()