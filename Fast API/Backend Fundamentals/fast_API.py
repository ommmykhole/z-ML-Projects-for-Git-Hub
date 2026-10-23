from fastapi import FastAPI

app = FastAPI()

@app.get("/")

def home():
    return {"Sales": 150000}




@app.get("/orders")

def get_orders():
    return {"Total Orders": 250}