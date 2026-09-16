import hashlib
import uuid
from quart import Quart, request, jsonify

app = Quart(__name__)

user_data = {}  # Diccionario para almacenar los datos de los usuarios

def generate_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

secret_uuid = uuid.uuid4() # Este se habrá generado una única vez y guardado en el servidor


@app.route('/user', methods=['PUT'])

async def create_user():
    data = await request.get_json()
    name = data.get('name')
    password = data.get('password')
    if not name or not password:
        return jsonify({'error': 'Name and password are required'}), 400

    if name in user_data:
        return jsonify({'error': 'User already exists'}), 409
    
    uid_del_usuario_como_string = str(uuid.uuid4()) # Este se habrá generado al hacer create_user 
    token = uuid.uuid5(secret_uuid, uid_del_usuario_como_string)

    user_data[name] = {'uid': uid_del_usuario_como_string, 'password_hash': generate_password(password),}
    return jsonify({
        'message': 'User created successfully',
        'uid': str(uid_del_usuario_como_string),
        'token': str(token),
    }), 201

@app.route('/user', methods=['POST'])

async def login():
    data = await request.get_json()
    name = data.get('name')
    password = data.get('password')
    if not name or not password:
        return jsonify({'error': 'Name and password are required'}), 400

@app.route('/user', methods=['PATCH'])

async def modify_user():
    data = await request.get_json()
    password = data.get('password')
    if not password:
        return jsonify({'error': 'Password is required'}), 400

if __name__ == '__main__':
    app.run(host='localhost', port=5050)
