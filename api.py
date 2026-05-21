import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from mssql_python import connect

# Load variables from .env file load
load_dotenv()
CONNECTION_STRING = os.getenv("SQL_CONNECTION_STRING")

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    in_stock: Optional[bool] = True

@app.get("/")
def home():
    return {"status": "Connected to Azure SQL API! Thanks"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    # Establish connection using context managers to cleanly close it afterward
    with connect(CONNECTION_STRING) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, price, in_stock FROM Items WHERE id = ?", (item_id,))
            row = cursor.fetchone()
            
            if not row:
                raise HTTPException(status_code=404, detail="Item not found in Azure SQL")
                
            return {
                "id": row[0],
                "name": row[1],
                "price": float(row[2]),
                "in_stock": bool(row[3])
            }

@app.post("/items/")
def create_item(item: Item):
    with connect(CONNECTION_STRING) as conn:
        with conn.cursor() as cursor:
            # Insert data safely using parameterized queries to block SQL injection
            sql = "INSERT INTO Items (name, price, in_stock) OUTPUT INSERTED.id VALUES (?, ?, ?)"
            cursor.execute(sql, (item.name, item.price, int(item.in_stock)))
            new_id = cursor.fetchone()[0]
            conn.commit() # Commit transaction to finalize the write
            
            return {
                "message": "Item stored in Azure SQL successfully", 
                "id": new_id, 
                "data": item.model_dump()
            }