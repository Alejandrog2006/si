import os
import uuid
from quart import Quart, request, jsonify

app = Quart(__name__)

@app.route('/user', methods=['GET'])
async def list_docs():
    data = await request.get_json()
    uid = data.get('uid')
    pass

@app.route('/user', methods=['PUT'])
async def modify_docs():
    data = await request.get_json()
    uid = data.get('uid')
    filename = data.get('filename')
    pass

@app.route('/user', methods=['GET'])
async def restore_docs():
    data = await request.get_json()
    uid = data.get('uid')
    filename = data.get('filename')
    pass

@app.route('/user', methods=['DELETE'])
async def delete_docs():
    data = await request.get_json()
    uid = data.get('uid')
    filename = data.get('filename')
    pass

@app.route('/user', methods=['PATCH'])
async def visibility_docs():
    data = await request.get_json()
    uid = data.get('uid')
    filename = data.get('filename')
    public = data.get('public')
    pass

if __name__ == '__main__':
    app.run(host='localhost', port=5051)
