
# test_functions.py
# Tests the functions contained in wimf/functions.py

from wimf import functions


if __name__ == "__main__":
    var = functions.AddItemDecision()
    print(var)
    print(functions.ValidateAndSaveGroceryItem(var))