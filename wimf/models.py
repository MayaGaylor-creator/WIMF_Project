# models.py
# Original code from section "3. Database table" - moved as-is.
# DEFINITIONS layer: describes the shape of the database table. Imports
# nothing from the project.

from decimal import Decimal
from sqlmodel import Field, SQLModel

# =================================================
# 3. Database table (SQLModel) - only what we want to store
# =================================================
# WHY A SEPARATE CLASS? In a SQLModel table (table=True), EVERY field becomes
# a column. Field(sa_column=None) does NOT exclude a field, because None is
# already the default. The clean way to store only some fields is to keep the
# API shape (CurrentWeather above) separate from the table shape (below).


class GroceryItem(SQLModel, table=True):
    __tablename__ = "GroceryItem"

    GroceryItem_id: int | None = Field(default=None, primary_key=True)

    GroceryItem_name: str = Field(max_length=25)
    GroceryItem_desc: str | None = Field(default=None, max_length=125)
    GroceryItem_price: Decimal = Field(max_digits=10, decimal_places=2)
    GroceryItem_quantity: int
    GroceryItem_warning: int
    GroceryItem_max: int
    GroceryItem_location: str = Field(max_length=10)
    GroceryItem_stores: str | None = Field(default=None, max_length=255)
    GroceryItem_size: str | None = Field(default=None, max_length=50)