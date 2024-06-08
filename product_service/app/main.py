# from fastapi import FastAPI, Depends, HTTPException, status
# from contextlib import asynccontextmanager
# from app.db import create_db_and_tables



# # Async context manager for application lifespan events
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("Creating tables..")
#     create_db_and_tables()  # Create database tables
#     yield  # Application startup

# # Create FastAPI app with custom lifespan and metadata
# app = FastAPI(
#     lifespan=lifespan,
#     title="Product_service_API",
#     version="0.0.1",
#     servers=[
#         {
#             "url": "http://127.0.0.1:8007",
#             "description": "Development Server"
#         }
#     ]
# )


# # Root endpoint
# @app.get("/")
# def read_root():
#     return {"Welcome": "product_service"}


from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from typing import List, Optional
from sqlmodel import SQLModel, Field, create_engine, Session, select
from app.models import Product
from app.db import create_db_and_tables , engine
from app.schemas import ProductCreate, ProductResponse, ProductUpdate



# Async context manager for application lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()  # Create database tables
    yield  # Application startup

# Create FastAPI app with custom lifespan and metadata
app = FastAPI(
    lifespan=lifespan,
    title="Product_service_API",
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8007",
            "description": "Development Server"
        }
    ]
)

# Dependency to get DB session
def get_db():
    with Session(engine) as session:
        yield session



# CRUD operations
def create_product(db: Session, product: ProductCreate):
    db_product = Product.from_orm(product)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product_by_id(db: Session, product_id: int):
    return db.get(Product, product_id)

def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.get(Product, product_id)
    if db_product:
        for key, value in product.dict(exclude_unset=True).items():
            setattr(db_product, key, value)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    return None

def delete_product(db: Session, product_id: int):
    db_product = db.get(Product, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False

def get_all_products(db: Session, skip: int = 0, limit: int = 10):
    statement = select(Product).offset(skip).limit(limit)
    return db.exec(statement).all()

# Root endpoint
@app.get("/")
def read_root():
    return {"Welcome": "product_service"}

# Create a new product
@app.post("/products/", response_model=ProductResponse)
def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = create_product(db=db, product=product)
    return db_product

# Get a product by ID
@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product_by_ID(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product_by_id(db=db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Update a product by ID
@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product_endpoint(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = update_product(db=db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Delete a product by ID
@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    result = delete_product(db=db, product_id=product_id)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted successfully"}

# Get all products
@app.get("/products/", response_model=List[ProductResponse])
def get_all_products_endpoint(db: Session = Depends(get_db)):
    products = get_all_products(db=db)
    return products

