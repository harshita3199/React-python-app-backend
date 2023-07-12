from flask import Flask, jsonify, request
import mysql.connector  # If you're using MySQL as the database
from flask_cors import CORS
# Create the Flask application
app = Flask(__name__)
CORS(app)

# MySQL configuration
db_config = {
    'host': 'database-1.cpk0oc0tylv5.us-east-1.rds.amazonaws.com',       # Replace with your MySQL host
    'user': 'adminusr',   # Replace with your MySQL username
    'password': 'WelcomeCloud9',  # Replace with your MySQL password
    'database': 'mydatabase'  # Replace with your MySQL database name
}

# Create a database connection
db_conn = mysql.connector.connect(**db_config)

# Create a cursor for executing queries
cursor = db_conn.cursor()

@app.route('/api/users', methods=['GET'])
def get_users():
    query = "SELECT * FROM mytable"
    cursor.execute(query)
    users = cursor.fetchall()

    user_list = []
    for user in users:
        user_dict = {
            'emp_id': user[0],
            'emp_name': user[1],
            'emp_age': user[2]
        }
        user_list.append(user_dict)

    return jsonify(user_list)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    emp_id = data['emp_id']
    emp_name = data['emp_name']
    emp_age = data['emp_age']

    query = "INSERT INTO mytable (emp_id, emp_name, emp_age) VALUES (%s, %s, %s)"
    cursor.execute(query, (emp_id, emp_name, emp_age))
    db_conn.commit()

    return jsonify({'message': 'User created successfully'})

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    emp_id = data['emp_id']
    emp_name = data['emp_name']
    emp_age = data['emp_age']

    query = "UPDATE mytable SET emp_id = %s, emp_name = %s, emp_age = %s WHERE emp_id = %s"
    cursor.execute(query, (emp_id, emp_name, emp_age, user_id))
    db_conn.commit()

    return jsonify({'message': 'User updated successfully'})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    query = "DELETE FROM mytable WHERE emp_id = %s"
    cursor.execute(query, (user_id,))
    db_conn.commit()

    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)