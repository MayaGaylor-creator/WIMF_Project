
from pydantic import ValidationError
from wimf.schemas import GroceryItemCreate

def ValidateGroceryItem(item_data: dict) -> GroceryItemCreate | None:
    """Validate grocery item data and return a validated schema object."""

    # Convert empty optional fields into None
    optional_fields = [
        "GroceryItem_desc",
        "GroceryItem_stores",
        "GroceryItem_size"
    ]

    cleaned_data = item_data.copy()

    for field in optional_fields:
        if cleaned_data.get(field) == "":
            cleaned_data[field] = None

    # Validate data using the GroceryItemCreate schema
    try:
        grocery_item = GroceryItemCreate.model_validate(cleaned_data)

    except ValidationError as e:
        print("\n--- Grocery Item Validation Failed ---")

        for error in e.errors():
            field = error["loc"][0]
            message = error["msg"]
            print(f"{field}: {message}")

        return None

    # Additional business rules
    if not grocery_item.GroceryItem_name.strip():
        print("Product name cannot be empty.")
        return None

    if grocery_item.GroceryItem_location not in [
        "fridge", "frozen", "pantry"
    ]:
        print("Invalid storage location.")
        return None

    if grocery_item.GroceryItem_quantity > grocery_item.GroceryItem_max:
        print("Current quantity cannot exceed maximum quantity.")
        return None

    if grocery_item.GroceryItem_warning > grocery_item.GroceryItem_max:
        print("Warning threshold cannot exceed maximum quantity.")
        return None

    return grocery_item
