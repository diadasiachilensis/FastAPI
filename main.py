# Importamos FastAPI para construir la API.
from fastapi import FastAPI

# Importamos los modelos definidos en models.py
from models import Customer, Transaction, Invoice, CustomerCreate

# Creamos una instancia de la aplicación FastAPI
app = FastAPI()

# Definimos la ruta raíz con un endpoint GET que devuelve un mensaje de bienvenida.
@app.get("/")
async def root():
    return {"message": "Hola, Mundo!"}

# Base de datos simulada como una lista en memoria para almacenar clientes.
db_customers: list[Customer] = []



# Endpoint para crear un nuevo cliente.
# - `@app.post("/customers")` indica que se accede mediante una solicitud POST a "/customers".
# - `response_model=Customer` define que la respuesta tendrá la estructura del modelo Customer.
@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate): 
    # Se valida y convierte la entrada (customer_data) en un objeto de tipo Customer.
    customer = Customer.model_validate(customer_data.model_dump())
    # Se asigna un ID al cliente (simulando una base de datos, usando el tamaño de la lista actual).
    customer.id = len(db_customers)

    # Se guarda el cliente en la lista simulada de clientes.
    db_customers.append(customer)

    # Se retorna el cliente creado.
    return customer

# Endpoint para obtener la lista de clientes.
@app.get("/customers", response_model=list[Customer])
async def list_customer():
    return db_customers  # Retorna la lista de clientes almacenados.

# Endpoint para crear una transacción.
# - `@app.post("/transactions")` indica que la ruta acepta solicitudes POST en "/transactions".
@app.post("/transactions")
async def create_transactions(transactions_data: Transaction):
    return transactions_data  # Retorna los datos de la transacción recibida.

# Endpoint para crear una factura.
# - `@app.post("/invoices")` indica que la ruta acepta solicitudes POST en "/invoices".
@app.post("/invoices")
async def create_invoices(invoice_data: Invoice):
    return invoice_data  # Retorna los datos de la factura recibida.
