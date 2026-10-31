import json
import xml.etree.ElementTree as ET
from dataclasses import asdict
from src.models import Bank, Client, Account, BankException

class FileFormatError(BankException):
    pass

def save_to_json(bank: Bank, filename: str) -> None:
    data = {
        "clients": [asdict(c) for c in bank.clients],
        "accounts": [asdict(a) for a in bank.accounts],
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_from_json(bank: Bank, filename: str) -> None:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        bank.clients = [Client(**c) for c in data.get("clients", [])]
        bank.accounts = [Account(**a) for a in data.get("accounts", [])]
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")
    except json.JSONDecodeError:
        raise FileFormatError("Некорректный JSON")

def save_to_xml(bank: Bank, filename: str) -> None:
    root = ET.Element("bank")

    for c in bank.clients:
        c_el = ET.SubElement(root, "client", id=str(c.id))
        ET.SubElement(c_el, "name").text = c.full_name
        ET.SubElement(c_el, "phone").text = c.phone

    for a in bank.accounts:
        a_el = ET.SubElement(root, "account", id=str(a.id), client_id=str(a.client_id))
        ET.SubElement(a_el, "balance").text = str(a.balance)
        ET.SubElement(a_el, "currency").text = a.currency

    ET.ElementTree(root).write(filename, encoding="utf-8", xml_declaration=True)

def load_from_xml(bank: Bank, filename: str) -> None:
    try:
        root = ET.parse(filename).getroot()

        bank.clients = [
            Client(id=int(el.get("id")), full_name=el.find("name").text, phone=el.find("phone").text)
            for el in root.findall("client")
        ]
        bank.accounts = [
            Account(id=int(el.get("id")), client_id=int(el.get("client_id")),
                    balance=float(el.find("balance").text), currency=el.find("currency").text)
            for el in root.findall("account")
        ]
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")
    except ET.ParseError:
        raise FileFormatError("Некорректный XML")