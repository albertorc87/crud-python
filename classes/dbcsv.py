import csv
import re
from tempfile import NamedTemporaryFile
import shutil


class DBbyCSV:

    def __init__(self, schema, filename):
        self._filename = f'./{filename}.csv'
        try:
            # Verificamos si ya existe el archivo
            f = open(self._filename)
            f.close()
        except IOError:
            # Si el archivo no existe creamos la cabecera
            with open(self._filename, mode='w', encoding='utf-16') as csv_file:
                data_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
                data_writer.writerow(schema.keys())
            

    def insert(self, data):

        id_contact = self.get_last_id() + 1
        line = [id_contact] + data

        with open(self._filename, mode='a', encoding='utf-16') as csv_file:
            data_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            data_writer.writerow(line)

        return True


    def get_last_id(self):
        
        list_ids = []
        with open(self._filename, mode='r', encoding='utf-16') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            is_header = True
            for row in csv_reader:
                if is_header:
                    is_header = False
                    continue

                if row:
                    list_ids.append(row[0])

        if not list_ids:
            return 0
        
        # Ordenamos la lista de mayor a menor y retornamos el elemento de mayor tamaño
        list_ids.sort(reverse = True) 
        return int(list_ids[0])


    def get_all(self):

        list_data = []
        list_header = []
        with open(self._filename, mode='r', encoding='utf-16') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            is_header = True
            for row in csv_reader:
                if is_header:
                    list_header = row
                    is_header = False
                    continue

                if row:
                    file = {}
                    for key, value in enumerate(row):
                        file[list_header[key]] = value

                    list_data.append(file)

        return list_data


    def get_by_filters(self, filters):

        list_data = []
        list_header = []
        with open(self._filename, mode='r', encoding='utf-16') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            is_header = True
            for row in csv_reader:
                if is_header:
                    list_header = row
                    is_header = False
                    continue

                if row:
                    file = {}

                    for key, value in enumerate(row):
                        file[list_header[key]] = value
                    
                    for key_filter, value_filter in filters.items():
                        matches = re.search(rf"{value_filter}", file[key_filter], re.IGNORECASE)
                        if matches:
                            list_data.append(file)
                            break

        return list_data

    def delete(self, id_object):
        return self.modify_file(id_object, {}, 'delete')

    def update(self, id_object, data):
        return self.modify_file(id_object, data, 'update')

    def modify_file(self, id_object, data, action):
        data_csv = self.get_by_id(id_object)

        if not data_csv:
            raise Exception('No se ha encontrado el objecto con el id enviado')

        for key, value in data.items():
            data_csv[key] = value

        tempfile = NamedTemporaryFile(mode='w', delete=False, encoding='utf-16')

        list_header = []
        with open(self._filename, mode='r', encoding='utf-16') as csv_file, tempfile:
            csv_reader = csv.reader(csv_file, delimiter=';')
            data_writer = csv.writer(tempfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

            is_header = True
            for row in csv_reader:
                if is_header:
                    list_header = row
                    is_header = False
                    data_writer.writerow(row)
                    continue

                # Si es update, actualizamos cuando hacemos match
                if row and action == 'update':
                    file = {}
                    for key, value in enumerate(row):
                        file[list_header[key]] = value
                    
                    if file['ID'] != data_csv['ID']:
                        data_writer.writerow(row)
                        continue

                    for key, value in data_csv.items():
                        file[key] = value

                    data_writer.writerow(file.values())
                # Si es delete cuando hacemos match continuamos para saltarnos el insertado de esa línea
                elif row and action == 'delete':
                    file = {}
                    for key, value in enumerate(row):
                        file[list_header[key]] = value
                    
                    if file['ID'] == data_csv['ID']:
                        continue

                    data_writer.writerow(row)

        shutil.move(tempfile.name, self._filename)
        return True


    def get_by_id(self, id_object):
        list_header = []
        with open(self._filename, mode='r', encoding='utf-16') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            is_header = True
            for row in csv_reader:
                if is_header:
                    list_header = row
                    is_header = False
                    continue

                if row:
                    file = {}
                    for key, value in enumerate(row):
                        file[list_header[key]] = value
                    if file['ID'] == id_object:
                        return file

        return {}