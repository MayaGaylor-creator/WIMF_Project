
import csv
from pathlib import Path

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
