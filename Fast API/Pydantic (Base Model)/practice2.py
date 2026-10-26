from typing import Annotated, Optional

from pydantic import (
    BaseModel,
    EmailStr,
    AnyUrl,
    Field,
    field_validator,
    model_validator,
    computed_field,
)


class Extra_info(BaseModel):
    calories: Annotated[float, Field(description="This Show How Calaries In Your Meal", examples=["High","Low"])]
    veg: Annotated[str, Field(title="Food Type", examples=["Veg","Non Veg"], description="Select Your Food Type")]
    spicy: Annotated[str, Field(title="Food Tecture", examples=["Spicy","Less Spicy"])]
    

class Cafe_item(BaseModel):
    
    id: Annotated[int, Field(strict=True, description="Food Id",examples=[801,802])]
    name: Annotated[str, Field(max_length=50, strict=True)]
    category: Annotated[str, Field(default="Cold Coffee", strict=True)]
    price: Annotated[float, Field(gt=0, strict=True)]
    available: bool
    quantity: float
    Nutrition: Extra_info


class Customer(BaseModel):
    customer_id: Annotated[int, Field(description="Enter Customer ID", strict=True, examples=[101])]
    name: Annotated[str, Field(description="Enter Customer Name",strict=True,examples=["Om"], max_length=50)]
    email: Annotated[EmailStr, Field(description="Enter Customer Email ID",strict=True,examples=["Om@gmail.com"])]
    phone: Annotated[int, Field(description="Enter Customer Phone Number", strict=True, examples=[98776637])]
    address: Annotated[str, Field(description="Enter Your Address")]= None



class order(BaseModel):
    order_id: Annotated[int, Field(description="Enter Order ID", strict=True, examples=[201])]
    customer: Customer
    items: Cafe_item
    total_amount: Annotated[float, Field(description="Enter The Total Amount", strict=True, gt=10)]
    order_status: Annotated[bool, Field(description="Whats A Order Status", strict=True)]
    payment_status: bool
    
    
    @model_validator(mode="before")
    def item_cheake(self):
        if Cafe_item not in order:
            raise "Item Not In Menu"
        return order
    
    


class CafeItem_Maneger:
    
    @staticmethod
    def show_items(cafe):
        pass