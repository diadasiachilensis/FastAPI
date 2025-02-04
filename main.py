from fastapi import FastAPI
from models import Customer, Transaction, Invoice

app=FastAPI()

@app.post("/customers")
async def create_customer(customer_data : Customer):
    return customer_data

@app.post("/transactions")
async def create_transactions(transactions_data : Transaction):
    return transactions_data

@app.post("/inovices")
async def create_inovices(invoice_data : Invoice):
    return invoice_data
