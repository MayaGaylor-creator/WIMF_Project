
import csv
from pathlib import Path
from decimal import Decimal
from wimf import storage


def GenerateLocationReports():
    """Generate separate CSV inventory reports for each storage location."""

    # Retrieve all grocery items
    items = storage.get_all_items()

    # Create the Reports directory if it doesn't exist
    report_directory = Path(__file__).resolve().parent.parent / "Reports"
    report_directory.mkdir(parents=True, exist_ok=True)

    # CSV column headings
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

    # Locations and their corresponding report filenames
    locations = {
        "fridge": "InventoryFridge.csv",
        "frozen": "InventoryFreezer.csv",
        "pantry": "InventoryPantry.csv"
    }

    print("\n--- Generating Inventory Reports ---")

    for location, filename in locations.items():

        # Select items belonging to this location
        location_items = [
            item for item in items
            if item.GroceryItem_location == location
        ]

        output_file = report_directory / filename

        # Create or replace the CSV file
        with output_file.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()

            for item in location_items:
                writer.writerow(item.model_dump())

        print(f"{filename}: {len(location_items)} items exported.")

    print(f"\nReports saved to: {report_directory.resolve()}")

    return report_directory


def GenerateLowStockReport():
    """Generate a CSV report of grocery items at or below their warning threshold."""

    # Retrieve all grocery items
    items = storage.get_all_items()

    # Identify items requiring replenishment
    low_stock_items = [
        item for item in items
        if item.GroceryItem_quantity <= item.GroceryItem_warning
    ]

    # Create the Reports directory if necessary
    report_directory = Path(__file__).resolve().parent.parent / "Reports"
    report_directory.mkdir(parents=True, exist_ok=True)

    output_file = report_directory / "LowStock.csv"

    fields = [
        "GroceryItem_id",
        "GroceryItem_name",
        "GroceryItem_size",
        "GroceryItem_quantity",
        "GroceryItem_warning",
        "GroceryItem_location"
    ]

    # Create or replace the CSV file
    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for item in low_stock_items:
            writer.writerow({
                field: getattr(item, field)
                for field in fields
            })

    print("\n--- Low Stock Report Generated ---")
    print(f"Items requiring replenishment: {len(low_stock_items)}")
    print(f"Report saved to: {output_file.resolve()}")

    return output_file
### Create Grocery List

from decimal import Decimal


def GenerateShoppingList():
    """Create a shopping list and export it to a CSV report."""

    print("\n--- Generate Shopping List ---")

    shopping_items = []
    used_ids = set()

    # Ask how many distinct items to include.
    while True:
        try:
            item_count = int(input("How many different items are you shopping for? "))
            if item_count <= 0:
                print("Please enter a number greater than zero.")
                continue
            break
        except ValueError:
            print("Please enter a valid whole number.")

    # Collect each item.
    while len(shopping_items) < item_count:

        try:
            item_id = int(input("\nEnter a GroceryItem ID: "))
        except ValueError:
            print("Please enter a valid numeric ID.")
            continue

        if item_id in used_ids:
            print("That item is already on your shopping list. Choose another ID.")
            continue

        item = storage.get_item_by_id(item_id)

        if item is None:
            print(f"No grocery item found with ID {item_id}.")
            continue

        print(f"\nItem: {item.GroceryItem_name}")
        print(f"Current quantity: {item.GroceryItem_quantity}")
        print(f"Maximum quantity: {item.GroceryItem_max}")
        print(f"Unit price: ${item.GroceryItem_price:.2f}")

        # Ask how many units the user intends to purchase.
        while True:
            try:
                purchase_quantity = int(
                    input("Quantity to buy: ")
                )

                if purchase_quantity <= 0:
                    print("Quantity must be greater than zero.")
                    continue

                break

            except ValueError:
                print("Please enter a valid whole number.")

        # Warn if the purchase exceeds the item's maximum.
        projected_quantity = (
            item.GroceryItem_quantity + purchase_quantity
        )

        if projected_quantity > item.GroceryItem_max:
            print(
                f"\nWarning: This purchase would bring "
                f"{item.GroceryItem_name} to {projected_quantity}, "
                f"exceeding its maximum of {item.GroceryItem_max}."
            )

            while True:
                confirmation = input(
                    "Do you want to include this purchase anyway? (y/n): "
                ).strip().lower()

                if confirmation == "y":
                    break
                elif confirmation == "n":
                    print("Purchase removed. Please enter another quantity.")
                    purchase_quantity = None
                    break
                else:
                    print("Please enter y or n.")

            if purchase_quantity is None:
                continue

        line_total = (
            Decimal(str(item.GroceryItem_price))
            * purchase_quantity
        )

        shopping_items.append({
            "GroceryItem_id": item.GroceryItem_id,
            "GroceryItem_name": item.GroceryItem_name,
            "Unit Price": item.GroceryItem_price,
            "Current Quantity": item.GroceryItem_quantity,
            "Maximum Quantity": item.GroceryItem_max,
            "Quantity to Buy": purchase_quantity,
            "Total Price": line_total
        })

        used_ids.add(item_id)

        print(f"Added {item.GroceryItem_name} to the shopping list.")

    # Calculate the grand total.
    grand_total = sum(
        (item["Total Price"] for item in shopping_items),
        Decimal("0.00")
    )

    # Create the Reports directory if it does not exist.
    report_directory = Path(__file__).resolve().parent.parent / "Reports"
    report_directory.mkdir(parents=True, exist_ok=True)

    output_file = report_directory / "ShoppingList.csv"

    fields = [
        "GroceryItem_id",
        "GroceryItem_name",
        "Unit Price",
        "Current Quantity",
        "Maximum Quantity",
        "Quantity to Buy",
        "Total Price"
    ]

    # Write the shopping list to CSV.
    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for item in shopping_items:
            csv_item = item.copy()

            # Keep monetary values at two decimal places.
            csv_item["Unit Price"] = f'{item["Unit Price"]:.2f}'
            csv_item["Total Price"] = f'{item["Total Price"]:.2f}'

            writer.writerow(csv_item)

        # Add the grand total as the final row.
        writer.writerow({
            "GroceryItem_name": "GRAND TOTAL",
            "Total Price": f"{grand_total:.2f}"
        })

    print(f"\nShopping list complete! Grand total: ${grand_total:.2f}")
    print(f"Report saved to: {output_file.resolve()}")

    return output_file


