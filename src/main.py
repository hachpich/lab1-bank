from src.models import Bank, Client, Account, InsufficientFundsError
from src.storage import save_to_json, load_from_json, save_to_xml, load_from_xml

def main() -> None:
    bank = Bank()

    try:
        print("1. Создание клиента и счета")
        bank.add_client(Client(1, "Иван Иванов", "+79991234567"))
        bank.accounts.append(Account(1, client_id=1, balance=1000.0))
        print("Клиент и счет созданы. Баланс: 1000.0")

        print("\n2. Банковские операции")
        bank.deposit(1, 500.0)
        print(f"После пополнения: {bank.accounts[0].balance} руб.")

        bank.withdraw(1, 200.0)
        print(f"После снятия: {bank.accounts[0].balance} руб.")

        print("\n3. Сохранение данных")
        save_to_json(bank, "bank.json")
        save_to_xml(bank, "bank.xml")
        print("JSON и XML успешно сохранены.")

        print("\n4. Загрузка из XML")
        bank2 = Bank()
        load_from_xml(bank2, "bank.xml")
        print(f"Загружен клиент: {bank2.clients[0].full_name}")
        print(f"Баланс из XML: {bank2.accounts[0].balance}")

        print("\n5. Проверка обработки ошибок")
        try:
            bank.withdraw(1, 5000.0)
        except InsufficientFundsError as e:
            print(f"Поймано исключение: {e}")

        try:
            load_from_json(bank, "missing.json")
        except FileNotFoundError as e:
            print(f"Поймано исключение: {e}")

    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main()