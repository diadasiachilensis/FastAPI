# Importamos BaseModel de Pydantic para definir modelos de datos.
from pydantic import BaseModel

# Definimos una clase base para los clientes.
class CustomerBase(BaseModel):
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

# Definimos la estructura de una transacción.
class Transaction(BaseModel):
    id         : int  # Identificador único de la transacción.
    ammount    : int  # Monto de la transacción.
    description: str | None  # Descripción opcional.

# Definimos la estructura de una factura (Invoice).
class Invoice(BaseModel):
    id          : int  # Identificador único de la factura.
    customer    : Customer  # Cliente asociado a la factura.
    transactions: list[Transaction]  # Lista de transacciones en la factura.

    # Propiedad para calcular el monto total de la factura sumando los montos de todas las transacciones.
    @property
    def ammount_total(self):
        return sum(transaction.ammount for transaction in self.transactions)
