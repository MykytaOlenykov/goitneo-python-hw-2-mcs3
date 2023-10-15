def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name"
        except KeyError:
            return "Enter user name"

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def show_all(contacts):
    if not contacts:
        return "Your phone book is empty."

    contacts_data = ""

    for name, phone in contacts.items():
        contacts_data += f"|{name:^15}|{phone:^25}|\n"

    return contacts_data.rstrip("\n")


@input_error
def show_phone(args, contacts):
    name = args[0]
    phone = contacts.get(name)
    if phone:
        return phone
    else:
        return f"A person with name {name} is not in your phone book"


@input_error
def add_contact(args, contacts):
    name, phone = args
    if name in contacts:
        return f"A person with name {name} already exists."
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    name, phone = args
    if not name in contacts:
        return f"A person with name {name} is not in your phone book"
    contacts[name] = phone
    return "Contact updated."


def main():
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input(">>> Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "all":
            print(show_all(contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
