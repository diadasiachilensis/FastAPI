#esctrcutra de datos de la aplciacion 

from pydantic import BaseModel

class CustomerBase(BaseModel):
    name       : str
    description: str | None
    email      : str
    age        : int


class CustomerCreate(CustomerBase):
    #herencia
    pass

class Customer(CustomerBase):
    id         : int | None = None 



class Transaction(BaseModel):
    id         : int
    ammount    : int
    description: str | None

class Invoice(BaseModel):
    id          : int
    customer    : Customer
    transactions: list[Transaction]

    @property
    def ammount_total(self):
        return sum(transaction.ammount for transaction in self.transactions)