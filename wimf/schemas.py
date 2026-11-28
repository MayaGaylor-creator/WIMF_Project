from pydantic import BaseModel, Field
from decimal import Decimal
# =================================================
# 2. Validation Models
# =================================================

class GroceryItemCreate(BaseModel):
    GroceryItem_name: str = Field(max_length=75)
    GroceryItem_desc: str | None = Field(default=None, max_length=125)
    GroceryItem_price: Decimal = Field(ge=0)
    GroceryItem_quantity: int = Field(ge=0)
    GroceryItem_warning: int = Field(ge=0)
    GroceryItem_max: int = Field(gt=0)
    GroceryItem_location: str = Field(max_length=10)
    GroceryItem_stores: str | None = Field(default=None, max_length=255)
    GroceryItem_size: str | None = Field(default=None, max_length=50)

class GroceryItemUpdate(BaseModel):
    GroceryItem_name: str | None = Field(default=None, max_length=75)
    GroceryItem_desc: str | None = Field(default=None, max_length=125)
    GroceryItem_price: Decimal | None = Field(default=None, ge=0)
    GroceryItem_quantity: int | None = Field(default=None, ge=0)
    GroceryItem_warning: int | None = Field(default=None, ge=0)
    GroceryItem_max: int | None = Field(default=None, gt=0)
    GroceryItem_location: str | None = Field(default=None, max_length=10)
    GroceryItem_stores: str | None = Field(default=None, max_length=255)
    GroceryItem_size: str | None = Field(default=None, max_length=50)

class GroceryItemRead(BaseModel):
    model_config = {"from_attributes": True}
    GroceryItem_id: int
    GroceryItem_name: str = Field(max_length=75)
    GroceryItem_desc: str | None = None
    GroceryItem_price: Decimal
    GroceryItem_quantity: int
    GroceryItem_warning: int
    GroceryItem_max: int
    GroceryItem_location: str = Field(max_length=10)
    GroceryItem_stores: str | None = None
    GroceryItem_size: str | None = None