from collections import UserDict


class InvalidPhoneLength(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10:
            raise InvalidPhoneLength

        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                print(f"{self.name}`s record contains this phone number: {phone}")
                return

        try:
            self.phones.append(Phone(phone))
        except InvalidPhoneLength:
            print("The phone number must be 10 characters long.")

    def remove_phone(self, phone):
        filtered_phone = list(filter(lambda p: p.value != phone, self.phones))

        if len(filtered_phone) == len(self.phones):
            print(f"{phone} phone number is not in the current record")
        else:
            self.phones = filtered_phone

    def edit_phone(self, old_phone, new_phone):
        try:
            for i, phone in enumerate(self.phones):
                if phone.value == old_phone:
                    self.phones[i] = Phone(new_phone)
                    return

            print(f"{self.name}`s record contains this phone number: {new_phone}")
        except InvalidPhoneLength:
            print("The phone number must be 10 characters long.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return phone

        return f"{phone} phone number is not in the current record"


class AddressBook(UserDict):
    def add_record(self, record):
        name = record.name.value

        if name in self.data:
            print(f"A person with name {name} already exists.")
        else:
            self.data[name] = record

    def find(self, name):
        if not name in self.data:
            return f"A person with name {name} is not in your phone book"
        else:
            return self.data.get(name)

    def delete(self, name):
        if not name in self.data:
            print(f"A person with name {name} is not in your phone book")
        else:
            self.data.pop(name)


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
