from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/students_db'
mongo = PyMongo(app)


@app.route('/students', methods=['POST'])
def create_student():
    student = mongo.db.students
    name = request.json['name']
    age = request.json['age']
    email = request.json['email']
    new_student = {'name': name, 'age': age, 'email': email}
    student_id = student.insert_one(new_student).inserted_id
    result = {'name': new_student['name'], 'age': new_student['age'], 'email': new_student['email']}
    return jsonify({'result': result})


@app.route('/students', methods=['GET'])
def get_students():
    student = mongo.db.students
    result = []
    for field in student.find():
        result.append({'name': field['name'], 'age': field['age'], 'email': field['email']})
    return jsonify({'result': result})


@app.route('/students/<name>', methods=['GET'])
def get_student(name):
    student = mongo.db.students
    result = student.find_one({'name': name})
    if result:
        output = {'name': result['name'], 'age': result['age'], 'email': result['email']}
    else:
        output = 'No results found'
    return jsonify({'result': output})


@app.route('/students/<name>', methods=['PUT'])
def update_student(name):
    student = mongo.db.students
    age = request.json['age']
    email = request.json['email']
    student.find_one_and_update({'name': name}, {'$set': {'age': age, 'email': email}})
    result = {'name': name, 'age': age, 'email': email}
    return jsonify({'result': result})


@app.route('/students/<name>', methods=['DELETE'])
def delete_student(name):
    student = mongo.db.students
    student.delete_one({'name': name})
    result = {'message': 'Student deleted successfully'}
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)
