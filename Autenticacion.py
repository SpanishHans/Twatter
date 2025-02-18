import sqlite3
import hashlib
import re
from datetime import datetime

DB_NAME = "usuarios.db"

# Conectar a la base de datos y crear la tabla si no existe
def inicializar_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS USUARIOS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_usuario TEXT UNIQUE NOT NULL,
                correo TEXT UNIQUE NOT NULL,
                contrasena_hash TEXT NOT NULL,
                foto_perfil TEXT,
                biografia TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

# Validar la seguridad de la contraseña
def validar_contraseña(contraseña):
    if len(contraseña) < 8:
        return "La contraseña debe tener al menos 8 caracteres."
    if not re.search(r"[A-Z]", contraseña):
        return "La contraseña debe contener al menos una letra mayúscula."
    if not re.search(r"\d", contraseña):
        return "La contraseña debe contener al menos un número."
    if not re.search(r"[!@#$%^&*(),.?'+-/:{}|<>]", contraseña):
        return "La contraseña debe contener al menos un carácter especial."
    return None

# Hash de la contraseña
def hash_contraseña(contraseña):
    return hashlib.sha256(contraseña.encode()).hexdigest()

# Verificar si el usuario existe
def usuario_existe(usuario):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM USUARIOS WHERE nombre_usuario = ?", (usuario,))
        return cursor.fetchone() is not None

# Registrar un usuario
def registrar_usuario():
    print("Registro de usuario")
    nombre_usuario = input("Ingrese su nombre de usuario: ")
    if usuario_existe(nombre_usuario):
        print("Ese nombre de usuario ya está en uso.")
        return

    correo = input("Ingrese su correo electrónico: ")
    while True:
        contraseña = input("Ingrese su contraseña: ")
        error = validar_contraseña(contraseña)
        if error:
            print(f"Error: {error}")
            continue
        confirmar_contraseña = input("Confirme su contraseña: ")
        if contraseña != confirmar_contraseña:
            print("Las contraseñas no coinciden.")
        else:
            break

    contrasena_hash = hash_contraseña(contraseña)
    fecha_creacion = datetime.now()

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO USUARIOS (nombre_usuario, correo, contrasena_hash, fecha_creacion)
            VALUES (?, ?, ?, ?)
        ''', (nombre_usuario, correo, contrasena_hash, fecha_creacion))
        conn.commit()
    print("Registro exitoso!")

# Iniciar sesión
def iniciar_sesion():
    print("\nInicio de sesión")
    usuario = input("Ingrese su nombre de usuario: ")
    contraseña = input("Ingrese su contraseña: ")
    contraseña_cifrada = hash_contraseña(contraseña)

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USUARIOS WHERE nombre_usuario = ? AND contrasena_hash = ?", (usuario, contraseña_cifrada))
        usuario_encontrado = cursor.fetchone()

    if usuario_encontrado:
        print(f"\nBienvenido, {usuario}")
    else:
        print("Usuario o contraseña incorrectos.")

# Menú principal
inicializar_db()
while True:
    print("\nMenú Principal")
    print("1. Registrar usuario")
    print("2. Iniciar sesión")
    print("3. Salir")
    
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1":
        registrar_usuario()
    elif opcion == "2":
        iniciar_sesion()
    elif opcion == "3":
        print("\nSaliendo del sistema...")
        break
    else:
        print("\nOpción inválida, intente de nuevo.")
