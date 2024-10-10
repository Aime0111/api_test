import mysql.connector
import json
from config import db_config
import os
from dotenv import load_dotenv

"""
# Configuración de la base de datos (cambia estos valores con los tuyos)
db_config = {
    'user': 'root',
    'password': 'root',
    'host': '68.183.130.198',  # La IP de tu VPS
    'port': 3308,         # El puerto donde está expuesto MySQL
    'database': 'mysql'
}
"""
# Cargar las variables de entorno
load_dotenv()

db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME')
}

# Función para conectarse a la base de datos
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Mostrar todos los estudiantes
def mostrar_estudiantes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estudiantes")
    estudiantes = cursor.fetchall()
    cursor.close()
    conn.close()

    if estudiantes:
        print(json.dumps(estudiantes, indent=4))
    else:
        print("No se encontraron estudiantes.")

# Agregar un nuevo estudiante
def agregar_estudiante(no_control, nombre, ap_paterno, ap_materno, semestre):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO estudiantes (no_control, nombre, ap_paterno, ap_materno, semestre) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (no_control, nombre, ap_paterno, ap_materno, semestre))
    conn.commit()
    cursor.close()
    conn.close()
    print("Estudiante agregado exitosamente.")

# Actualizar un estudiante existente
def actualizar_estudiante(no_control, nombre, ap_paterno, ap_materno, semestre):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE estudiantes SET nombre=%s, ap_paterno=%s, ap_materno=%s, semestre=%s WHERE no_control=%s"
    cursor.execute(query, (nombre, ap_paterno, ap_materno, semestre, no_control))
    conn.commit()
    cursor.close()
    conn.close()
    print("Estudiante actualizado exitosamente.")

# Eliminar un estudiante
def eliminar_estudiante(no_control):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM estudiantes WHERE no_control=%s"
    cursor.execute(query, (no_control,))
    conn.commit()
    cursor.close()
    conn.close()
    print("Estudiante eliminado exitosamente.")

# Guardar datos de estudiantes en archivo JSON
def guardar_json(estudiantes):
    with open('estudiantes.json', 'w') as archivo:
        json.dump(estudiantes, archivo, indent=4)
    print("Datos guardados en 'estudiantes.json'.")

# Menú principal de la API
def main():
    while True:
        print("\n--- Menú ---")
        print("1. Mostrar estudiantes")
        print("2. Agregar estudiante")
        print("3. Actualizar estudiante")
        print("4. Eliminar estudiante")
        print("5. Guardar estudiantes en archivo JSON")
        print("6. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            mostrar_estudiantes()
        elif opcion == '2':
            no_control = input("No. Control: ")
            nombre = input("Nombre: ")
            ap_paterno = input("Apellido Paterno: ")
            ap_materno = input("Apellido Materno: ")
            semestre = int(input("Semestre: "))
            agregar_estudiante(no_control, nombre, ap_paterno, ap_materno, semestre)
        elif opcion == '3':
            no_control = input("No. Control del estudiante a actualizar: ")
            nombre = input("Nombre: ")
            ap_paterno = input("Apellido Paterno: ")
            ap_materno = input("Apellido Materno: ")
            semestre = int(input("Semestre: "))
            actualizar_estudiante(no_control, nombre, ap_paterno, ap_materno, semestre)
        elif opcion == '4':
            no_control = input("No. Control del estudiante a eliminar: ")
            eliminar_estudiante(no_control)
        elif opcion == '5':
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM estudiantes")
            estudiantes = cursor.fetchall()
            cursor.close()
            conn.close()
            guardar_json(estudiantes)
        elif opcion == '6':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == '__main__':
    main()


""" 
import requests
import json

API_URL = 'http://127.0.0.1:5000/estudiantes'

def mostrar_estudiantes():
    response = requests.get(API_URL)
    if response.status_code == 200:
        estudiantes = response.json()
        print(json.dumps(estudiantes, indent=4))
    else:
        print(f"Error al obtener los estudiantes. Código de respuesta: {response.status_code}")

def agregar_estudiante(no_control, nombre, ap_paterno, ap_materno, semestre):
    estudiante = {
        'no_control': no_control,
        'nombre': nombre,
        'ap_paterno': ap_paterno,
        'ap_materno': ap_materno,
        'semestre': semestre
    }
    response = requests.post(API_URL, json=estudiante)
    if response.status_code == 201:
        print("Estudiante agregado exitosamente.")
    else:
        print(f"Error al agregar el estudiante. Código de respuesta: {response.status_code}")

def actualizar_estudiante(no_control, nombre, ap_paterno, ap_materno, semestre):
    estudiante = {
        'nombre': nombre,
        'ap_paterno': ap_paterno,
        'ap_materno': ap_materno,
        'semestre': semestre
    }
    response = requests.put(f"{API_URL}/{no_control}", json=estudiante)
    if response.status_code == 200:
        print("Estudiante actualizado exitosamente.")
    else:
        print(f"Error al actualizar el estudiante. Código de respuesta: {response.status_code}")

def eliminar_estudiante(no_control):
    response = requests.delete(f"{API_URL}/{no_control}")
    if response.status_code == 200:
        print("Estudiante eliminado exitosamente.")
    else:
        print(f"Error al eliminar el estudiante. Código de respuesta: {response.status_code}")

def guardar_json(estudiantes):
    with open('estudiantes.json', 'w') as archivo:
        json.dump(estudiantes, archivo, indent=4)
    print("Datos guardados en 'estudiantes.json'.")

def main():
    while True:
        print("\n--- Menú ---")
        print("1. Mostrar estudiantes")
        print("2. Agregar estudiante")
        print("3. Actualizar estudiante")
        print("4. Eliminar estudiante")
        print("5. Guardar estudiantes en archivo JSON")
        print("6. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            mostrar_estudiantes()
        elif opcion == '2':
            no_control = input("No. Control: ")
            nombre = input("Nombre: ")
            ap_paterno = input("Apellido Paterno: ")
            ap_materno = input("Apellido Materno: ")
            semestre = int(input("Semestre: "))
            agregar_estudiante(no_control, nombre, ap_paterno, ap_materno, semestre)
        elif opcion == '3':
            no_control = input("No. Control del estudiante a actualizar: ")
            nombre = input("Nombre: ")
            ap_paterno = input("Apellido Paterno: ")
            ap_materno = input("Apellido Materno: ")
            semestre = int(input("Semestre: "))
            actualizar_estudiante(no_control, nombre, ap_paterno, ap_materno, semestre)
        elif opcion == '4':
            no_control = input("No. Control del estudiante a eliminar: ")
            eliminar_estudiante(no_control)
        elif opcion == '5':
            response = requests.get(API_URL)
            if response.status_code == 200:
                estudiantes = response.json()
                guardar_json(estudiantes)
            else:
                print(f"Error al obtener los estudiantes. Código de respuesta: {response.status_code}")
        elif opcion == '6':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == '__main__':
    main()
"""