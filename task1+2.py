from models import *
from datetime import datetime


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Give me name and phone please."

    return wrapper


@input_error
def handle_hello():
    return "How can I help you?"


@input_error
def handle_add(command, address_book):
    _, name, phone, *birthday = command.split()
    birthday = birthday[0] if birthday else None
    address_book.add_record(name, phone, birthday)
    return "Contact added."


@input_error
def handle_change(command, address_book):
    _, name, phone = command.split()
    record = address_book.find(name)
    record.edit_phone(record.phones[0].value, phone)
    return "Contact changed."


@input_error
def handle_phone(command, address_book):
    _, name = command.split()
    record = address_book.find(name)
    return f"Phone number for {name}: {record.phones[0].value}"


@input_error
def handle_delete(command, address_book):
    _, name = command.split()
    address_book.delete(name)
    return f"Deleted {name}"


@input_error
def handle_all(address_book):
    result = "All records:\n"
    for name, record in address_book.data.items():
        birthday_info = f" ({record.birthday.value})" if record.birthday else ""
        result += f"{name}: {record.phones[0].value}{birthday_info}\n"
    return result


@input_error
def handle_add_birthday(command, address_book):
    _, name, birthday = command.split()
    address_book.find(name).add_birthday(birthday)
    return f"Birthday added for {name}."


@input_error
def handle_show_birthday(command, address_book):
    _, name = command.split()
    record = address_book.find(name)
    if record.birthday:
        return f"Birthday for {name}: {record.birthday.value}"
    else:
        return f"No birthday found for {name}."


def main():
    try:
        with open("contacts", "rb"):
            pass
        file_exists = True
    except FileNotFoundError:
        file_exists = False

    address_book = AddressBook()

    if file_exists:
        address_book.load_from_file("contacts")
        print("Data loaded from file.")
    else:
        print("No data found in file. Creating a new one.")

    while True:
        command = input("Enter a command: ").strip()
        if command in ["close", "exit"]:
            address_book.save_to_file("contacts")
            print("Good bye!")
            break
        elif command == "hello":
            print(handle_hello())
        elif command.startswith("change"):
            print(handle_change(command, address_book))
        elif command.startswith("phone"):
            print(handle_phone(command, address_book))
        elif command == "all":
            print(handle_all(address_book))
        elif command.startswith("delete"):
            print(handle_delete(command, address_book))
        elif command.startswith("add-birthday"):
            print(handle_add_birthday(command, address_book))
        elif command.startswith("show-birthday"):
            print(handle_show_birthday(command, address_book))
        elif command.startswith("add"):
            print(handle_add(command, address_book))
        elif command == "birthdays":
            handle_all_birthdays(address_book)
        else:
            print("Invalid command. Try again.")


if __name__ == "__main__":
    main()
