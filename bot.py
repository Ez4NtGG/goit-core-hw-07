from datetime import datetime

# Decorator to handle input errors
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            return str(ve)
        except IndexError:
            return "Please provide all necessary arguments."
        except KeyError:
            return "Contact not found."
        except Exception as e:
            return f"An unexpected error occurred: {e}"
    return wrapper

# Base field class
class Field:
    pass

# Birthday class inheriting from Field
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

# Class to represent a contact record
class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

# AddressBook class to manage records
class AddressBook:
    def __init__(self):
        self.contacts = {}

    def add_record(self, record):
        self.contacts[record.name] = record

    def find(self, name):
        return self.contacts.get(name)

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.today()

        for record in self.contacts.values():
            if record.birthday:
                days_until_birthday = (record.birthday.value - today).days
                if 0 <= days_until_birthday <= 7:  # Including today
                    upcoming_birthdays.append({
                        "name": record.name,
                        "birthday": record.birthday.value.strftime("%d.%m.%Y")
                    })
        return upcoming_birthdays

# Main command functions
@input_error
def add_contact(args, book):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added."

@input_error
def change_contact(args, book):
    name, new_phone = args
    record = book.find(name)
    if record:
        # Replace the last phone number or add if none exist
        if record.phones:
            record.phones[-1] = new_phone  # Replace the last phone number
        else:
            record.add_phone(new_phone)  # Add if no phone exists
        return "Contact updated."
    else:
        raise ValueError(f"Contact {name} not found.")

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.phones:
        return f"{name}: {', '.join(record.phones)}"
    else:
        raise ValueError(f"No phone found for {name}.")

@input_error
def show_all_contacts(book):
    if not book.contacts:
        return "No contacts found."
    return "\n".join(f"{name}: {', '.join(record.phones)}" for name, record in book.contacts.items())

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday for {name} added: {birthday}."
    else:
        raise ValueError(f"No contact found with the name {name}.")

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is {record.birthday.value.strftime('%d.%m.%Y')}."
    else:
        raise ValueError(f"No birthday found for {name}.")

@input_error
def birthdays(book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No upcoming birthdays."
    return "\n".join(f"{entry['name']} - {entry['birthday']}" for entry in upcoming_birthdays)

# Main function to run the bot
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.split()

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all_contacts(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()