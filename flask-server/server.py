from flask import Flask, request, jsonify, render_template, send_from_directory
import sqlite3
import os

app = Flask(__name__)

# Members API route
@app.route("/members")
def members():
    return {"members": ["Member 1", "Member 2", "Member 3"]}

# Serve React app
@app.route("/")
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html") 

@app.route("/employee/<email>", methods=['GET'])
def getEmployeeByEmail(email):
    req_args = request.view_args
    print('req_args: ', req_args)

    db_file = 'database.db'
    os.chdir('../sql-database/')
    db_connection = sqlite3.connect(os.path.join(os.path.abspath(os.curdir), db_file))

    cur = db_connection.cursor()
    cur.execute("SELECT employee_id, name, email, created_date, updated_date FROM employee WHERE email = '%s'" % email)
    data = cur.fetchone()
    if (data and len(data) > 0):
        response = jsonify({ # TODO: I wonder how to improve these to have an object definition interface
                        'status': 200,
                        'employee': {
                            'employee_id': data[0],
                            'name': data[1],
                            'email': data[2],
                            'created_date': data[3],
                            'updated_date': data[4]
                        }
                    })
    else:
        response = jsonify({
                        'status': 404,
                        'message': 'No employee found with provided email address.'
                    })
    return response

@app.route("/employee", methods=['GET'])
def listAllEmployees():
    req_args = request.view_args
    print('req_args: ', req_args)

    db_file = 'database.db'
    os.chdir('../sql-database/')
    db_connection = sqlite3.connect(os.path.join(os.path.abspath(os.curdir), db_file))

    cur = db_connection.cursor()
    cur.execute("SELECT employee_id, name, email FROM employee")
    data = cur.fetchall()
    employees = []
    for i in data:
        employees.append({
            'employee_id': i[0],
            'name': i[1],
            'email': i[2]
        })

    if (data and len(data) > 0):
        response = jsonify({ # TODO: I wonder how to improve these to have an object definition interface
                        'status': 200,
                        'employee': employees
                    })
    else:
        response = jsonify({
                        'status': 404,
                        'message': 'No employee found with provided email address.'
                    })
    return response

@app.route("/device", methods=['GET'])
def listAllDevices():
    req_args = request.view_args
    print('req_args: ', req_args)

    db_file = 'database.db'
    os.chdir('../sql-database/')
    db_connection = sqlite3.connect(os.path.join(os.path.abspath(os.curdir), db_file))

    cur = db_connection.cursor()
    cur.execute("SELECT device_id, model, unique_device_identifier, employee_id FROM device")
    data = cur.fetchall()
    devices = []
    for i in data:
        devices.append({
            'device_id': i[0],
            'model': i[1],
            'unique_device_identifier': i[2],
            'employee_id': i[3]
        })
    if (data and len(data) > 0):
        response = jsonify({ # TODO: I wonder how to improve these to have an object definition interface
                        'status': 200,
                        'scans': devices
                    })
    else:
        response = jsonify({
                        'status': 404,
                        'message': 'No scans found with provided query parameters.'
                    })
    return response

@app.route("/scans", methods=['GET'])
def listAllScans():
    req_args = request.view_args
    print('req_args: ', req_args)

    db_file = 'database.db'
    os.chdir('../sql-database/')
    db_connection = sqlite3.connect(os.path.join(os.path.abspath(os.curdir), db_file))

    cur = db_connection.cursor()
    cur.execute("SELECT scan_id, os_version, app_version, threats, device_id FROM scan")
    data = cur.fetchall()
    scans = []
    for i in data:
        scans.append({
            'scan_id': i[0],
            'os_version': i[1],
            'app_version': i[2],
            'threats': i[3],
            'device_id': i[4]
        })
    if (data and len(data) > 0):
        response = jsonify({ # TODO: I wonder how to improve these to have an object definition interface
                        'status': 200,
                        'scans': scans
                    })
    else:
        response = jsonify({
                        'status': 404,
                        'message': 'No scans found with provided query parameters.'
                    })
    return response

if __name__ == "__main__":
    app.run(debug=True)