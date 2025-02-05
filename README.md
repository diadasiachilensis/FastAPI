# Documentación de la API - FastAPI

## 📌 Índice
1. [Explicación detallada del código en FastAPI](#explicación-detallada-del-código-en-fastapi)
2. [Validación de datos con Pydantic](#Validación-de-datos-con-Pydantic)
   - [📌 Importación de Pydantic](#📌-importación-de-pydantic)
   - [📌 Modelo `CustomerBase`](#📌-Modelo-CustomerBase)
   - [📌 Modelo `CustomerCreate`](#📌-modelo-customercreate)
   - [📌 Modelo `Customer`](#📌-modelo-customer)
   - [📌 Modelo `Transaction`](#📌-modelo-transaction)
   - [📌 Modelo `Invoice` (Factura)](#📌-modelo-invoice-factura)
4. [3. Explicación de `main.py` (Rutas de la API)](#3-explicación-de-mainpy-rutas-de-la-api)
   - [📌 Importaciones](#📌-importaciones)
   - [📌 Instancia de FastAPI](#📌-instancia-de-fastapi)
   - [📌 Ruta raíz (`GET /`)](#📌-ruta-raíz-get-)
   - [📌 Base de datos simulada](#📌-base-de-datos-simulada)
   - [📌 Crear un Cliente (`POST /customers`)](#📌-crear-un-cliente-post-customers)
   - [📌 Listar Clientes (`GET /customers`)](#📌-listar-clientes-get-customers)
   - [📌 Crear una Transacción (`POST /transactions`)](#📌-crear-una-transacción-post-transactions)
   - [📌 Crear una Factura (`POST /invoices`)](#📌-crear-una-factura-post-invoices)
5. [4. Conceptos Clave de FastAPI](#4-conceptos-clave-de-fastapi)
   - [✅ 1. Endpoints y Métodos HTTP](#✅-1-endpoints-y-métodos-http)
   - [✅ 2. Tipado Estricto y Validación con Pydantic](#✅-2-tipado-estricto-y-validación-con-pydantic)
   - [✅ 3. Asincronía (`async/await`)](#✅-3-asincronía-asyncawait)
6. [5. ¿Qué son los Endpoints?](#¿Qué-son-los-Endpoints?)
   - [📌 Ejemplo de un Endpoint en FastAPI](#📌-Ejemplo-de-un-Endpoint-en-Fastapi) 
   - [📌 Ejemplo de Uso en `curl`](#📌-ejemplo-de-uso-en-curl)
   - [📌 Ejemplo de Endpoint con Método POST](#📌-ejemplo-de-endpoint-con-método-post)
7. [6. Ejemplo de Uso con `curl`](#6-ejemplo-de-uso-con-curl)

## **Explicación detallada del código en FastAPI**
El código define una API con **FastAPI**, que permite manejar clientes, transacciones e invoices (facturas). Vamos a analizarlo en detalle dividiendo la explicación en **estructura del código**, **funcionalidad de cada parte**, y **conceptos clave de FastAPI**.

---
## Validación de datos con Pydantic
Para crear un endpoint dinámico y seguro en FastAPI, es fundamental validar la información recibida, especialmente si el contenido se envía en el cuerpo de la solicitud. Los usuarios pueden ingresar datos incorrectos o no válidos, como un correo electrónico mal formateado, por lo que validar estos datos es crucial para el correcto funcionamiento de la API. 

FastAPI facilita esta validación a través de **Pydantic**, una biblioteca de Python que permite construir modelos de datos robustos. A continuación, exploraremos cómo crear un modelo básico de cliente para validar datos en un endpoint.

### 📌 **Importación de Pydantic**
```python
from pydantic import BaseModel
```
- **`BaseModel`**: Clase base de Pydantic que permite definir modelos de datos con validación automática.

---
### 📌 **Modelo CustomerBase**
```python
class CustomerBase(BaseModel):
    name       : str         # Nombre del cliente (obligatorio).
    description: str | None  # Descripción opcional del cliente por el operador logico |.
    email      : str         # Correo electrónico (obligatorio).
    age        : int         # Edad del cliente (obligatorio).
```
Este modelo define las propiedades básicas de un **Cliente** para que sean validos para el endpoint que los datos que esta ingresando el usuario sean los validos:
- **`name`**, **`email`** y **`age`** son obligatorios.
- **`description`** es opcional (`None` significa que puede faltar).
---
### 📌 Integrar el modelo CustomerBase al endpoint

Una vez definido el modelo, el siguiente paso es integrarlo en un endpoint. Esto se realiza mediante una función asincrónica, por ejemplo, ``async def create_customer``, que acepta datos de tipo ``Customer`` en el cuerpo de la solicitud.

```python
@app.post("/customers")
async def create_customer(customer_data: Customer):
    return customer_data
```

1. Se define el endpoint con el método `post`, para la creacion las APIRest necesitan el metodo ``post``.
2. Se registran los datos del cliente con el decorador ``@app.post("/customers")``.
3. En el cuerpo de la solicitud, los datos enviados serán automáticamente validados según el esquema de `Customer`.
4. Finalmente, la función puede retornar los mismos datos recibidos para verificar su recepción o realizar acciones adicionales como guardar en una base de datos o enviar una notificación.
---

## Modelado de Datos en APIs con FastAPI

Para diseñar una API robusta y eficiente, es fundamental modelar correctamente los datos. Un buen diseño de modelos no solo permite organizar y estructurar la información de manera eficiente, sino que también facilita la conexión entre distintos modelos y optimiza la funcionalidad de la API. En esta guía, exploraremos cómo crear modelos en **FastAPI** para estructurar datos, conectar modelos y mejorar la base de datos.

Cuando se desarrolla una API, es recomendable mantener los modelos en un archivo separado, como **`models.py`**, en lugar de definirlos dentro del archivo principal (`main.py`). Esta práctica ayuda a evitar el **"código espagueti"**, manteniendo el código modular, limpio y fácil de mantener. Aunque **FastAPI** no impone esta estructura, es una convención ampliamente utilizada en el desarrollo de aplicaciones en **Python**.

Para implementar esta organización, se deben copiar los modelos de datos y la clase **`BaseModel`** de **Pydantic** desde `main.py` y moverlos a `models.py`. Esto permite centralizar la definición de los modelos, facilitando su reutilización y modificación sin afectar directamente la lógica de la API.

El éxito de una API depende en gran medida de cómo se modelan los datos. Definir correctamente los modelos mejora la eficiencia de la base de datos y permite conectar adecuadamente la información dentro de la API. Utilizar un archivo **`models.py`** no solo es una práctica recomendada en **FastAPI**, sino que también es una buena práctica **"pythónica"**, alineada con los principios de modularidad y organización en el desarrollo de software.

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
## **¿Qué son los Endpoints?**
Un **endpoint** es una URL específica dentro de una API que permite a los clientes (usuarios o aplicaciones) **enviar y recibir datos** mediante **solicitudes HTTP**. 

En **FastAPI**, los endpoints están definidos por funciones que manejan solicitudes **GET, POST, PUT, DELETE**, entre otras.

### 📌 **Ejemplo de un Endpoint en FastAPI**
En tu script `main.py`, tienes el siguiente endpoint:

```python
@app.get("/customers", response_model=list[Customer])
async def list_customer():
    return db_customers
```

🔹 **Explicación:**
1. `@app.get("/customers")` → Define un endpoint que responde a solicitudes **GET** en la ruta **`/customers`**.
2. `response_model=list[Customer]` → Indica que la respuesta será una **lista de objetos `Customer`**.
3. `async def list_customer():` → Es una función asíncrona que maneja la solicitud.
4. `return db_customers` → Devuelve la lista de clientes almacenados.

### 📌 **¿Cómo funciona este endpoint en la práctica?**
- Un usuario o una aplicación puede hacer una **solicitud GET** a **`/customers`**.
- La API responderá con una lista de clientes en formato **JSON**.

---

## **Ejemplo de Uso en `curl`**
Si quieres obtener la lista de clientes desde la terminal, puedes usar:

```sh
curl -X 'GET' 'http://127.0.0.1:8000/customers' -H 'accept: application/json'
```

🔹 **Salida esperada (si hay clientes en la base de datos simulada)**:
```json
[
    {
        "id": 0,
        "name": "Juan Pérez",
        "description": "Cliente VIP",
        "email": "juan@example.com",
        "age": 35
    },
    {
        "id": 1,
        "name": "María López",
        "description": "Cliente regular",
        "email": "maria@example.com",
        "age": 29
    }
]
```

Si no hay clientes, el resultado será un **JSON vacío**: `[]`.

---

## **Ejemplo de Endpoint con Método POST**
Otro ejemplo en `main.py` es el endpoint para **crear clientes**:

```python
@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate):
    customer = Customer.model_validate(customer_data.model_dump())  # Convierte los datos a un objeto Customer
    customer.id = len(db_customers)  # Asigna un ID único
    db_customers.append(customer)  # Guarda el cliente en la lista simulada
    return customer  # Devuelve el cliente creado
```

🔹 **¿Cómo funciona este endpoint?**
1. Se accede con **POST** en **`/customers`**.
2. Recibe datos en formato **JSON** con la estructura de `CustomerCreate`.
3. Se valida y almacena el cliente en la base de datos en memoria.
4. Devuelve el cliente creado.

---

## **Ejemplo de Uso con curl**
Para **crear un nuevo cliente**, usa:

```sh
curl -X 'POST' 'http://127.0.0.1:8000/customers' \
     -H 'Content-Type: application/json' \
     -d '{
           "name": "Carlos Gómez",
           "description": "Nuevo cliente",
           "email": "carlos@example.com",
           "age": 40
         }'
```

🔹 **Salida esperada:**
```json
{
    "id": 2,
    "name": "Carlos Gómez",
    "description": "Nuevo cliente",
    "email": "carlos@example.com",
    "age": 40
}
```
---

## **Sintesis**
- Un **endpoint** es una dirección en la API que maneja solicitudes HTTP específicas.
- FastAPI usa **decoradores** (`@app.get()`, `@app.post()`, etc.) para definir endpoints.
- Puedes probarlos con herramientas como `curl` o Postman.
- `GET` sirve para **obtener** datos, `POST` para **enviar** datos, entre otros.
