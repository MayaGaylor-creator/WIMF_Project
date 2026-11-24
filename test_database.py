from sqlalchemy import inspect, text
from wimf.database import engine
from wimf.models import GroceryItem


def main():
    # Test the database connection
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT DATABASE()")
        )
        print("Connected to:", result.scalar())

    # Check whether SQLModel recognizes our table
    print("Python model:", GroceryItem.__tablename__)

    # Check which tables MySQL actually contains
    inspector = inspect(engine)
    print("MySQL tables:", inspector.get_table_names())


if __name__ == "__main__":
    main()
