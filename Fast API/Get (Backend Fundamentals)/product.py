from fastapi import FastAPI

app = FastAPI()

@app.get("/products/{product_id}")
def get_product(product_id: int):
    return {"Product ID": product_id}