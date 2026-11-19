from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

# 1. AI Chat Endpoint (/chat) 
class ChatRequest(BaseModel):
    question: str = Field(..., min_length=2, description="User's Qustions: ")

class ChatResponse(BaseModel):
    question: str
    answer: str
    sql_queries: List[str]

# 2. Retail Sales Table (15 Columns)
class SaleRecord(BaseModel):
    date: datetime                                  # datetime64[ns]
    store_id: str                                   # object
    product_id: str                                 # object
    category: str                                   # object
    region: str                                     # object
    inventory_level: int = Field(..., ge=0)         # int64
    units_sold: int = Field(..., ge=0)              # int64
    units_ordered: int = Field(..., ge=0)           # int64
    demand_forecast: float = Field(..., ge=0.0)     # float64
    price: float = Field(..., gt=0.0)               # float64
    discount: int = Field(..., ge=0, le=100)        # int64
    weather_condition: str                          # object
    holiday_promotion: int = Field(..., ge=0, le=1) # int64
    competitor_pricing: float = Field(..., gt=0.0)  # float64
    seasonality: str                                # object