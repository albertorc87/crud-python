import re
import datetime

regex_email = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
regex_phone = '^[0-9]{9}$'

class Validations:

    def __init__(self):
        pass

    def validateName(self, name):
        if len(name) < 3 or len(name) > 50:
            raise ValueError(f'El nombre debe tener como mínimo 3 caractares y un máximo de 50 caracteres, tamaño actual: {len(name)}')
        return True

    def validateSurname(self, surname):
        if len(surname) < 5 or len(surname) > 100:
            raise ValueError(f'Los apellidos deben tener como mínimo 5 caractares y un máximo de 100 caracteres, tamaño actual: {len(surname)}')
        return True


    def validateEmail(self, email):
        if not re.search(regex_email, email):
            raise ValueError('El formato del email no es válido')
        return True

    def validatePhone(self, phone):
        if not re.search(regex_phone, phone):
            raise ValueError('El formato del teléfono no es válido, debe ser un número de 9 cifras sin guiones ni puntos')
        return True


    def validateBirthday(self, birthday):
        try:
            datetime.datetime.strptime(birthday, '%Y-%m-%d')
        except ValueError:
            raise ValueError('El formato de la fecha es incorrecta, debe ser YYYY-MM-DD')
        return True