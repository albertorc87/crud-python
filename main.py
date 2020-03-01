import os
import time
from classes.validations import Validations
from classes.contact import Contact
from classes.dbcontacts import DBContacts
from prettytable import PrettyTable
validator = Validations()
db = DBContacts()


def print_options():
    print('AGENDA DE CONTACTOS')
    print('*' * 50)
    print('Selecciona una opción:')
    print('[C]rear contacto')
    print('[L]istado de contactos')
    print('[M]odificar contacto')
    print('[E]liminar contacto')
    print('[B]uscar contacto')
    print('[S]ALIR')


def check_contact_data(message, data_name):
    print(message)
    input_data = input()
    try:
        getattr(validator, f'validate{data_name.capitalize()}')(input_data)
        return input_data
    except ValueError as err:
        print(err)
        check_contact_data(message, data_name)


def check_name():
    print('Inserta el nombre:')
    name = input()
    try:
        validator.validateName(name)
        return name
    except ValueError as err:
        print(err)
        check_name()


def check_surname():
    print('Inserta los apellidos:')
    surname = input()
    try:
        validator.validateSurname(surname)
        return surname
    except ValueError as err:
        print(err)
        check_surname()


def check_email():
    print('Inserta el email:')
    email = input()
    try:
        validator.validateEmail(email)
        return email
    except ValueError as err:
        print(err)
        check_email()


def check_phone():
    print('Inserta el teléfono (9 cifras sin guiones ni puntos):')
    phone = input()
    try:
        validator.validatePhone(phone)
        return phone
    except ValueError as err:
        print(err)
        check_phone()


def check_birthday():
    print('Inserta la fecha de nacimiento (YYYY-MM-DD):')
    birthday = input()
    try:
        validator.validateBirthday(birthday)
        return birthday
    except ValueError as err:
        print(err)
        check_birthday()


def create_contact():

    print('CREACIÓN DE CONTACTO')
    print('*' * 50)
    name = check_contact_data('Inserta el nombre:', 'name')
    surname = check_contact_data('Inserta los apellidos:', 'surname')
    email = check_contact_data('Inserta el email:', 'email')
    phone = check_contact_data('Inserta el teléfono (9 cifras sin guiones ni puntos):', 'phone')
    birthday = check_contact_data('Inserta la fecha de nacimiento (YYYY-MM-DD):', 'birthday')

    contact = Contact(None, name, surname, email, phone, birthday)
    if db.save_contact(contact):
        print('Contacto insertado con éxito')
    else:
        print('Error al guardar el contacto')


def list_contacts():
    list_contacts = db.list_contacts()

    if not list_contacts:
        return print('Todavía no hay contactos guardados')

    table = PrettyTable(db.get_schema().keys())
    for contact in list_contacts:
        table.add_row([
            contact.id_contact,
            contact.name,
            contact.surname,
            contact.email,
            contact.phone,
            contact.birthday
        ])

    print(table)
    print('Pulsa cualquier letra para salir')
    command = input()

def run():
    print_options()

    command = input()
    command = command.upper()

    if command == 'C':
        create_contact()
    elif command == 'L':
        list_contacts()
    elif command == 'M':
        pass
    elif command == 'E':
        pass
    elif command == 'B':
        pass
    elif command == 'S':
        os._exit(1)
    else:
        print('Comando inválido')

    time.sleep(1)
    run()

if __name__ == "__main__":
    run()