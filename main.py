import sqlite3
import bcrypt
from cryptography.fernet import Fernet


def initialize_db():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS passwords 
    (
    id INTEGER PRIMARY KEY,
    service TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
    )
    """
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS settings 
    (
    master_password TEXT,
    key_string TEXT
    )
    """
    )

    conn.commit()
    conn.close()


def create_master_password():
    master_password = str(get_input("Set a master password:\n>"))
    hashed = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt())

    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO settings (master_password) VALUES (?)", (hashed,))
    conn.commit()
    conn.close()
    print("\nSuccessfully created a master password!")


def verify_master_password():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()

    cursor.execute("SELECT master_password FROM settings")
    result = cursor.fetchone()

    if not result:
        create_master_password()
    else:
        master_password = str(input("Enter your master password:\n>"))
        if not bcrypt.checkpw(master_password.encode(), result[0]):
            print("Incorrect master password!")
            exit(1)


def load_key():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()

    cursor.execute("SELECT key_string FROM settings")
    result = cursor.fetchone()
    if result[0] is None:
        key = Fernet.generate_key()
        cursor.execute("UPDATE settings set key_string = ?", (key,))
        conn.commit()
        conn.close()
    else:
        key = result[0]

    return key


def get_input(prompt=""):
    user_input = input(prompt).strip().lower()
    if user_input == "q":
        print("\nExiting Password Manager...")
        exit(0)
    return user_input


def save_password(cipher):
    name = get_input("\nEnter the service name:\n>")
    usn = get_input("\nEnter the username:\n>")
    pwd = get_input("\nEnter the password:\n>")
    encrypted_pwd = cipher.encrypt(pwd.encode()).decode()

    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO passwords (service, username, password) VALUES (?, ?, ?)",
        (name, usn, encrypted_pwd),
    )
    conn.commit()
    conn.close()
    print("\nSuccessfully saved password!")
    get_input("\nPress ENTER to continue...\n>")


def retrieve_passwords(cipher):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT service, username, password FROM passwords")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        print("\nNo saved passwords.")
    else:
        print("\nSAVED PASSWORDS")
        for service, username, password in rows:
            password = cipher.decrypt(password.encode()).decode()
            print(f"\nService: {service}\nUsername: {username}\nPassword: {password}")
        get_input("\nPress ENTER to continue...\n>")


def main():
    initialize_db()
    print("\nPress Q anywhere to quit.\n")
    verify_master_password()
    key = load_key()
    cipher = Fernet(key)

    while True:
        mode = get_input("\n1. add a new password \n2. view existing ones\n>")

        if mode == "1":
            save_password(cipher)

        elif mode == "2":

            retrieve_passwords(cipher)

        else:
            print("Invalid input.")
            continue


if __name__ == "__main__":
    main()
