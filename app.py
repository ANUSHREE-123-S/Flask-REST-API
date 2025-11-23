from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data store (acts as a temporary database)
users = {}

# Home Route
@app.route("/")
def home():
    return {"message": "User Management API is running!"}

# GET all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

# GET single user by ID
@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return {"error": "User not found"}, 404

# POST - Create new user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json

    if "id" not in data or "name" not in data:
        return {"error": "id and name are required"}, 400

    user_id = data["id"]
    if user_id in users:
        return {"error": "User already exists"}, 400

    users[user_id] = {
        "id": user_id,
        "name": data["name"],
        "email": data.get("email", "")
    }

    return {"message": "User created", "user": users[user_id]}, 201

# PUT - Update user
@app.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    if user_id not in users:
        return {"error": "User not found"}, 404

    data = request.json
    users[user_id]["name"] = data.get("name", users[user_id]["name"])
    users[user_id]["email"] = data.get("email", users[user_id]["email"])

    return {"message": "User updated", "user": users[user_id]}

# DELETE - Remove user
@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in users:
        return {"error": "User not found"}, 404

    del users[user_id]
    return {"message": "User deleted"}

if __name__ == "__main__":
    app.run(debug=True)
