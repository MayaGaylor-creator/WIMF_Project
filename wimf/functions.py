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

    validated_item = validate.ValidateGroceryItem(item_data)

    if validated_item is None:
        print("Failed to create grocery item.")
        return None

    storage.create_item(validated_item)
    print("Grocery item created successfully.")
    return validated_item