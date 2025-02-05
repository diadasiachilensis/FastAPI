from fastapi import FastAPI
from models import Customer, Transaction, Invoice, CustomerCreate

app=FastAPI()

@app.get("/")
async def root():
    return {"message": "Hola, Mundo!"}

db_customers: list[Customer] = []

@app.post("/customers", response_model=Customer) #response_model, esta respodiendo 
async def create_customer(customer_data : CustomerCreate): #recibiendo datos 
    customer = Customer.model_validate(customer_data.model_dump())
    # Ausmiendo que hace base de datos
    customer.id = len(db_customers)
    db_customers.append(customer)
    return customer

@app.get("/customers", response_model=list[Customer])
async def list_customer():
    return db_customers


@app.post("/transactions")
async def create_transactions(transactions_data : Transaction):
    return transactions_data

@app.post("/inovices")
async def create_inovices(invoice_data : Invoice):
    return invoice_data
