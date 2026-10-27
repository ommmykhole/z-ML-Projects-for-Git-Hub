from fastapi import FastAPI, Path, HTTPException, Query
import json 
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal


app = FastAPI()

class Product(BaseModel):
    id: Annotated[str, Field(... , description="Products Unique ID")]
    name: Annotated[str, Field(... , description="This Is Product Name")]
    category: Annotated[str, Field(... , description="This Is Product Category", examples=["Home"])]
    price: Annotated[float, Field(... , description="Product Price",gt=0)]
    stock: Annotated[int, Field(... , description="Available Stock Of Product", ge=0)]
    brand: Annotated[str, Field(... , description="Brand Name")]



def load_date():
    with open("product.json","r")as f:
        data = json.load(f)
    return data



def save_data(data):
    with open("product.json","w")as f:
        json.dump(data, f)







@app.post("/create")
def create_product(product: Product):
    data = load_date()
    
    if product.id in data:
        raise HTTPException(status_code=400, detail="Product Already Available")
        
    data[product.id] = product.model_dump(exclude=["id"])
    
    save_data(data)
    
    return JSONResponse(status_code=201, content={"Message":"Product Saved SuccessFully"})






@app.get("/")
def home():
    return {"Message":"Hello Customers This Is Our Home Page"}


with open("product.json", "r") as file:
    data = json.load(file)

@app.get("/Products")
def get_all_products():
    return data



@app.get("/products/{product_id}")
def get_product(product_id: str):
    
    if product_id in data:
        return data[product_id]
    
    raise HTTPException(status_code=401, detail="Product Not Found")
    
    


@app.get("/Category")
def get_product_category(category: str = None):
    
    if category:
        filtered_data = []
        
        for product in data.values():
            if product["category"].lower() == category.lower():
                filtered_data.append(product)
            
        return filtered_data
    
    return data






@app.get("/Product_sort")
def get_product_sort(
    category: str,
    price: float
):
    
    sorted_data = []
    
    
    for product in data.values():
        if(
            product["category"].lower() == category.lower()
            and product["price"] > price
        ):
            
            sorted_data.append(product)
        
    return sorted_data





@app.get("/chip_product")
def show_cheap_product():
    
    sorted_price = []
    
    
    for price in data.values():
        if price["price"]<=1000:
            sorted_price.append(price)
    
    return sorted_price




