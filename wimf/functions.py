import csv
from pathlib import Path
from wimf import fetch, validate, storage

def FetchGroceryItemFromBarcode(barcode: str):
    """Fetch grocery item information using an OpenFoodFacts barcode."""

    response_dict = fetch.run_food_fetch(barcode)

    if response_dict is None:
        print(f"No product found for barcode: {barcode}")
        return None

    product = response_dict.get("product", {})

    product_name = product.get("product_name", "")
    quantity = product.get("quantity", "")
    stores = product.get("stores", "")

    return {
        "GroceryItem_name": product_name,
        "GroceryItem_size": quantity,
        "GroceryItem_stores": stores
    }

def ReviewFetchedData(product_data: dict) -> dict:
    """Allow the user to review and correct fetched product information."""

    reviewed_data = {}

    fields = {
        "GroceryItem_name": "Product name",
        "GroceryItem_size": "Package size",
        "GroceryItem_stores": "Stores"
    }

    for field, label in fields.items():
        fetched_value = product_data.get(field, "")

        print(f"\n{label}: {fetched_value or 'Not available'}")
        choice = input("Keep this value? (Y/N): ").strip().lower()

        if choice == "n":
            reviewed_data[field] = input(f"Enter {label.lower()}: ").strip()
        else:
            reviewed_data[field] = fetched_value

    return reviewed_data


def CreateGroceryItem(prefilled_data: dict | None = None):
    """Collect all grocery item attributes, using prefilled data when available."""

    if prefilled_data is None:
        prefilled_data = {}

    item_data = {}

    # Collect text and numeric attributes
    fields = {
        "GroceryItem_name": "Product name",
        "GroceryItem_desc": "Description",
        "GroceryItem_price": "Price",
        "GroceryItem_quantity": "Current inventory quantity",
        "GroceryItem_warning": "Low-stock warning threshold",
        "GroceryItem_max": "Maximum inventory quantity",
        "GroceryItem_stores": "Stores",
        "GroceryItem_size": "Package size"
    }

    for field, label in fields.items():
        existing_value = prefilled_data.get(field)

        if existing_value is not None and existing_value != "":
            item_data[field] = existing_value
        else:
            item_data[field] = input(f"{label}: ").strip()

    # Select storage location
    locations = {
        "1": "fridge",
        "2": "frozen",
        "3": "pantry"
    }

    print("\n--- Storage Location ---")
    print("1. Fridge")
    print("2. Freezer")
    print("3. Pantry")

    while True:
        choice = input("Select a location (1-3): ").strip()

        if choice in locations:
            item_data["GroceryItem_location"] = locations[choice]
            break

        print("Invalid selection. Please choose 1, 2, or 3.")

    return item_data


def AddItemFromBarcode():
    """Fetch, review, and prepare a grocery item for creation."""

    barcode = input("Enter product barcode: ")

    product_data = FetchGroceryItemFromBarcode(barcode)

    if product_data is None:
        return None

    reviewed_data = ReviewFetchedData(product_data)

    return CreateGroceryItem(reviewed_data)

def AddItemDecision():
    """Ask the user if they want to add a grocery item from a barcode."""

    choice1 = input("Do you want to add a grocery item from a barcode? (Y/N): ").strip().lower()

    if choice1 == "y":
        return AddItemFromBarcode()
    elif choice1 == "n":
        choice2 = input("Do you want to add a grocery item manually? (Y/N): ").strip().lower()
        if choice2 == "y":
            return CreateGroceryItem()
        else:
            print("No item added.")
            return None
    else:
        print("Invalid input. No item added.")
        return None

def ValidateAndSaveGroceryItem(item_data: dict):
    """Validate the grocery item data and save it to the database."""

    if item_data is not None:
        print("\n--- Grocery Item Validation ---")
        print(item_data)
        choice = input("Do you want to save this grocery item to the database? (Y/N): ").strip().lower()

        validated_item = validate.ValidateGroceryItem(item_data)

        if validated_item is None:
            print("Failed to create grocery item.")
            return None

        if choice == "y":
            storage.create_item(validated_item)
            print("Grocery item created successfully.")
            return validated_item
        else:
            print("Grocery item not saved.")
            return None

### VIEWING ITEMS ###

def ViewOneGroceryItem():
    """Retrieve and display one grocery item by ID."""

    try:
        item_id = int(input("Enter the GroceryItem ID: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        return None

    item = storage.get_item_by_id(item_id)

    if item is None:
        print(f"No grocery item found with ID {item_id}.")
        return None

    print("\n========== GROCERY ITEM ==========")
    print(f"ID:          {item.GroceryItem_id}")
    print(f"Name:        {item.GroceryItem_name}")
    print(f"Description: {item.GroceryItem_desc or 'N/A'}")
    print(f"Price:       ${item.GroceryItem_price}")
    print(f"Quantity:    {item.GroceryItem_quantity}")
    print(f"Low warning: {item.GroceryItem_warning}")
    print(f"Maximum:     {item.GroceryItem_max}")
    print(f"Location:    {item.GroceryItem_location}")
    print(f"Stores:      {item.GroceryItem_stores or 'N/A'}")
    print(f"Package size:{item.GroceryItem_size or 'N/A'}")
    print("==================================")

    return item


def ViewAllGroceryItems():
    """Export the entire grocery inventory to inventory.csv."""

    items = storage.get_all_items()

    output_file = Path(__file__).resolve().parent.parent / "inventory.csv"

    fields = [
        "GroceryItem_id",
        "GroceryItem_name",
        "GroceryItem_desc",
        "GroceryItem_price",
        "GroceryItem_quantity",
        "GroceryItem_warning",
        "GroceryItem_max",
        "GroceryItem_location",
        "GroceryItem_stores",
        "GroceryItem_size"
    ]

    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for item in items:
            writer.writerow(item.model_dump())

    print(f"\nInventory exported successfully!")
    print(f"Items exported: {len(items)}")
    print(f"File location: {output_file.resolve()}")

    return output_file

def ViewItemsDecision():
    """Ask the user if they want to view one item or all items."""

    choice = input("Do you want to view one item or all items? (one/all): ").strip().lower()

    if choice == "one":
        return ViewOneGroceryItem()
    elif choice == "all":
        return ViewAllGroceryItems()
    else:
        print("Invalid input. No items viewed.")
        return None

############## Editing Items

def EditGroceryItem():
    """Allow the user to edit an existing grocery item."""

    # Retrieve the item
    try:
        item_id = int(input("Enter the GroceryItem ID to edit: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        return None

    current_item = storage.get_item_by_id(item_id)

    if current_item is None:
        print(f"No grocery item found with ID {item_id}.")
        return None

    # Attributes available for editing
    fields = {
        "1": ("GroceryItem_name", "Product name"),
        "2": ("GroceryItem_desc", "Description"),
        "3": ("GroceryItem_price", "Price"),
        "4": ("GroceryItem_quantity", "Current inventory quantity"),
        "5": ("GroceryItem_warning", "Low-stock warning threshold"),
        "6": ("GroceryItem_max", "Maximum inventory quantity"),
        "7": ("GroceryItem_location", "Storage location"),
        "8": ("GroceryItem_stores", "Stores"),
        "9": ("GroceryItem_size", "Package size")
    }

    # Store requested changes here
    changes = {}

    while True:
        print(f"\n========== EDITING: {current_item.GroceryItem_name} ==========")

        for number, (field, label) in fields.items():
            current_value = changes.get(
                field,
                getattr(current_item, field)
            )
            print(f"{number}. {label}: {current_value or 'N/A'}")

        print("0. Finish editing")

        choice = input("\nSelect an attribute to edit: ").strip()

        if choice == "0":
            break

        if choice not in fields:
            print("Invalid selection. Please choose a number from 0-9.")
            continue

        field, label = fields[choice]

        # Handle storage location separately
        if field == "GroceryItem_location":
            locations = {
                "1": "fridge",
                "2": "frozen",
                "3": "pantry"
            }

            print("\n1. Fridge")
            print("2. Freezer")
            print("3. Pantry")

            location_choice = input("Select a location (1-3): ").strip()

            if location_choice not in locations:
                print("Invalid location selection.")
                continue

            new_value = locations[location_choice]

        else:
            new_value = input(f"Enter new {label.lower()}: ").strip()

        # Store the requested change
        changes[field] = new_value

        print(f"{label} updated in pending changes.")

    # Nothing was changed
    if not changes:
        print("No changes were made.")
        return current_item

    # Validate the complete updated item
    validated_changes = validate.ValidateGroceryItemUpdate(
        current_item,
        changes
    )

    if validated_changes is None:
        print("Update cancelled. No changes were saved.")
        return None

    # Save changes to the database
    updated_item = storage.update_item(
        item_id,
        validated_changes
    )

    if updated_item is None:
        print("Failed to update grocery item.")
        return None

    print("\nGrocery item updated successfully!")
    return updated_item

#### Delete items
def DeleteGroceryItem():
    """Delete an existing grocery item after user confirmation."""

    # Retrieve the item
    try:
        item_id = int(input("Enter the GroceryItem ID to delete: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        return None

    item = storage.get_item_by_id(item_id)

    if item is None:
        print(f"No grocery item found with ID {item_id}.")
        return None

    # Display item information
    print("\n========== GROCERY ITEM ==========")
    print(f"ID:          {item.GroceryItem_id}")
    print(f"Name:        {item.GroceryItem_name}")
    print(f"Description: {item.GroceryItem_desc or 'N/A'}")
    print(f"Price:       ${item.GroceryItem_price}")
    print(f"Quantity:    {item.GroceryItem_quantity}")
    print(f"Low warning: {item.GroceryItem_warning}")
    print(f"Maximum:     {item.GroceryItem_max}")
    print(f"Location:    {item.GroceryItem_location}")
    print(f"Stores:      {item.GroceryItem_stores or 'N/A'}")
    print(f"Package size:{item.GroceryItem_size or 'N/A'}")
    print("==================================")

    # Request confirmation
    print("\nAre you sure you want to delete this item?")
    print("1. Yes, delete item")
    print("2. No, cancel")

    choice = input("Select an option (1-2): ").strip()

    if choice == "1":
        deleted = storage.delete_item(item_id)

        if deleted:
            print(f"\n{item.GroceryItem_name} successfully deleted.")
            return True

        print("Failed to delete grocery item.")
        return False

    elif choice == "2":
        print("Deletion cancelled.")
        return False

    else:
        print("Invalid selection. Deletion cancelled.")
        return False
    