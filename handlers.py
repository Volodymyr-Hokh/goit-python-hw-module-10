import csv
import os
import platform
import re
import sys

import classes
from data_manager import open_file_and_check_name, write_to_csv


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


@set_commands("add")
@input_error
def add_user(*args):
    """Take as input username and phone number and add them to the base.
    If username already exist add phone numbers to this user."""
    name = classes.Name(args[0])
    phone_numbers = [classes.Phone(phone) for phone in args[1:]]

    data, name_exists = open_file_and_check_name(name.value)

    if name_exists and phone_numbers:
        msg = data[name.value].add_phones(phone_numbers)
    elif not phone_numbers:
        raise IndexError
    else:
        record = classes.Record(name, *phone_numbers)
        data.add_record(record)
        msg = f"User {name} added successfully."

    write_to_csv(data, "data.csv")
    return msg


@set_commands("change")
@input_error
def change(*args):
    """Take as input username, old and new phone number 
    and changes the corresponding data."""
    name = classes.Name(args[0])
    old_phone = classes.Phone(args[1])
    new_phone = classes.Phone(args[2])

    data, name_exists = open_file_and_check_name(name.value)

    if not name_exists:
        msg = f"Name {name} doesn`t exists. "\
            "If you want to add it, please type 'add user <name> <phone number>'."
    else:
        msg = data[name.value].change_phone(old_phone, new_phone)

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


@set_commands("del user")
@input_error
def delete_user(*args):
    """Take as input username and delete that user"""
    name = classes.Name(args[0])

    data, name_exists = open_file_and_check_name(name.value)

    if not name_exists:
        return f"Name {name} doesn`t exists."
    else:
        data.delete_record(name)

    write_to_csv(data, "data.csv")
    return f"User {name} deleted successfully."


@set_commands("del phone")
@input_error
def delete_phone(*args):
    """Take as input username and phone number and delete that phone"""
    name = classes.Name(args[0])
    phone = classes.Phone(args[1])

    data, name_exists = open_file_and_check_name(name.value)

    if not name_exists:
        msg = f"Name {name} doesn`t exists."
    else:
        msg = data[name.value].delete_phone(phone)

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
    name = classes.Name(args[0])

    data, name_exists = open_file_and_check_name(name.value)

    if not name_exists:
        return f"Name {name} doesn`t exists. "\
            "If you want to add it, please type 'add <name> <phone number>'."
    else:
        phone_numbers = ", ".join(str(phone)
                                  for phone in data[name.value].phones)
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
                username = classes.Name(row["Name"])
                phones_str = re.sub(r"\[|\]|\ ", "",
                                    row["Phone numbers"]).split(",")
                phones = [classes.Phone(phone) for phone in phones_str]

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
