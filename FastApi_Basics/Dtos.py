from pydantic import BaseModel

class ProductDTO(BaseModel):
    id:int
    productname:str
    price:int=0
    Quantity:int=0