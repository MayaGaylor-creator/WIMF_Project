from sqlmodel import Session, select

# ==========================================================
# >>> ADDED FOR DATA FLOW (START)
# ==========================================================
# The functions below use three names that used to sit in the same file.
# Each now lives in its own module, so each must be imported here:
#
#   engine        <- database.py : the connection to the SQLite file.
#                                  Both save and print use this ONE shared
#                                  engine, so they talk to the same database.
#   GroceryItem <- models.py   : the table blueprint. Used to build a row
#                                  to save, and to tell select() which table
#                                  to read.
#   GroceryItemCreate, GroceryItemUpdate <- schemas.py  : the type of the object this module
#                                  RECEIVES from validate.py (via main.py).
#                                  Used in the type hint of
#                                  save_weather_report().
from wimf.database import engine
from wimf.models import GroceryItem
from wimf.schemas import GroceryItemCreate, GroceryItemUpdate # only for the type hint; not actually used
# ==========================================================
# <<< ADDED FOR DATA FLOW (END)
# ==========================================================

def get_all_items() -> list[GroceryItem]:
    """Return all GroceryItem rows in the database."""
    with Session(engine) as session:
        return session.exec(select(GroceryItem)).all()

def get_item_by_id(item_id: int) -> GroceryItem | None:
    """Return a GroceryItem row by its ID, or None if not found."""
    with Session(engine) as session:
        return session.get(GroceryItem, item_id)

def create_item(item: GroceryItemCreate) -> GroceryItem:
    """Create a new GroceryItem row in the database."""
    record = GroceryItem(
        GroceryItem_name=item.GroceryItem_name,
        GroceryItem_desc=item.GroceryItem_desc,
        GroceryItem_price=item.GroceryItem_price,
        GroceryItem_quantity=item.GroceryItem_quantity,
        GroceryItem_warning=item.GroceryItem_warning,
        GroceryItem_max=item.GroceryItem_max,
        GroceryItem_location=item.GroceryItem_location,
        GroceryItem_stores=item.GroceryItem_stores,
        GroceryItem_size=item.GroceryItem_size
    )

    with Session(engine) as session:
        session.add(record)
        session.commit()
        session.refresh(record)
        print(f"Record saved to DB: {record}")
    return record

def update_item(item_id: int, item: GroceryItemUpdate) -> GroceryItem | None:
    """Update an existing GroceryItem row in the database."""
    with Session(engine) as session:
        record = session.get(GroceryItem, item_id)
        if record is None:
            return None
        for field, value in item.model_dump(exclude_unset=True).items():
            setattr(record, field, value)
        session.add(record)
        session.commit()
        session.refresh(record)
        print(f"Record updated in DB: {record}")
    return record

def delete_item(item_id: int) -> bool:
    """Delete a GroceryItem row from the database."""
    with Session(engine) as session:
        record = session.get(GroceryItem, item_id)
        if record is None:
            return False
        session.delete(record)
        session.commit()
        print(f"Record deleted from DB: {record}")
    return True

# 5.4 Print the DB contents
def print_db():
    with Session(engine) as session:
        records = session.exec(select(GroceryItem)).all()
        for record in records:
            print(record)