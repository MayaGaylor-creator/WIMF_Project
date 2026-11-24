import requests
import json
from pathlib import Path

code = input("Enter a barcode to fetch food data: ")

def run_food_fetch(code) -> dict:
    params = {
    "fields": "product_name,quantity,stores"
    }
    headers = {
        "User-Agent": "FoodInventoryProj/1.0"}
    url = f'https://us.openfoodfacts.org/api/v2/product/{code}'


    print("Requesting live food data...")
    response = requests.get(url, params=params, headers=headers)

    print(f"response:\n{response.text}")
    response_text = response.text
    response_dict = json.loads(response_text)

    print(type(response_dict))
    print("RESPONSE\n=================\n",response_dict,"\n=============================")


    print(f"Request URL: {response.url}")
    print(f"Status Code: {response.status_code}")

    output_file = Path("food_report.json")
    output_file.write_text(response.text, encoding="utf-8")
    print(f"Saved response to {output_file.name}. Open it and find the food!")
    return response_dict

run_food_fetch(code)