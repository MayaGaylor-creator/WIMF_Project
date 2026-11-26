from wimf import fetch, storage, schemas

def AddGroceryItemFromBarcode(barcode: str):
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

if __name__ == "__main__":
    barcode = input("Enter a barcode to fetch food data: ")
    product_data = AddGroceryItemFromBarcode(barcode)

    if product_data:
        reviewed_data = ReviewFetchedData(product_data)
        print("\nFinal reviewed data:")
        for key, value in reviewed_data.items():
            print(f"{key}: {value}")