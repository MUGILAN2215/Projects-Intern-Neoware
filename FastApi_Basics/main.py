from fastapi import FastAPI
from mockdata import products
from Dtos import ProductDTO

app=FastAPI()

@app.get("/")
def home():
    return "FastApi HomePage"

@app.get("/products")
def get_products():
    return products
#pathvariable
@app.get("/product/{id}")
def get_products_ByID(id:int):
    for product in products:
        if product["id"]==id:
            return product
        else:
            return "The Project is Not Found"
#RequestParam or QueryParameter
@app.get("/productUsage")
def product_usage(name:str,count:int):
    return f"The Product name is {name} and Product count is {count}"

@app.post("/product")
def create_product(product:ProductDTO):
    products.append(product.model_dump())
    return product

