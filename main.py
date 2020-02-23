import os
import time


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


def run():
    print_options()

    command = input()
    command = command.upper()

    if command == 'C':
        pass
    elif command == 'L':
        pass
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