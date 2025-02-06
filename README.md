# Documentación de la API - FastAPI

## 📌 Índice

# Índice

1. [Explicación detallada del código en FastAPI](#explicación-detallada-del-código-en-fastapi)
2. [Validación de datos con Pydantic](#validación-de-datos-con-pydantic)
   - [📌 Importación de Pydantic](#📌-importación-de-pydantic)
   - [📌 Modelo CustomerBase](#📌-modelo-customerbase)
   - [📌 Integrar el modelo CustomerBase al endpoint](#📌-integrar-el-modelo-customerbase-al-endpoint)
3. [Modelado de Datos en APIs con FastAPI](#modelado-de-datos-en-apis-con-fastapi)
   - [📌 Script models.py](#📌-script-modelspy)
   - [📃 ¿Por qué usar models.py?](#📃-¿por-qué-usar-modelspy)
   - [📌 Importación de Pydantic](#📌-importación-de-pydantic-1)
   - [📌 Modelo de Datos](#📌-modelo-de-datos)
   - [📌 Creación de Modelos Diferenciados](#📌-creación-de-modelos-diferenciados)
4. [Creación de relaciones entre datos](#creación-de-relaciones-entre-datos)
   - [📌 ¿Cómo se usa models.py en main.py?](#📌-¿cómo-se-usa-modelspy-en-mainpy)
5. [Validación y gestión de Modelos](#validación-y-gestión-de-modelos)
   - [📌 Configurar los modelos para crear un nuevo cliente sin ID](#📌-configurar-los-modelos-para-crear-un-nuevo-cliente-sin-id)
   - [📌 Gestionar la validación y asignación de ID en el backend](#📌-gestionar-la-validación-y-asignación-de-id-en-el-backend)
6. [Listar base de datos en un JSON en un endpoint](#listar-base-de-datos-en-un-json-en-un-endpoint)
   - [📌 Crear un endpoint para obtener todos los clientes](#📌-crear-un-endpoint-para-obtener-todos-los-clientes)
   - [📌 Ejemplo de uso con curl para agregar clientes](#📌-ejemplo-de-uso-con-curl-para-agregar-clientes)
   - [📌 Ejemplo de uso con curl para listar clientes](#📌-ejemplo-de-uso-con-curl-para-listar-clientes)
   - [📌 Obtener un cliente específico por ID](#📌-obtener-un-cliente-específico-por-id)


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

### 📌 **Script models.py**
En **FastAPI**, el archivo models.py cumple una función clave: definir la estructura de los datos que manejará la API. Estos modelos actúan como **plantillas** que permiten validar y organizar la información enviada y recibida en las solicitudes HTTP.

#### **📃 ¿Por qué usar models.py?**
- 📂 **Organización del código**: Mantiene el código modular y fácil de mantener.
- ✅ **Validación automática**: Gracias a Pydantic, se asegura que los datos cumplan con los tipos esperados.
- 🔗 **Conexión con bases de datos**: En caso de usar SQLAlchemy, se pueden definir modelos que se convierten en tablas de la base de datos.
- 🔄 **Serialización y deserialización**: Convierte datos entre formatos JSON ↔ Python de manera automática.

---

### **📌 Importación de Pydantic**
FastAPI utiliza Pydantic para definir modelos de datos con validación automática. Se importa BaseModel desde pydantic:

`models.py`
```python
from pydantic import BaseModel
```

``BaseModel`` permite crear modelos con validación integrada.

### 📌 **Modelo de Datos**

Un modelo de datos define la estructura de los objetos que manejará la API. Ejemplo:

`models.py`
```python
class Customer(BaseModel):
    id: int
    name: str
    email: str
    age: int
```
- Cada atributo (id, name, email, age) tiene un tipo de dato obligatorio.
- Si se envían datos incorrectos (por ejemplo, age="veinte" en vez de un número), FastAPI generará un error automáticamente.

### 📌 **Creación de Modelos Diferenciados**

En algunos casos, es útil tener diferentes modelos para distintas operaciones. Por ejemplo:

`models.py`
```python
# No agrega nuevos atributos, solo reutiliza la estructura.
class CustomerCreate(CustomerBase):
    pass  # Se usa al crear un cliente

# `Customer` extiende `CustomerBase` e incluye un ID opcional.
class Customer(CustomerBase):
    id: int  # Se añade un ID solo cuando el cliente ya existe
```
**Diferencias entre modelos:**

1. ``CustomerBase``: Modelo base con los datos esenciales.
2. ``CustomerCreate``: Se usa al crear un cliente (sin id).
3. ``Customer``: Representa un cliente ya almacenado (incluye id).

Mejor explicado queda de la siguiente manera: 

`models.py`
```python
# Definimos una clase base para los clientes.
class CustomerBase(BaseModel): #heredar BaseModel para agregar campos que sean validos sin necesidad de hacer algun otro metodo para crear estas validaciones.
    name       : str  # Nombre del cliente.
    description: str | None  # Descripción opcional.
    email      : str  # Correo electrónico.
    age        : int  # Edad.

# `CustomerCreate` hereda de `CustomerBase`, por lo que tiene los mismos atributos.
class CustomerCreate(CustomerBase):
    pass  # No agrega nuevos atributos, solo reutiliza la estructura.

# `Customer` extiende `CustomerBase` e incluye un ID opcional.
class Customer(CustomerBase):
    id         : int | None = None  # ID opcional del cliente.
    id         : int | None = None  # ID opcional del cliente.
```

## **Creación de relaciones entre datos**

Cuando se manejan relaciones entre datos (ej. clientes y facturas):

`models.py`
```python
# Definimos la estructura de una transacción.
class Transaction(BaseModel):
    id         : int  # Identificador único de la transacción.
    ammount    : int  # Monto de la transacción.
    description: str | None  # Descripción opcional con |.

# Definimos la estructura de una factura (Invoice).
class Invoice(BaseModel):
    id          : int  # Identificador único de la factura.
    customer    : Customer  # Cliente asociado a la factura.
    transactions: list[Transaction]  # Lista de transacciones en la factura.

    # Propiedad para calcular el monto total de la factura sumando los montos de todas las transacciones.
    @property
    def ammount_total(self):
        return sum(transaction.ammount for transaction in self.transactions)
```

**Explicación**:

``Invoice`` tiene un campo ``customer``, que es un objeto ``Customer``.
``transactions`` es una lista de objetos ``Transaction``.
La propiedad ``total_amount`` **calcula automáticamente el total de las transaccione**s.

---

### 📌 ¿Cómo se usa models.py en main.py?

El archivo ``models.py`` no funciona solo. Se importa en ``main.py`` para definir los **endpoints** de la API:

``main.py``
```python

# Importamos FastAPI para construir la API.
from fastapi import FastAPI
# Importamos los modelos definidos en models.py
from models import Customer, CustomerCreate

# Creamos una instancia de la aplicación FastAPI
app = FastAPI()

# Base de datos simulada como una lista en memoria para almacenar clientes.
db_customers: list[Customer] = []  # Simulación de base de datos en memoria

# Endpoint para crear un nuevo cliente.
# - `@app.post("/customers")` indica que se accede mediante una solicitud POST a "/customers".
# - `response_model=Customer` define que la respuesta tendrá la estructura del modelo Customer.
@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: Customer):
    # Se valida y convierte la entrada (customer_data) en un objeto de tipo Customer.
    customer = Customer(**customer_data.dict(), id=len(db_customers))
    # Se guarda el cliente en la lista simulada de clientes.
    db_customers.append(customer)
    # Se retorna el cliente creado.
    return customer
```
**📌 ¿Qué pasa aquí?**

- Se recibe un objeto Customer, se convierte en Customer y se guarda en una lista.
- La API devuelve el cliente creado en formato JSON.

---

## **Validacion y gestion de Modelos**

### 📌 Configurar los modelos para crear un nuevo cliente sin ID

Para evitar enviar un ID manualmente, creamos ``CustomerCreate``, que hereda de ``Customer`` pero excluye el ID, dejándolo en blanco hasta que se complete la validación. Esto es útil porque:

- El ID se asigna automáticamente en la base de datos o mediante código en memoria.
- Evitamos exposición de datos sensibles innecesarios en las solicitudes.

`models.py`
```python
# Definimos una clase base para los clientes.
class CustomerBase(BaseModel): #heredar BaseModel para agregar campos que sean validos sin necesidad de hacer algun otro metodo para crear estas validaciones.
    name       : str  # Nombre del cliente.
    description: str | None  # Descripción opcional.
    email      : str  # Correo electrónico.
    age        : int  # Edad.

# `CustomerCreate` hereda de `CustomerBase`, por lo que tiene los mismos atributos.
class CustomerCreate(CustomerBase):
    pass  # No agrega nuevos atributos, solo reutiliza la estructura.

# `Customer` extiende `CustomerBase` e incluye un ID opcional.
class Customer(CustomerBase):
    id         : int | None = None  # ID opcional del cliente.
    id         : int | None = None  # ID opcional del cliente.
```

Ahora el endpoint de ``Customer`` tiene el id, se debe cambiar por el ``CustomerCreate`` 

``main.py``
```python
# Importamos los modelos definidos en models.py
from models import Customer, Transaction, Invoice, CustomerCreate

# Endpoint para crear un nuevo cliente.
@app.post("/customers", response_model=Customer) #responder con un modelo que tenga el id
async def create_customer(customer_data: CustomerCreate): 
    return customer_data
```
---

### 📌 Gestionar la validacion y asignacion de id en el backend

FastAPI permite validar datos mediante modelos y gestionar IDs sin base de datos:

1. Se usa una variable ``current_id`` inicializada en 0 que se incrementa por cada nuevo registro.

    ``main.py``
    ```python
    current_id: int = 0 
    ```
<br/>

2. Los datos recibidos son validados y convertidos a diccionario ``(model.dict())``, creando una entrada limpia y sin errores.

    - Devuelve un diccionario con todos los datos que esta ingresando el usuario. queda definida como ``customer`` si la validacion no es exitosa, FastAPI devuelve un error 

    ``main.py``
    ```python
    # Endpoint para crear un nuevo cliente.
    @app.post("/customers", response_model=Customer) #responder con un modelo que tenga el id
    async def create_customer(customer_data: CustomerCreate): 
    # Se valida y convierte la entrada (customer_data) en un objeto de tipo Customer.
    customer = Customer.model_validate(customer_data.model_dump())
    ``` 
    <br/>
3.  En un entorno asincrónico, no se recomienda incrementar ``current_id`` de forma manual, por lo que una lista simula la base de datos en memoria, donde el ID es el índice del elemento.

    ``main.py``
    ```python
    # Endpoint para crear un nuevo cliente.
    @app.post("/customers", response_model=Customer) #responder con un modelo que tenga el id
    async def create_customer(customer_data: CustomerCreate): 
    # Se valida y convierte la entrada (customer_data) en un objeto de tipo Customer.
    customer = Customer.model_validate(customer_data.model_dump())
    #Asumiendo que hace base de datos
    customer.id = current_id +1 
    ```
    <br/>

    ``customer.id = current_id +1`` esto no resulta en un entorno asincrónico.
    <br/>
    - Para obtener el id debemos saber cuantos elementos estan en la lista

        1. **Base de datos simulada**
            - Se crea una **lista en memoria** para almacenar clientes. En un sistema real, esto debería ser una base de datos.
            - Tenemos una lista que se asume que es nuestra base de datos ```db_customers```, pero queda en memoria, osea si se apaga el servidor se borran los datos. 

                ``main.py``
                ```python
                db_customers: list[Customer] = [] #tenemos una lista vacia 
                ``` 

        2. **Crear un Cliente (POST `/customers`)**
            - Se recibe un ``customer_data`` del ``CustomerCreate`` del que no tiene el id. 
                - **`customer_data: CustomerCreate`** → Recibe datos con el modelo `CustomerCreate`:
                - FastAPI usa **tipado fuerte** para validar automáticamente los datos.
                - **`customer_data`** debe tener la estructura del modelo `CustomerCreate`. Si falta algún dato obligatorio, **FastAPI devolverá un error automático**.

                    ``main.py``
        
                    ```python
                    @app.post("/customers", response_model=Customer)
                    async def create_customer(customer_data: CustomerCreate): 
                    ```
      

        3. Se valida con la clase `Customer` 
            - Convierte los datos en una instancia válida de `Customer`

                ``main.py``
            
                ```python
                customer = Customer.model_validate(customer_data.model_dump())
                ```

        4. Asigna un ID único
            - Luego, se cuentan cuantos elementos hay en la lista `db_customers` y se asgina como el id del customer
            
                ``main.py``

                ```python            
                customer.id = len(db_customers)
                ```
        
        5. Guarda el cliente en la lista
            - Al final, se agrega el customer a la lista y retorna el customer para que el usuario lo pueda ver

                ``main.py``

                ```python
                db_customers.append(customer)
                return customer
                ```

    🔹**Devuelve el cliente creado**🔹

### 📌 Listar base de datos en un JSON en un endpoint

Un **endpoint** es una URL específica dentro de una API que permite a los clientes (usuarios o aplicaciones) **enviar y recibir datos** mediante **solicitudes HTTP**. 
En **FastAPI**, los endpoints están definidos por funciones que manejan solicitudes **GET, POST, PUT, DELETE**, entre otras.

Se crea un nuevo endpoint que va a ser del tipo `get`.

- Un usuario o una aplicación puede hacer una **solicitud GET** a **`/customers`**.
- La API responderá con una lista de clientes en formato **JSON**.

1. Una funcion que retorna la basee de datos la cual es una lista

    ```python
    @app.get("/customers")
    async def list_customer():
        return db_customers
    ```
2. En un listado se debe definir el `response_model=list[Customer]` para mostrar el JSON con los clientes. 

    ```python
    @app.get("/customers",response_model=list[Customer])
    async def list_customer():
        return db_customers
    ```
    🔹 **Explicación:**
    1.  `@app.get("/customers")` → Define un endpoint que responde a solicitudes **GET** en la ruta **`/customers`**.
    2. `response_model=list[Customer]` → Indica que la respuesta será una **lista de objetos `Customer`**.
    3. `async def list_customer():` → Es una función asíncrona que maneja la solicitud.
    4. `return db_customers` → Devuelve la lista de clientes almacenados.

    🔹 **¿Cómo funciona este endpoint?**
    1. Se accede con **POST** en **`/customers`**.
    2. Recibe datos en formato **JSON** con la estructura de `CustomerCreate`.
    3. Se valida y almacena el cliente en la base de datos en memoria.
    4. Devuelve el cliente creado.

**FastAPI convierte automáticamente la lista de Customer a un JSON, haciéndola accesible desde la documentación.**

**Ejemplo de Uso con curl**
    Para **crear un nuevo cliente**, usa:

```bash
    curl -X 'POST' 'http://127.0.0.1:8000/customers' \
        -H 'Content-Type: application/json' \
        -d '{
            "name": "Carlos Gómez",
            "description": "Nuevo cliente",
            "email": "carlos@example.com",
            "age": 40
            }'
```

🔹**Salida esperada:**

```javascript
    {
        "id": 2,
        "name": "Carlos Gómez",
        "description": "Nuevo cliente",
        "email": "carlos@example.com",
        "age": 40
    }
```

**Ejemplo de Uso en `curl`**
    Si quieres obtener la lista de clientes desde la terminal, puedes usar:

```bash
    curl -X 'GET' 'http://127.0.0.1:8000/customers' -H 'accept: application/json'
```

🔹 **Salida esperada (si hay clientes en la base de datos simulada)**:

```javascript
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


- **¿Qué ocurre al crear un nuevo cliente en memoria?**
    Dado que estamos trabajando en memoria:

    - Los datos se borran al reiniciar el servidor.
        Para cada cliente creado, asignamos un ID basado en el índice de la lista, simulando el autoincremento de una base de datos real.

- **¿Cómo crear un endpoint para obtener un cliente específico por ID?**
    Finalmente, para acceder a un cliente específico, añadimos un nuevo endpoint que recibe el ID en la URL:

    - Este endpoint busca en la lista por ID y devuelve el cliente en formato JSON.
    - Si el cliente no existe, FastAPI devuelve un error, protegiendo la integridad de los datos.

--- 

















-------------
-------------
-------------

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

