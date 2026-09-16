import hashlib
import uuid
from quart import Quart, request, jsonify

app = Quart(__name__)

@app.route('/user', methods=['PUT'])



@app.route('/user', methods=['POST'])



@app.route('/user', methods=['PATCH'])



if __name__ == '__main__':
    app.run(host='localhost', port=5050)
