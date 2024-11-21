import os

import bcrypt
from cryptography.fernet import Fernet


def create_master_password():
    master_password = get_input("Set a master password:\n>")
    hashed = bcrypt.hashpw(master_password.encode(), bcrypt.gensalt())

    with open("master_password.txt", "wb") as file:
        file.write(hashed)

    print("\nSuccessfully created a master password!")


def verify_master_password():
    if not os.path.exists("master_password.txt"):
        create_master_password()
    else:
        with open("master_password.txt", "rb") as file:
            stored_hash = file.read()
        master_password = input("Enter your master password:\n>")
        if not bcrypt.checkpw(master_password.encode(), stored_hash):
            print("Incorrect master password!")
            exit(1)


def load_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("key.key", "rb") as key_file:
            key = key_file.read()

    return key


def get_input(prompt=""):
    user_input = input(prompt).strip().lower()
    if user_input == "q":
        print("\nExiting Password Manager...")
        exit(0)
    return user_input


def add(fer):
    name = get_input("\nEnter the service name:\n>")
    usn = get_input("\nEnter the username:\n>")
    pwd = get_input("\nEnter the password:\n>")

    with open("passwords.txt", "a") as f:
        f.write(f"{name} | {usn} | {fer.encrypt(pwd.encode()).decode()}\n")
        print(f"\nPassword saved for {name}.")


def view(fer):
    if not os.path.exists("passwords.txt"):
        print("\nNo saved passwords.")
    else:
        with open("passwords.txt", "r") as f:
            for line in f.readlines():
                name, usn, pwd = line.strip().split(" | ")
                print(
                    f"\nService: {name}\nUsername: {usn}\nPassword: {fer.decrypt(pwd.encode()).decode()}"
                )
            get_input("\nPress ENTER to continue...\n>")


def main():
    print("\nPress Q anywhere to quit.\n")
    verify_master_password()
    key = load_key()
    cipher = Fernet(key)

    while True:
        mode = get_input("\n1. add a new password \n2. view existing ones\n>")

        if mode == "1":
            add(cipher)

        elif mode == "2":
            view(cipher)

        else:
            print("Invalid input.")
            continue


if __name__ == "__main__":
    main()
