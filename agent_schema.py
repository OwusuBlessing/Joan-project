from langchain.pydantic_v1 import BaseModel, Field
class Product_details(BaseModel):
    product:str = Field(..., description="The car product name")
    