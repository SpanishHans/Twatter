from flask import Flask, request, jsonify
import bcrypt
import logging
from mod_conn import get_db_connection
from mod_token import generate_token  
from flask_limiter import Limiter

app = Flask(__name__)
limiter = Limiter(app, key_func=lambda: 'global')  

logging.basicConfig(level=logging.INFO)

# Endpoint de registro
@app.route('/registro', methods=['POST'])
def post_register():
    data = request.get_json()

    # Validar los datos de entrada
    nombre_usuario = data.get('nombre_usuario')
    correo = data.get('correo')
    contrasena = data.get('clave')
    biografia = data.get('biografia')

    # Comprobar campos obligatorios
    if not nombre_usuario or not contrasena or not correo:
        return jsonify({"error": "Se requiere nombre de usuario, correo y contraseña!"}), 400

    # Hashear la contraseña
    hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())

    connection = None
    try:
        connection = get_db_connection()  # Obtener conexión a la base de datos
        with connection.cursor() as cursor:
            # Comprobar si el usuario ya existe
            cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s", (nombre_usuario,))
            if cursor.fetchone():
                logging.warning(f"||post_register|| Registro fallido: el usuario '{nombre_usuario}' ya existe.")
                return jsonify({"error": "Nombre de usuario ya existe!"}), 409

            # Insertar nuevo usuario
            cursor.execute(
                "INSERT INTO usuarios (nombre_usuario, correo, clave, biografia) VALUES (%s, %s, %s, %s)",
                (nombre_usuario, correo, hashed_password, biografia)
            )
            connection.commit()
            logging.info(f"||post_register|| Usuario '{nombre_usuario}' registrado exitosamente.")

    except Exception as e:
        logging.error(f"||post_register|| Error en la base de datos durante el registro: {e}")
        return jsonify({"error": "Problema en la base de datos."}), 500

    finally:
        if connection:
            connection.close()  # Asegurarse de que la conexión se cierre

    return jsonify({"message": "Usuario registrado exitosamente!"}), 201

# Endpoint de inicio de sesión
@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Limitar el número de solicitudes para evitar abusos
def post_login():
    data = request.get_json()
    nombre_usuario = data.get('nombre_usuario')
    contrasena = data.get('clave')
    
    if not nombre_usuario or not contrasena:
        logging.error("||post_login|| Error: Se requiere nombre de usuario y contraseña!")
        return jsonify({"error": "Se requiere nombre de usuario y contraseña!"}), 400

    connection = None
    try:
        connection = get_db_connection()  # Obtener conexión a la base de datos
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, clave, biografia FROM usuarios WHERE nombre_usuario = %s", (nombre_usuario,))
            user = cursor.fetchone()
        
        if user and bcrypt.checkpw(contrasena.encode('utf-8'), user[1].encode('utf-8')):
            token = generate_token(user_id=user[0])  # Generar token
            logging.info(f"||post_login|| Ha entrado el usuario {nombre_usuario}")
            return jsonify({"token": token, "id": user[0], "biografia": user[2]}), 200
        else:
            logging.error(f"||post_login|| Error: Credenciales inválidas para usuario {nombre_usuario}")
            return jsonify({"error": "Credenciales inválidas"}), 401
    
    except Exception as e:
        logging.error(f"||post_login|| Error en la base de datos durante el inicio de sesión: {e}")
        return jsonify({"error": "Problema en la base de datos"}), 500
    
    finally:
        if connection:
            connection.close()  # Asegurarse de que la conexión se cierre

if __name__ == '__main__':
    app.run(debug=True)
