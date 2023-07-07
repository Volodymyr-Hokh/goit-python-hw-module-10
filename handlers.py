import csv
import os
import platform
import re
import sys

import classes
from other import open_file_and_check_name, write_to_csv


commands = {}


def set_commands(name, *additional):
    def inner(func):
        commands[name] = func
        for command in additional:
            commands[command] = func
    return inner


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except (IndexError, ValueError):
            return "Enter all require arguments please.\nTo see more info type 'help'."
    inner.__doc__ = func.__doc__
    return inner


@set_commands("adduser")
@input_error
def add_user(*args):
    """Take as input username and phone number and add them to the base."""
    name = args[0]
    phone_numbers = args[1:]

    data, name_exists = open_file_and_check_name(name)
    print(data)

    if name_exists:
        return f"Name {name} already exists. "\
            "If you want to change it, please type 'change <name> <phone number>'."
    else:
        record = classes.Record(name, *phone_numbers)
        data.add_record(record)

    write_to_csv(data, "data.csv")
    print(data)
    return f"User {name} added successfully."


@set_commands("addphone")
@input_error
def add_phone(*args):
    """Take as input username and phone number and add the number for user."""

    name = args[0]
    phone_number = classes.Phone(args[1])

    data, name_exists = open_file_and_check_name(name)

    if not name_exists:
        msg = f"Name {name} doesn`t exists. "\
            "If you want to add it, please type 'add user <name> <phone number>'."
    else:
        msg = data[name].add_phone(phone_number)

    write_to_csv(data, "data.csv")
    return msg


@set_commands("changeuser")
@input_error
def change_user(*args):
    """Take as input username and phone number and changes the corresponding data."""
    name = args[0]
    phone_numbers = args[1:]

    data, name_exists = open_file_and_check_name(name)

    if not name_exists:
        return f"Name {name} doesn`t exists. "\
            "If you want to add it, please type 'add <name> <phone number>'."
    else:
        record = classes.Record(name, *phone_numbers)
        data.change_record(name, record)

    write_to_csv(data, "data.csv")
    return f"Phone numbers for {name} has been updated."


@set_commands("changephone")
@input_error
def change_phone(*args):
    """Take as input username, old and new phone number and changes the corresponding data."""
    name = args[0]
    old_phone = classes.Phone(args[1])
    new_phone = classes.Phone(args[2])

    data, name_exists = open_file_and_check_name(name)

    if not name_exists:
        msg = f"Name {name} doesn`t exists. "\
            "If you want to add it, please type 'add user <name> <phone number>'."
    else:
        msg = data[name].change_phone(old_phone, new_phone)

    write_to_csv(data, "data.csv")
    return msg


@set_commands("clear")
@input_error
def clear(*args):
    """Clear the console."""
    system = platform.system()
    if system == "Windows":
        os.system("cls")
    elif system in ("Linux", "Darwin"):
        os.system("clear")
    else:
        return "Sorry, this command is not available on your operating system."


@set_commands("deluser")
@input_error
def delete_user(*args):
    """Take as input username and delete that user"""
    name = args[0]

    data, name_exists = open_file_and_check_name(name)

    if not name_exists:
        return f"Name {name} doesn`t exists."
    else:
        data.delete_record(name)

    write_to_csv(data, "data.csv")
    return f"User {name} deleted successfully."


@set_commands("delphone")
@input_error
def delete_phone(*args):
    name = args[0]
    phone = classes.Phone(args[1])

    data, name_exists = open_file_and_check_name(name)

    if not name_exists:
        msg = f"Name {name} doesn`t exists."
    else:
        msg = data[name].delete_phone(phone)

    write_to_csv(data, "data.csv")
    return msg


@set_commands("hello")
@input_error
def hello(*args):
    """Greet user."""
    return "How can I help you?"


@set_commands("help")
@input_error
def help_command(*args):
    """Show all commands available."""
    all_commands = ""
    for command, func in commands.items():
        all_commands += f"{command}: {func.__doc__}\n"
    return all_commands


@set_commands("phone")
@input_error
def phone(*args):
    """Take as input username and show user`s phone number."""
    name = args[0]

    data, name_exists = open_file_and_check_name(name)

    if not name_exists:
        return f"Name {name} doesn`t exists. "\
            "If you want to add it, please type 'add <name> <phone number>'."
    else:
        phone_numbers = ", ".join(str(phone) for phone in data[name].phones)
        return f"Phone numbers for {name}: {phone_numbers}."


@set_commands("show all")
@input_error
def show_all(*args):
    """Show all users."""
    try:
        with open("data.csv") as file:
            reader = csv.DictReader(file)
            data = classes.AddressBook()
            for row in reader:
                username = row["Name"]
                phones = re.sub(r"\[|\]|\ ", "",
                                row["Phone numbers"]).split(",")
                record = classes.Record(username, *phones)
                data[record.name.value] = record

    except FileNotFoundError:
        data = classes.AddressBook()

    all_users = ""
    for record in data.values():
        phone_numbers = ", ".join(str(phone) for phone in record.phones)
        all_users += f"{record.name}: {phone_numbers}\n"
    return all_users


@set_commands("exit", "close", "good bye")
@input_error
def exit(*args):
    """Interrupt program."""
    sys.exit(0)
