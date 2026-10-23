import json

from fastapi import FastAPI, Path, HTTPException, Query


app = FastAPI()


# ==================== LOAD PRODUCTS DATA ====================

with open("data.json", "r") as file:
    products = json.load(file)


# ==================== HOME ====================

@app.get("/")
def home():
    return {
        "Message": "This is Products Management Backend API"
    }


# ==================== ABOUT ====================

@app.get("/About")
def about():
    return {
        "Message": "This is Fully Functional API"
    }


# ==================== VIEW ALL PRODUCTS ====================

@app.get("/View")
def view_products():
    return products


# ==================== VIEW PRODUCT BY ID ====================

@app.get("/product/{product_id}")
def view_product(
    product_id: int = Path(
        ...,
        description="The Product ID Of Product",
        example=1
    )
):

    for product in products:

        if product["id"] == product_id:
            return product

    raise HTTPException(
        status_code=404,
        detail="Product Not Found"
    )


# ==================== SORT PRODUCTS ====================

@app.get("/Sort")
def sort_products(
    sort_by: str = Query(
        ...,
        description="Sort On The Basis Of Price, Stock, Rating"
    ),

    order: str = Query(
        "asc",
        description="Sort In ASC and DESC Order"
    )
):

    # Valid sorting fields
    valid_fields = ["Price", "Stock", "Rating"]


    # Check sorting field
    if sort_by not in valid_fields:

        raise HTTPException(
            status_code=400,
            detail=f"Invalid Field, Select From {valid_fields}"
        )


    # Check sorting order
    if order not in ["asc", "desc"]:

        raise HTTPException(
            status_code=400,
            detail="Invalid Order, Select Between asc and desc"
        )


    # Convert order into reverse=True / False
    sort_order = True if order == "desc" else False


    # Sort products
    sorted_data = sorted(
        products,
        key=lambda x: x.get(sort_by, 0),
        reverse=sort_order
    )


    return sorted_data