from flask import Flask, request, jsonify
import threading
import time
import requests

# ---------------------------
# 1. Flask API Server
# ---------------------------
app = Flask(__name__)
users = {
    1: {"name": "John Doe", "email": "john@example.com"}
}
next_id = 2

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    global next_id
    data = request.json
    users[next_id] = data
    users[next_id]['id'] = next_id
    next_id += 1
    return jsonify(users[next_id - 1]), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    if user_id in users:
        users[user_id].update(data)
        return jsonify(users[user_id])
    return jsonify({"error": "User not found"}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return '', 204
    return jsonify({"error": "User not found"}), 404

# ---------------------------
# 2. Start Flask in Background
# ---------------------------
def run_server():
    app.run(port=5000)

threading.Thread(target=run_server, daemon=True).start()
time.sleep(1)  # Give server time to start

# ---------------------------
# 3. Requests Client Code
# ---------------------------
print("\n=== GET Request ===")
res = requests.get('http://localhost:5000/users')
print(res.json())

print("\n=== POST Request ===")
new_user = {"name": "Jane Smith", "email": "jane@example.com"}
res = requests.post('http://localhost:5000/users', json=new_user)
print(res.json())

print("\n=== PUT Request ===")
updated_user = {"name": "Jane Johnson"}
res = requests.put('http://localhost:5000/users/2', json=updated_user)
print(res.json())

print("\n=== DELETE Request ===")
res = requests.delete('http://localhost:5000/users/2')
print("Deleted" if res.status_code == 204 else "Failed to delete")
