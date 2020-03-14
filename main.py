import os
import time
from classes.validations import Validations
from classes.contact import Contact
from classes.dbcontacts import DBContacts
from prettytable import PrettyTable
validator = Validations()
db = DBContacts()
from classes.dbpostgresql import DBPostgresql

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


def check_contact_data(message, data_name, force = True):
    print(message)
    input_data = input()
    if not force and not input_data:
        return
    try:
        getattr(validator, f'validate{data_name.capitalize()}')(input_data)
        return input_data
    except ValueError as err:
        print(err)
        return check_contact_data(message, data_name, force)


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

    _print_table_contacts(list_contacts)


def search_contact():

    filters = {}
    print('Introduce un nombre (vacío para usar otro filtro):')
    nombre = input()
    if nombre:
        filters['NAME'] = nombre
    print('Introduce un apellido (vacío para usar otro filtro):')
    apellidos = input()
    if apellidos:
        filters['SURNAME'] = apellidos
    print('Introduce un email (vacío para usar otro filtro):')
    email = input()
    if email:
        filters['EMAIL'] = email

    try:
        list_contacts = db.search_contacts(filters)
        if not list_contacts:
            return print('No hay ningún contacto con esos criterios de búsqueda')

        _print_table_contacts(list_contacts)
    except ValueError as err:
        print(err)
        time.sleep(1)
        search_contact()


def update_contact():

    list_contacts()

    print('Introduce el id del contacto que quieres actualizar:')
    id_object = input()

    data = {}
    nombre = check_contact_data('Introduce un nombre (vacío para mantener el nombre actual):', 'name', False)
    if nombre:
        data['name'] = nombre
    apellidos = check_contact_data('Introduce un apellido (vacío para mantener los apellidos actuales):', 'surname', False)
    if apellidos:
        data['surname'] = apellidos
    email = check_contact_data('Introduce un email (vacío para mantener el email actual):', 'email', False)
    if email:
        data['email'] = email
    phone = check_contact_data('Introduce un teléfono (vacío para mantener el teléfono actual):', 'phone', False)
    if phone:
        data['phone'] = phone
    birthday = check_contact_data('Introduce una fecha de nacimiento YYYY-MM-DD (vacío para mantener la fecha actual):', 'birthday', False)
    if birthday:
        data['birthday'] = birthday
    
    try:
        res = db.update(id_object, data)
        if res:
            print('Contacto actualizado con éxito')
    except Exception as err:
        print(err)
        time.sleep(1)
        update_contact()

def delete_contact():
    list_contacts()

    print('Introduce el id del contacto que quieres eliminar:')
    id_object = input()
    try:
        res = db.delete(id_object)
        if res:
            print('Contacto eliminado con éxito')
    except Exception as err:
        print(err)
        time.sleep(1)
        delete_contact()
    

def _print_table_contacts(list_contacts):
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
    print('Pulsa cualquier letra para continuar')
    command = input()

def run():

    # data = {
    #     'name':'Peter', 
    #     'surname':'Paulin', 
    #     'email':'peter@cosas.com', 
    #     'phone':'999929999', 
    #     'birthday':'1977-01-21'
    # }
    # return db.insert(data)

    print_options()

    command = input()
    command = command.upper()

    if command == 'C':
        create_contact()
    elif command == 'L':
        list_contacts()
    elif command == 'M':
        update_contact()
    elif command == 'E':
        delete_contact()
    elif command == 'B':
        search_contact()
    elif command == 'S':
        os._exit(1)
    else:
        print('Comando inválido')

    time.sleep(1)
    run()

if __name__ == "__main__":
    run()