from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product

from database import session, engine
import database_model
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"]
    
)


database_model.Base.metadata.create_all(bind=engine)

Products = [Product(id=1, name="Laptop", price=999.99, description="High-performance laptop", quantity=10),
            Product(id=2, name="Smartphone", price=499.99, description="Latest model smartphone", quantity=20),
            Product(id=3, name="Headphones", price=199.99, description="Noise-cancelling headphones", quantity=15),
            Product(id=4, name="Smartwatch", price=299.99, description="Stylish smartwatch", quantity=25),
            ]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = session()

    count = db.query(database_model.Product).count()

    if count == 0:
        for product in Products:
            db.add(database_model.Product(**product.model_dump()))
    
        db.commit()
init_db()

@app.get('/')
def greet():
    return "WELCOMME"

@app.get('/products')
def get_products(db : Session = Depends(get_db)):
    db_products = db.query(database_model.Product).all()
    return db_products

@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == product_id).first()
    if db_product:
        return db_product
    return {"message": "Product not found"}

@app.post('/products')
def add_product(product: Product , db: Session = Depends(get_db)):
    db.add(database_model.Product(**product.model_dump()))
    db.commit()
    return product

@app.put('/products/{product_id}')
def update_product(product_id : int , product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == product_id).first()
    if db_product:
        db_product.name = product.name
        db_product.price = product.price
        db_product.description = product.description
        db_product.quantity = product.quantity
        db.commit()
        return db_product

    else:
       return {"message": "Product not found"}

@app.delete('/products/{product_id}')
def delete_product(product_id : int, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted successfully"
    return {"message": "Product not found"}