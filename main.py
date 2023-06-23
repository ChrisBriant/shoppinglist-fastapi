from typing import Union, List

from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app_database import Database
import os, dotenv

app = FastAPI()
basedir = os.path.abspath(os.path.dirname(__file__))

origins=['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


dotenv_file = os.path.join(basedir, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

#Models

class Item(BaseModel):
    name: str
    qty: int

class DBItem(BaseModel):
    id : int
    name: str
    qty: int

class ShoppingList(BaseModel):
    items: List[DBItem]

class ItemResponse(BaseModel):
    success: bool
    item: DBItem



@app.get("/shopping/getlist",response_model=ShoppingList)
def get_shopping_list():
    db_conn = Database()
    items = db_conn.get_list()
    shopping_list = {'items':items}
    return shopping_list

#DELETE
@app.delete("/shopping/deleteitem")
def delete_item(id: int, response: Response):
    db_conn = Database()
    rows_deleted = db_conn.delete_item(id)
    if rows_deleted > 0:
        response.status_code = 200
    else:
        response.status_code = 204
    return

#UPDATE METHODS

@app.put("/shopping/updateitem", response_model=ItemResponse)
def update_item(item: DBItem):
    db_conn = Database()
    rows_changed = db_conn.update_item(item)
    if rows_changed < 1:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"success": True, "item": item}

#CREATE METHODS
@app.post("/shopping/additem", response_model=ItemResponse)
def add_item(item: Item):
    db_conn = Database()

    id = db_conn.add_item(item)
    added_item = {
        'id' : id,
        'name' : item.name,
        'qty' : item.qty
    }
    return {"success": True, "item": added_item}
