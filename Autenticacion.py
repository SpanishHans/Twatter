from flask import Flask, request, jsonify
import sqlite3
import hashlib
import re
from datetime import datetime

app = Flask(__name__)
DB_NAME = "usuarios.db"

def inicializar_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS USUARIOS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_usuario TEXT UNIQUE NOT NULL,
                correo TEXT UNIQUE NOT NULL,
                contrasena_hash TEXT NOT NULL,
                biografia TEXT,  -- Agregado campo de biografía
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

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
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM USUARIOS WHERE nombre_usuario = ?", (usuario,))
        return cursor.fetchone() is not None

@app.route("/registro", methods=["POST"])
def registrar_usuario():
    data = request.json
    nombre_usuario = data.get("nombre_usuario")
    correo = data.get("correo")
    contraseña = data.get("contrasena")
    biografia = data.get("biografia")  # Obtener biografía
    
    if usuario_existe(nombre_usuario):
        return jsonify({"error": "Ese nombre de usuario ya está en uso."}), 400
    
    error = validar_contraseña(contraseña)
    if error:
        return jsonify({"error": error}), 400
    
    contrasena_hash = hash_contraseña(contraseña)
    fecha_creacion = datetime.now()
    
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO USUARIOS (nombre_usuario, correo, contrasena_hash, biografia, fecha_creacion)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre_usuario, correo, contrasena_hash, biografia, fecha_creacion))
        conn.commit()
    
    return jsonify({"mensaje": "Registro exitoso!"}), 201

@app.route("/login", methods=["POST"])
def iniciar_sesion():
    data = request.json
    usuario = data.get("nombre_usuario")
    contraseña = data.get("contrasena")
    contraseña_cifrada = hash_contraseña(contraseña)
    
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nombre_usuario, biografia FROM USUARIOS WHERE nombre_usuario = ? AND contrasena_hash = ?", (usuario, contraseña_cifrada))
        usuario_encontrado = cursor.fetchone()
    
    if usuario_encontrado:
        return jsonify({"mensaje": f"Bienvenido, {usuario_encontrado[0]}", "biografia": usuario_encontrado[1]}), 200
    else:
        return jsonify({"error": "Usuario o contraseña incorrectos."}), 401

@app.route("/verificar_usuario", methods=["GET"])
def verificar_usuario():
    nombre_usuario = request.args.get("nombre_usuario")
    if usuario_existe(nombre_usuario):
        return jsonify({"existe": True}), 200
    else:
        return jsonify({"existe": False}), 404
    
@app.route("/", methods=["GET"])
def home():
    return jsonify({"routes": ["/registro", "/login", "/verificar_usuario"]}), 200


if __name__ == "__main__":
    inicializar_db()
    app.run(host="0.0.0.0", port=5001, debug=True)
