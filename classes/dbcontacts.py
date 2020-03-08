from .contact import Contact
from .dbcsv import DBbyCSV

SCHEMA = {
    'ID': {
        'type': 'autoincrement',
    }, 
    'NAME': {
        'type': 'string',
        'min_length': 3,
        'max_length': 50
    }, 
    'SURNAME': {
        'type': 'string',
        'min_length': 5,
        'max_length': 100
    }, 
    'EMAIL': {
        'type': 'string',
        'max_length': 254
    }, 
    'PHONE': {
        'type': 'int'
    }, 
    'BIRTHDAY': {
        'type': 'date'
    }
}

class DBContacts(DBbyCSV):

    def __init__(self):
        super().__init__(SCHEMA, 'contacts')

    
    def save_contact(self, contact):
        data = [contact.name, contact.surname, contact.email, contact.phone, contact.birthday]
        return self.insert(data)
    

    def update_contact(self, id_object, data):
        if not id_object:
            raise ValueError('Debes envíar el id del contacto')
        if not data:
            raise ValueError('Debes envíar al menos un parámetro a actualizar')
        self.update(id_object, data)


    def delete_contact(self, id_object):
        if not id_object:
            raise ValueError('Debes envíar el id del contacto')
        self.delete(id_object)


    def list_contacts(self):
        list_contacts = self.get_all()
        return self._create_object_contacts(list_contacts)

    
    def get_schema(self):
        return SCHEMA


    def search_contacts(self, filters):
        if 'NAME' not in filters and 'SURNAME' not in filters and 'EMAIL' not in filters:
            raise ValueError('Debes envíar al menos un filtro')

        list_contacts = self.get_by_filters(filters)
        return self._create_object_contacts(list_contacts)


    def _create_object_contacts(self, list_contacts):

        if not list_contacts:
            return None

        object_contacts = []
        # Convertimos los datos a objectos de tipo contact
        for contact in list_contacts:
            c = Contact(contact['ID'], contact['NAME'], contact['SURNAME'], contact['EMAIL'], contact['PHONE'], contact['BIRTHDAY'])
            object_contacts.append(c)

        return object_contacts