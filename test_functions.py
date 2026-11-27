
# test_functions.py
# Tests the functions contained in wimf/functions.py

from wimf import functions, reports



if __name__ == "__main__":
### CREATES ITEM ###
    var = functions.AddItemDecision()
    functions.ValidateAndSaveGroceryItem(var)
##### VIEW ITEMS ###
#    functions.ViewItemsDecision()
##### EDIT ITEMS ###
#    functions.EditGroceryItem()
### DELETE ITEMS ###
#    functions.DeleteGroceryItem()
# Report 1 Location Report
    reports.GenerateLocationReports()
# Report 2 Low Report
    reports.GenerateLowStockReport()