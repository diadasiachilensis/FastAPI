# fastAPI

# Documentación de la API - FastAPI

## 📌 Índice
1. [Introducción](#introducción)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Instalación y Configuración](#instalación-y-configuración)
4. [Explicación de los Modelos de Datos (`models.py`)](#explicación-de-los-modelos-de-datos-modelspy)
   - [Importación de Pydantic](#importación-de-pydantic)
   - [Modelo `CustomerBase`](#modelo-customerbase)
   - [Modelo `CustomerCreate`](#modelo-customercreate)
   - [Modelo `Customer`](#modelo-customer)
   - [Modelo `Transaction`](#modelo-transaction)
   - [Modelo `Invoice`](#modelo-invoice)
5. [Explicación de las Rutas de la API (`main.py`)](#explicación-de-las-rutas-de-la-api-mainpy)
   - [Instancia de FastAPI](#instancia-de-fastapi)
   - [Ruta raíz (`GET /`)](#ruta-raíz-get-)
   - [Base de Datos Simulada](#base-de-datos-simulada)
   - [Crear un Cliente (`POST /customers`)](#crear-un-cliente-post-customers)
   - [Listar Clientes (`GET /customers`)](#listar-clientes-get-customers)
   - [Crear una Transacción (`POST /transactions`)](#crear-una-transacción-post-transactions)
   - [Crear una Factura (`POST /invoices`)](#crear-una-factura-post-invoices)
6. [Conceptos Clave de FastAPI](#conceptos-clave-de-fastapi)
   - [Endpoints y Métodos HTTP](#endpoints-y-métodos-http)
   - [Tipado Estricto y Validación con Pydantic](#tipado-estricto-y-validación-con-pydantic)
   - [Asincronía (`async/await`)](#asincronía-asyncawait)
7. [Ejemplo de Uso con `curl`](#ejemplo-de-uso-con-curl)
8. [Ejecución del Servidor](#ejecución-del-servidor)
9. [Mejoras y Próximos Pasos](#mejoras-y-próximos-pasos)

## **Explicación detallada del código en FastAPI**
El código define una API con **FastAPI**, que permite manejar clientes, transacciones e invoices (facturas). Vamos a analizarlo en detalle dividiendo la explicación en **estructura del código**, **funcionalidad de cada parte**, y **conceptos clave de FastAPI**.

---

## **1. Estructura del Código**
El código está organizado en dos archivos principales:

1. **`main.py`** → Define la API, sus rutas y la lógica de procesamiento de datos.
2. **`models.py`** → Define los modelos de datos utilizando **Pydantic**, que nos ayuda a validar la estructura de los datos recibidos y enviados.

---

## **2. Explicación de `models.py` (Modelos de datos)**
Este archivo define la estructura de los datos que maneja la API. Utiliza **Pydantic**, una librería de validación de datos en Python, para garantizar que los datos sean correctos antes de ser procesados.

### 📌 **Importación de Pydantic**
```python
from pydantic import BaseModel
```
- **`BaseModel`**: Clase base de Pydantic que permite definir modelos de datos con validación automática.

---

### 📌 **Modelo `CustomerBase`**
```python
class CustomerBase(BaseModel):
    name       : str  # Nombre del cliente (obligatorio).
    description: str | None  # Descripción opcional del cliente.
    email      : str  # Correo electrónico (obligatorio).
    age        : int  # Edad del cliente (obligatorio).
```
Este modelo define las propiedades básicas de un **Cliente**:
- **`name`**, **`email`** y **`age`** son obligatorios.
- **`description`** es opcional (`None` significa que puede faltar).

---

### 📌 **Modelo `CustomerCreate`**
```python
class CustomerCreate(CustomerBase):
    pass
```
- Hereda de `CustomerBase`, lo que significa que tiene los mismos atributos.
- No agrega nuevos atributos, se usa para diferenciar la creación de clientes en la API.

---

### 📌 **Modelo `Customer`**
```python
class Customer(CustomerBase):
    id: int | None = None  # ID opcional, se asignará al crearlo.
```
- Extiende `CustomerBase` añadiendo un atributo `id`, que se asignará automáticamente cuando se registre un cliente.

---

### 📌 **Modelo `Transaction`**
```python
class Transaction(BaseModel):
    id         : int  # Identificador único de la transacción.
    ammount    : int  # Monto de la transacción.
    description: str | None  # Descripción opcional de la transacción.
```
- Representa una **transacción** con tres atributos: `id`, `ammount` y `description`.
- El `id` es único para cada transacción.
- `description` es opcional.

---

### 📌 **Modelo `Invoice` (Factura)**
```python
class Invoice(BaseModel):
    id          : int  # Identificador único de la factura.
    customer    : Customer  # Cliente asociado a la factura.
    transactions: list[Transaction]  # Lista de transacciones asociadas.

    @property
    def ammount_total(self):
        return sum(transaction.ammount for transaction in self.transactions)
```
- **`id`**: Identificador de la factura.
- **`customer`**: Cliente que generó la factura.
- **`transactions`**: Lista de transacciones asociadas.
- **`ammount_total`**: Propiedad que calcula el monto total sumando todas las transacciones.

---

## **3. Explicación de `main.py` (Rutas de la API)**
Este archivo define las **rutas** y la lógica para procesar solicitudes HTTP.

### 📌 **Importaciones**
```python
from fastapi import FastAPI
from models import Customer, Transaction, Invoice, CustomerCreate
```
- Se importa `FastAPI` para definir la API.
- Se importan los modelos desde `models.py`.

---

### 📌 **Instancia de FastAPI**
```python
app = FastAPI()
```
- `FastAPI()` crea una instancia de la aplicación, necesaria para definir rutas y manejar solicitudes.

---

### 📌 **Ruta raíz (GET)**
```python
@app.get("/")
async def root():
    return {"message": "Hola, Mundo!"}
```
- Define un endpoint en `/` que responde con `{"message": "Hola, Mundo!"}` cuando se accede con un **GET**.
- `async def` indica que la función es asíncrona, lo que permite manejar solicitudes de forma eficiente.

---

### 📌 **Base de datos simulada**
```python
db_customers: list[Customer] = []
```
- Se crea una **lista en memoria** para almacenar clientes. En un sistema real, esto debería ser una base de datos.

---

### 📌 **Crear un Cliente (POST `/customers`)**
```python
@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate):
    customer = Customer.model_validate(customer_data.model_dump())
    customer.id = len(db_customers)  # Se asigna un ID basado en la cantidad de clientes.
    db_customers.append(customer)  # Se agrega el cliente a la lista.
    return customer  # Se devuelve el cliente creado.
```
1. **`customer_data: CustomerCreate`** → Recibe datos con el modelo `CustomerCreate`.
2. **`model_validate(customer_data.model_dump())`** → Convierte los datos en una instancia válida de `Customer`.
3. **`customer.id = len(db_customers)`** → Asigna un ID único.
4. **`db_customers.append(customer)`** → Guarda el cliente en la lista.
5. **Devuelve el cliente creado**.

---

### 📌 **Listar Clientes (GET `/customers`)**
```python
@app.get("/customers", response_model=list[Customer])
async def list_customer():
    return db_customers
```
- Devuelve la lista de clientes registrados.

---

### 📌 **Crear una Transacción (POST `/transactions`)**
```python
@app.post("/transactions")
async def create_transactions(transactions_data: Transaction):
    return transactions_data
```
- Recibe datos de una **transacción** en formato `Transaction` y los devuelve.
- No almacena los datos (se necesita una base de datos real para eso).

---

### 📌 **Crear una Factura (POST `/invoices`)**
```python
@app.post("/invoices")
async def create_invoices(invoice_data: Invoice):
    return invoice_data
```
- Recibe datos de una **factura** en formato `Invoice` y los devuelve.
- No almacena los datos (se necesita una base de datos real).

---

## **4. Conceptos Clave de FastAPI**
### ✅ **1. Endpoints y Métodos HTTP**
FastAPI usa **decoradores** para definir endpoints:
- `@app.get("/ruta")` → Maneja solicitudes **GET**.
- `@app.post("/ruta")` → Maneja solicitudes **POST**.
- `@app.put("/ruta")` → Maneja solicitudes **PUT** (actualizar datos).
- `@app.delete("/ruta")` → Maneja solicitudes **DELETE** (eliminar datos).

---

### ✅ **2. Tipado Estricto y Validación con Pydantic**
FastAPI usa **tipado fuerte** para validar automáticamente los datos.
Ejemplo:
```python
async def create_customer(customer_data: CustomerCreate):
``` 
- **`customer_data`** debe tener la estructura del modelo `CustomerCreate`. Si falta algún dato obligatorio, **FastAPI devolverá un error automático**.

---

### ✅ **3. Asincronía (async/await)**
- **FastAPI soporta asincronía con `async def`**, lo que permite manejar muchas solicitudes sin bloquear la aplicación.
- Es útil en aplicaciones con muchas conexiones simultáneas (como APIs web de alto tráfico).

---

## **Conclusión**
- 🚀 **FastAPI** es rápido y potente, con validación automática y compatibilidad con asincronía.
- ✅ **`models.py`** define estructuras de datos con **Pydantic**.
- ✅ **`main.py`** define rutas que permiten **crear y listar clientes, transacciones y facturas**.
- 📌 **La API necesita una base de datos real** para almacenar datos de forma permanente.