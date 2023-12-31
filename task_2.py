from collections import UserDict


class InvalidPhone(Exception):
    pass


class RecordNotFound(Exception):
    def __init__(self, name, *args):
        super().__init__(*args)
        self.name = name


class RecordConflict(Exception):
    def __init__(self, name, *args):
        super().__init__(*args)
        self.name = name


class PhoneNotFound(Exception):
    def __init__(self, phone, *args):
        super().__init__(*args)
        self.phone = phone


class PhoneConflict(Exception):
    def __init__(self, name, phone, *args):
        super().__init__(*args)
        self.name = name
        self.phone = phone


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise InvalidPhone

        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, new_phone):
        for phone in self.phones:
            if phone.value == new_phone:
                raise PhoneConflict(self.name.value, new_phone)

        self.phones.append(Phone(new_phone))
        return "Phone added."

    def remove_phone(self, phone):
        filtered_phone = list(filter(lambda p: p.value != phone, self.phones))

        if len(filtered_phone) == len(self.phones):
            raise PhoneNotFound(phone)
        else:
            self.phones = filtered_phone
            return "Phone removed."

    def edit_phone(self, old_phone, new_phone):
        new_phone = Phone(new_phone)

        for phone in self.phones:
            if phone.value == new_phone.value:
                raise PhoneConflict(self.name.value, new_phone.value)

        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = new_phone
                return "Phone edited."

        raise PhoneNotFound(old_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p

        raise PhoneNotFound(phone)


class AddressBook(UserDict):
    def __str__(self):
        return "".join([f"{record}\n" for record in self.data.values()]).rstrip("\n")

    def add_record(self, record):
        name = record.name.value

        if name in self.data:
            raise RecordConflict(name)
        else:
            self.data[name] = record
            return "Record added."

    def find(self, name):
        if not name in self.data:
            raise RecordNotFound(name)
        else:
            return self.data[name]

    def delete(self, name):
        if not name in self.data:
            raise RecordNotFound(name)
        else:
            self.data.pop(name)
            return "Record deleted."


def main():
    # Створення нової адресної книги

    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")


if __name__ == "__main__":
    main()
