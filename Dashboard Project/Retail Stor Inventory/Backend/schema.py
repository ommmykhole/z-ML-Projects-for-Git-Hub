from pydantic import BaseModel, Field

class RetailItem(BaseModel):
    # Standard columns 
    Date: str
    Category: str
    Region: str
    Price: float
    Discount: float
    Seasonality: str
    
    # Columns in Alias Format
    Store_ID: str = Field(..., alias="Store ID")
    Product_ID: str = Field(..., alias="Product ID")
    Inventory_Level: float = Field(..., alias="Inventory Level")
    Units_Sold: int = Field(..., alias="Units Sold")
    Units_Ordered: int = Field(..., alias="Units Ordered")
    Demand_Forecast: float = Field(..., alias="Demand Forecast")
    Weather_Condition: str = Field(..., alias="Weather Condition")
    Holiday_Promotion: int = Field(..., alias="Holiday/Promotion")
    Competitor_Pricing: float = Field(..., alias="Competitor Pricing")
    
    # New Columns During Data Cleaning
    Total_Revenue: float = Field(..., alias="Total Revenue")

    class Config:
        # Import Alias Name To Fast API And Streamlit 
        populate_by_name = True