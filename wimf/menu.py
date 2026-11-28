from wimf import functions, reports


def MainMenu():
    """Display the main WIMF menu and handle user selections."""

    while True:
        print("\n====================================")
        print("       WHAT'S IN MY FRIDGE?")
        print("====================================")
        print("\n--- MAIN MENU ---")
        print("1. Add grocery item")
        print("2. View grocery items")
        print("3. Edit grocery item")
        print("4. Delete grocery item")
        print("5. Generate reports")
        print("0. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            print("Add grocery item selected.")
            item_data = functions.AddItemDecision()

            if item_data is not None:
                functions.ValidateAndSaveGroceryItem(item_data)
        
        elif choice == "2":
            functions.ViewItemsDecision()

        elif choice == "3":
            functions.EditGroceryItem()

        elif choice == "4":
            functions.DeleteGroceryItem()
            
        elif choice == "5":
            ReportsMenu()

        elif choice == "0":
            print("\nThank you for using WIMF. Goodbye!")
            break

        else:
            print("\nInvalid selection. Please choose an option from the menu.")


def ReportsMenu():
    """Display the reports submenu and handle user selections."""

    while True:
        print("\n====================================")
        print("          REPORTS MENU")
        print("====================================")
        print("1. Generate location inventory reports")
        print("2. Generate low-stock report")
        print("3. Generate shopping list")
        print("0. Return to main menu")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            reports.GenerateLocationReports()

        elif choice == "2":
            reports.GenerateLowStockReport()

        elif choice == "3":
            reports.GenerateShoppingList()

        elif choice == "0":
            break

        else:
            print("\nInvalid selection. Please choose an option from the menu.")

