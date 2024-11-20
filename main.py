from user import User
import sqlite3
import getpass
import os
#import pyfiglet


def create_user(user):
    conn = sqlite3.connect("passwords.db")
    cur = conn.cursor()

    try:
        cur.execute(f"INSERT INTO users(username, password) values ('{user.username}', '{user.password}');")
        conn.commit()
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
    #t = pyfiglet.figlet_format("Password Manager")
    t = "Password Manager"
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

isLoggedIn = False
while True:
    print_menu(isLoggedIn)
    choice = int(input("> "))

    if not isLoggedIn:
        if choice == 1:
            user = login()
            if user != False:
                isLoggedIn = True
        elif choice == 2:
            u = input("Please enter a username: ")
            p = getpass.getpass("Please enter a password: ")
            p2 = getpass.getpass("Please confirm password: ")

            if p == p2:
                user = User(u, p)
                create_user(user)
            else:
                print("Passwords do not match.")
                input("Press enter to continue...")
                print_menu(isLoggedIn)
        elif choice == 3:
            print("Quitting...")
            break
    else:
        print("Logged in")

