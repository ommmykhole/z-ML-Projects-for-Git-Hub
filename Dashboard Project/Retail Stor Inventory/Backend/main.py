from fastapi import FastAPI
import pandas as pd
from sqlalchemy import create_engine
from typing import List
from schema import RetailItem  # Our New File

app = FastAPI(title="Shivnetra Industries Backend API")

# MySQL Connection 
engine = create_engine("mysql+pymysql://root:Shivnetra%402026@localhost/retail")

# Get EndPoint
@app.get("/api/get_retail_data", response_model=List[RetailItem])
def get_retail_data():
    query = "SELECT * FROM retail_data"
    df = pd.read_sql(query, engine)
    
    # Convert Data to Dataframe
    return df.to_dict(orient="records")