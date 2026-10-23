from fastapi import FastAPI

# 1. Initialization
app = FastAPI()

# 2. Routing (Main Gate)
@app.get("/")
def welcome_api():
    # 3. Response
    return {"Message": "Welcome to Shivnetra Analytics Backend!", "Status": "Active"}