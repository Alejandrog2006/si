# Autores: Alejandro González y Manuel Salvador

# Microservicio de usuario
import hashlib # para hashear la contraseña
import uuid # para generar UIDs y tokens
from quart import Quart, jsonify, request # en presentacion, para el framework

app = Quart(__name__) # iniciar app y espera http 

# Secreto compartido entre microservicios (fijado para que sea persistente)
SECRET_UUID = uuid.UUID("12345678-1234-5678-1234-567812345678")

# Base de datos en memoria
# Estructura:
# users_by_name[name] = {"uid": str, "password_hash": str}
# users_by_uid[uid]   = {"name": str, "password_hash": str}
users_by_name = {}
users_by_uid = {}

# Función para hashear la contraseña usando SHA-256
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

# Genera un token único para un usuario dado su UID
def generate_token(user_uid: str) -> str:
    return str(uuid.uuid5(SECRET_UUID, user_uid))

# Rutas del microservicio de usuario, con el metodo Put
@app.route("/user", methods=["PUT"]) # si se manda petiion put a /user se ejecuta
async def create_user():
    data = await request.get_json()
    if not data or "name" not in data or "password" not in data:
        return jsonify({"error": "Faltan datos (name y password requeridos)"}), 400

    name = data["name"]
    password = data["password"]

    if name in users_by_name:
        return jsonify({"error": "El usuario ya existe"}), 409

    # si el usuario no existe, lo creamos
    user_uid = str(uuid.uuid4())
    pass_hash = hash_password(password)

    user_entry = {"uid": user_uid, "name": name, "password_hash": pass_hash}
    users_by_name[name] = user_entry
    users_by_uid[user_uid] = user_entry

    token = generate_token(user_uid)
    return jsonify({"uid": user_uid, "token": token}), 201


@app.route("/user", methods=["POST"])
async def login():
    data = await request.get_json()
    if not data or "name" not in data or "password" not in data:
        return jsonify({"error": "Faltan datos (name y password requeridos)"}), 400

    name = data["name"]
    password = data["password"]

    user = users_by_name.get(name)
    if not user or user["password_hash"] != hash_password(password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    token = generate_token(user["uid"])
    return jsonify({"uid": user["uid"], "token": token}), 200


@app.route("/user", methods=["PATCH"])
async def modify_user():
    # Se pide el token de autorización en la cabecera Authorization Bearer
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Cabecera Authorization Bearer requerida"}), 401

    parts = auth_header.split()
    if len(parts) != 2 or parts[0] != "Bearer":
        return jsonify({"error": "Cabecera Authorization con formato incorrecto"}), 401
    token_recibido = parts[1]

    data = await request.get_json()
    if not data or "password" not in data:
        return jsonify({"error": "Falta la nueva password"}), 400

    # Buscamos qué usuario corresponde a ese token
    authenticated_user = None
    for uid, u in users_by_uid.items():
        if generate_token(uid) == token_recibido:
            authenticated_user = u
            break

    if not authenticated_user:
        return jsonify({"error": "Token no válido o expirado"}), 401

    authenticated_user["password_hash"] = hash_password(data["password"])
    return jsonify({"message": "Contraseña actualizada correctamente"}), 200

# Arranque del servidor Quart en el puerto 5050, escuchando en todas las interfaces
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050) # lo pone en la presentación, ("5050" para microservicio de usuario, "5051" para microservicio)
    # host 0.0.0.0 esccucha a todas las interfaces, localhost solo las del docker