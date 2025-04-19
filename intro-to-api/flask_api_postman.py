from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample in-memory database
users = {
    1: {"id": 1, "name": "John Doe", "email": "john@example.com"}
}
next_id = 2

# GET /users - List all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# POST /users - Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    global next_id
    data = request.json
    data['id'] = next_id
    users[next_id] = data
    next_id += 1
    return jsonify(data), 201

# PUT /users/<id> - Update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id in users:
        data = request.json
        users[user_id].update(data)
        return jsonify(users[user_id])
    return jsonify({'error': 'User not found'}), 404

# DELETE /users/<id> - Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return '', 204
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
