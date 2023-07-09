from collections import UserDict


class Field:
    def __init__(self, value=None, required=False):
        self.value = value
        self.required = required
        if required and not value:
            raise ValueError("Required field is not provided.")

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)


class Name(Field):
    def __eq__(self, other):
        if isinstance(other, Name):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)


class Phone(Field):
    def __eq__(self, other):
        if isinstance(other, Phone):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)


class Record:
    def __init__(self, name=None, *phones):
        self.name = name
        self.phones = list(phones)

    def __str__(self):
        return f"{self.name.value}: {self.phones}"

    def __repr__(self):
        return str(self)

    def add_phones(self, phones: list[Phone]):
        self.phones.extend(phones)
        self.phones = list(set(self.phones))
        phones_values = [phone.value for phone in phones]
        return f"Phone numbers {', '.join(phones_values)} for user {self.name.value} added successfully."

    def change_phone(self, old_number: Phone, new_number: Phone):
        if old_number not in self.phones:
            return f"Number {old_number} not found."
        else:
            phone_number_index = self.phones.index(old_number)
            self.phones[phone_number_index] = new_number
            return f"The phone number {old_number} for the user {self.name} "\
                f"has been changed to {new_number}"

    def delete_phone(self, phone):
        try:
            self.phones.remove(phone)
            return f"Phone number {phone} for user {self.name} deleted successfully."
        except ValueError:
            return f"Phone number {phone} for user {self.name} not found"


class AddressBook(UserDict):
    def add_record(self, record):
        self[record.name.value] = record

    def delete_record(self, name: Name):
        del self[name.value]

    def change_record(self, name, new_record):
        self[new_record.name.value] = new_record
