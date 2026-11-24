
from getpass import getpass

# MySQL connection settings
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DB = "WIMF"


def get_database_credentials():
    """Prompt the user for their MySQL login credentials."""

    print("\n--- WIMF Database Setup ---")

    username = input("MySQL username [root]: ").strip() or "root"
    password = getpass("MySQL password: ")

    return username, password
