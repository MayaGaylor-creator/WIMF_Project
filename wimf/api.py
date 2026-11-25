# api.py
# Run from the project root:
# uvicorn wimf.api:app
#
# Interactive API documentation:
# http://127.0.0.1:8000/docs

from fastapi import FastAPI, HTTPException
from wimf import storage
from wimf.database import init_db
from wimf.schemas import (
    GroceryItemCreate,
    GroceryItemUpdate,
    GroceryItemRead,
)


app = FastAPI(title="WIMF API")


init_db()



@app.get("/items", response_model=list[GroceryItemRead])
def list_items():
    return storage.get_all_items()



@app.get("/items/{item_id}", response_model=GroceryItemRead)
def get_item(item_id: int):
    item = storage.get_item_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Grocery item not found")
    return item



@app.post("/items", response_model=GroceryItemRead, status_code=201)
def create_item(data: GroceryItemCreate):
    return storage.create_item(data)


@app.patch("/items/{item_id}", response_model=GroceryItemRead)
def update_item(item_id: int, data: GroceryItemUpdate):
    item = storage.update_item(item_id, data)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Grocery item not found"
        )

    return item


# DELETE /items/{item_id} - Delete a grocery item
@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    deleted = storage.delete_item(item_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Grocery item not found"
        )
