import requests

def run_food_fetch(code: str) -> dict | None:
    params = {
    "fields": "product_name,quantity,stores"
    }
    headers = {
        "User-Agent": "FoodInventoryProj/1.0"}
    url = f'https://us.openfoodfacts.org/api/v2/product/{code}'


    print("Requesting live food data...")
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    print(f"Request URL: {response.url}")
    print(f"Status Code: {response.status_code}")

    response_dict = response.json()
    return response_dict if response_dict.get('status') == 1 else None


if __name__ == "__main__":
    code = input("Enter a barcode to fetch food data: ")
    result = run_food_fetch(code)
    print(result)