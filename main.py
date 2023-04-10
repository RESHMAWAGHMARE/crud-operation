from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'
mongo = PyMongo(app)


# Create operation
@app.route('/users', methods=['POST'])
def create_user():
    user = mongo.db.users
    name = request.json['name']
    email = request.json['email']
    new_user = {'name': name, 'email': email}
    user_id = user.insert_one(new_user).inserted_id
    result = {'name': new_user['name'], 'email': new_user['email']}
    return jsonify({'result': result})


# Read operation
@app.route('/users', methods=['GET'])
def get_users():
    user = mongo.db.users
    result = []
    for field in user.find():
        result.append({'name': field['name'], 'email': field['email']})
    return jsonify({'result': result})


# Update operation
@app.route('/users/<name>', methods=['PUT'])
def update_user(name):
    user = mongo.db.users
    email = request.json['email']
    user.find_one_and_update({'name': name}, {'$set': {'email': email}})
    result = {'name': name, 'email': email}
    return jsonify({'result': result})


# Delete operation
@app.route('/users/<name>', methods=['DELETE'])
def delete_user(name):
    user = mongo.db.users
    user.delete_one({'name': name})
    result = {'message': 'User deleted successfully'}
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)
