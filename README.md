# 🔐 Secure Password Manager

A simple yet secure password management application built with Python, using SQLite for storage, bcrypt for hashing, and Fernet encryption for securing passwords. Manage your sensitive information with ease and safety!

---

## 📜 Features

- **Master Password**: Protect access to your password database with a master password hashed using `bcrypt`.
- **Password Encryption**: All stored passwords are encrypted with `Fernet` to ensure data security.
- **Service-Based Storage**: Save and retrieve passwords based on services (e.g., Gmail, Facebook).
- **Interactive CLI**: User-friendly command-line interface with clear options.
- **Press Q to Quit**: Exit the application anytime by typing `Q`.
- **Search Functionality**: Search saved passwords by service name or username.

---

## 📁 Table Structure

### 1. Passwords Table
Stores service names, usernames, and encrypted passwords.
- `id` (Primary Key)
- `service` (Service name)
- `username` (Account username)
- `password` (Encrypted password)

### 2. Settings Table
Stores the master password hash and encryption key.
- `master_password` (Hashed master password)
- `key_string` (Encryption key used for securing passwords)

---

## 💻 Technologies Used

- **Python**: Core programming language.
- **SQLite**: Lightweight database for data storage.
- **bcrypt**: For secure master password hashing.
- **Fernet (Cryptography)**: For encrypting stored passwords.

---

## 🚀 How to Use

1. **Clone the repository**:
    ```bash
    git clone https://github.com/tonyrav3n/password-manager-tonyrav3n.git
    cd password-manager-tonyrav3n
    ```

2. **Set Up a Virtual Environment** *(Optional but recommended)*:
    ```bash
    python -m venv venv
    ```
    - **Activate the virtual environment**:
        - **Windows**:
            ```bash
            .\venv\Scripts\activate
            ```
        - **macOS/Linux**:
            ```bash
            source venv/bin/activate
            ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application**:
    ```bash
    python main.py
    ```

5. **Follow the prompts** to set up a master password and start managing your credentials!

---

## ⚠️ Disclaimer

This project is for educational purposes only. Always ensure sensitive data is handled with robust security practices in production environments.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
