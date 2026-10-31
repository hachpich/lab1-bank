from dataclasses import dataclass, field

class BankException(Exception):
    pass

class InsufficientFundsError(BankException):
    pass

class ValidationError(BankException):
    pass

@dataclass
class Client:
    id: int
    full_name: str
    phone: str

@dataclass
class Account:
    id: int
    client_id: int
    balance: float = 0.0
    currency: str = "RUB"
    is_blocked: bool = False

@dataclass
class Transaction:
    id: int
    account_id: int
    amount: float
    tx_type: str

@dataclass
class Card:
    id: int
    account_id: int
    card_number: str

@dataclass
class Loan:
    id: int
    client_id: int
    amount: float

@dataclass
class Deposit:
    id: int
    client_id: int
    amount: float

@dataclass
class Branch:
    id: int
    address: str

@dataclass
class Employee:
    id: int
    full_name: str

@dataclass
class CurrencyRate:
    code: str
    rate: float

class Bank:
    def __init__(self):
        self.clients: list[Client] = []
        self.accounts: list[Account] = []
        self.transactions: list[Transaction] = []

    def add_client(self, client: Client) -> None:
        self.clients.append(client)

    def deposit(self, account_id: int, amount: float) -> None:
        if amount <= 0:
            raise ValidationError("Сумма пополнения должна быть больше нуля")

        acc = next((a for a in self.accounts if a.id == account_id), None)
        if not acc:
            raise BankException("Счет не найден")
        if acc.is_blocked:
            raise BankException("Счет заблокирован")

        acc.balance += amount
        self.transactions.append(Transaction(len(self.transactions)+1, account_id, amount, "deposit"))

    def withdraw(self, account_id: int, amount: float) -> None:
        if amount <= 0:
            raise ValidationError("Сумма снятия должна быть больше нуля")

        acc = next((a for a in self.accounts if a.id == account_id), None)
        if not acc:
            raise BankException("Счет не найден")
        if acc.balance < amount:
            raise InsufficientFundsError(f"Недостаточно средств. Баланс: {acc.balance}")

        acc.balance -= amount
        self.transactions.append(Transaction(len(self.transactions)+1, account_id, amount, "withdrawal"))