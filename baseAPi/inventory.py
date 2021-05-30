from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional  # Recommend by fastAPI when using option parameter
from pydantic import BaseModel

app = FastAPI()

inventory = {}
ErrorDetails = {
    "ITEM_NOT_FOUND" : "Item Not found",
    "ITEM_ALREADY_EXISTS": "Item Already Exists"
}
class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


@app.get("/get-item/{item_id}")
def get_item(
    item_id: int = Path(None, description="The ID of the item you'd like to view"),
    gt=0
):  # FastAPI will automatically return a message when they tupe if item-id is not int
    if item_id not in inventory:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=ErrorDetails["ITEM_NOT_FOUND"])
    return inventory[item_id]


@app.get("/get-by-name/{item_id}")
def get_by_name(item_id: int, name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id].name.lower() == name.lower():
            return inventory[item_id]

    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=ErrorDetails["ITEM_NOT_FOUND"])


@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail=ErrorDetails["ITEM_ALREADY_EXISTS"])

    inventory[item_id] = item #{"name": item.name, "brand": item.brand, "price": item.price}
    return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND)

    if item.name != None:
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].price = item.price
    if item.brand != None:
        inventory[item_id].brand = item.brand
    return inventory[item_id]


@app.delete('/delete-item/{item_id}')
def delete_item(item_id: int = Query(..., description="The ID of item to be deleted")):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail=ErrorDetails["ITEM_NOT_FOUND"])
    del inventory[item_id]
    return {"Success": "Item deleted"}
