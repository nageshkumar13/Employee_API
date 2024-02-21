# Import the json module for handling JSON data
import json  
# Import necessary modules from Flask
from flask import Flask, jsonify, request  
# Create a Flask application instance with the name of the script's module
app = Flask(__name__)  

# Define a list containing dictionaries representing employee data
employees = [ 
    {'id': 1, 'name': 'Ashley'},
    {'id': 2, 'name': 'Kate'},
    {'id': 3, 'name': 'Joe'}
]

# Initialize a variable to track the ID of the next employee
nextEmployeeId = 4  

# Define a route for handling GET requests to '/employees'
@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)  # Return a JSON response containing the list of employees

# Define a route for handling GET requests to '/employees/<id>'
@app.route('/employees/<int:id>', methods=['GET'])
def get_employee_by_id(id: int):
    employee = get_employee(id)  # Retrieve employee data based on the provided ID
    if employee is None:
        # Return a JSON response with an error message and 404 status code if employee is not found.
        return jsonify({'error': 'Employee does not exist'}), 404  
    # Return a JSON response containing the employee data
    return jsonify(employee)  

# Define a function to retrieve employee data based on ID
def get_employee(id):
    # Return the first employee with the provided ID, or None if not found.
    return next((e for e in employees if e['id'] == id), None)  

# Define a function to check if employee data is valid
def employee_is_valid(employee):
    for key in employee.keys():
        if key != 'name':
            return False
    return True

# Define a route for handling POST requests to '/employees'
@app.route('/employees', methods=['POST'])
def create_employee():
    # Access the global variable nextEmployeeId
    global nextEmployeeId 
    # Parse the JSON data from the request body
    employee = json.loads(request.data)  
    if not employee_is_valid(employee):
        # Return a JSON response with an error message and 400 status code if employee data is invalid
        return jsonify({'error': 'Invalid employee properties.'}), 400 
    # Assign the next available ID to the new employee
    employee['id'] = nextEmployeeId 
    # Increment the next available ID 
    nextEmployeeId += 1  
    # Add the new employee to the list
    employees.append(employee) 

    return '', 201, {'location': f'/employees/{employee["id"]}'}

# Define a route for handling PUT requests to '/employees/<id>'
@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id: int):
    # Retrieve the employee to update based on the provided ID
    employee = get_employee(id)  
    if employee is None:
        # Return a JSON response with an error message and 404 status code if employee is not found.
        return jsonify({'error': 'Employee does not exist.'}), 404  
    
    # Parse the JSON data from the request body
    updated_employee = json.loads(request.data)  
    if not employee_is_valid(updated_employee):
         # Return a JSON response with an error message and 400 status code if updated employee data is invalid
        return jsonify({'error': 'Invalid employee properties.'}), 400 

    employee.update(updated_employee)  # Update the employee data with the provided data

    return jsonify(employee)  # Return a JSON response containing the updated employee data

# Define a route for handling DELETE requests to '/employees/<id>'
@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id: int):
    global employees  # Access the global variable employees
    employee = get_employee(id)  # Retrieve the employee to delete based on the provided ID
    if employee is None:
        return jsonify({'error': 'Employee does not exist.'}), 404  # Return a JSON response with an error message and 404 status code if employee is not found

    employees = [e for e in employees if e['id'] != id]  # Remove the employee from the list
    return jsonify(employee), 200  # Return a JSON response containing the deleted employee data and 200 status code


# Start the Flask application on port 5000 if the script is executed directly
if __name__ == '__main__':
    app.run(port=5000)
