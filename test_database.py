from sqlalchemy import inspect, text
from sqlalchemy.exc import OperationalError
from wimf.database import engine
from wimf.models import GroceryItem


def main():
    # Test the database connection
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT DATABASE()"))
            print("Connected to:", result.scalar())

    except OperationalError:
        print("\nUnable to connect to the WIMF database.")
        print("Please check your MySQL credentials and ensure")
        print("that MySQL Server is running.")
        return

    # Continue with the remaining tests if connection succeeds
    print("Python model:", GroceryItem.__tablename__)

    inspector = inspect(engine)
    print("MySQL tables:", inspector.get_table_names())


if __name__ == "__main__":
    main()
