import re
import hashlib
import os

ARCHIVO_USUARIOS = "registro_usuarios.txt"
SESIÓN_ACTUAL = None  # Variable para mantener la sesión activa

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

def hash_contraseña(contraseña):
    return hashlib.sha256(contraseña.encode()).hexdigest()

def usuario_existe(usuario):
    if not os.path.exists(ARCHIVO_USUARIOS):
        return False
    with open(ARCHIVO_USUARIOS, "r") as archivo:
        for linea in archivo:
            if f"Usuario: {usuario}" in linea:
                return True
    return False

def registrar_usuario():
    print("Registro de usuario")
    nombre = input("Ingrese su nombre: ")
    
    while True:
        usuario = input("Ingrese su nombre de usuario: ")
        if usuario_existe(usuario):
            print("Ese nombre de usuario ya está en uso. Intente con otro.")
        else:
            break

    correo = input("Ingrese su correo electrónico: ")
    rol = input("Ingrese su rol (admin/usuario): ").strip().lower()
    if rol not in ["admin", "usuario"]:
        print("Rol inválido. Se asignará 'usuario' por defecto.")
        rol = "usuario"

    while True:
        contraseña = input("Ingrese su contraseña: ")
        error = validar_contraseña(contraseña)
        if error:
            print(f"Error: {error}")
            continue
        confirmar_contraseña = input("Confirme su contraseña: ")
        if contraseña != confirmar_contraseña:
            print("Las contraseñas no coinciden. Inténtelo de nuevo.")
        else:
            break

    contraseña_cifrada = hash_contraseña(contraseña)

    usuario_registrado = {
        "Nombre": nombre,
        "Usuario": usuario,
        "Correo": correo,
        "Rol": rol,
        "Contraseña": contraseña_cifrada  # Almacena la versión cifrada
    }

    with open(ARCHIVO_USUARIOS, "a") as archivo:
        for key, value in usuario_registrado.items():
            archivo.write(f"{key}: {value}\n")
        archivo.write("\n")  # Agrega un salto de línea para separar usuarios
    
    print("Registro exitoso!")
    return usuario_registrado

def iniciar_sesion():
    global SESIÓN_ACTUAL
    print("\nInicio de sesión")
    usuario = input("Ingrese su nombre de usuario: ")
    contraseña = input("Ingrese su contraseña: ")
    contraseña_cifrada = hash_contraseña(contraseña)

    if not os.path.exists(ARCHIVO_USUARIOS):
        print("No hay usuarios registrados.")
        return None

    with open(ARCHIVO_USUARIOS, "r") as archivo:
        datos_usuario = {}
        for linea in archivo:
            if linea.strip():  # Evitar líneas vacías
                clave, valor = linea.strip().split(": ", 1)
                datos_usuario[clave] = valor
            else:
                if datos_usuario.get("Usuario") == usuario and datos_usuario.get("Contraseña") == contraseña_cifrada:
                    SESIÓN_ACTUAL = datos_usuario
                    print(f"\nBienvenido, {usuario} ({datos_usuario['Rol']})")
                    return datos_usuario
                datos_usuario = {}

    print("Usuario o contraseña incorrectos.")
    return None

def cerrar_sesion():
    global SESIÓN_ACTUAL
    if SESIÓN_ACTUAL:
        print(f"\nCerrando sesión de {SESIÓN_ACTUAL['Usuario']}")
        SESIÓN_ACTUAL = None
    else:
        print("\nNo hay ninguna sesión activa.")

# Menú principal
while True:
    print("\nMenú Principal")
    print("1. Registrar usuario")
    print("2. Iniciar sesión")
    print("3. Cerrar sesión")
    print("4. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        registrar_usuario()
    elif opcion == "2":
        iniciar_sesion()
    elif opcion == "3":
        cerrar_sesion()
    elif opcion == "4":
        print("\nSaliendo del sistema...")
        break
    else:
        print("\nOpción inválida, intente de nuevo.")
