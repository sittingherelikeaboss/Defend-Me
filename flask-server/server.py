from flask import Flask, request, jsonify, render_template, send_from_directory
import sqlite3
import os
import bcrypt
import serverUtils
import datetime

app = Flask(__name__)

# Serve React app
@app.route("/")
def serve():
    return send_from_directory('.', 'index.html')

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
                        'data': {
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

'''
Validates an employee email and password (credentials).

Returns true when employee exists and password matches.
'''
@app.route("/employee/validate/<email>", methods=['GET'])
def validateEmployeeCredentials(email):
    req_args = request.view_args
    password = request.args.get('password')
    print('req_args: ', req_args)

    db_file = 'database.db'
    os.chdir('../sql-database/')
    db_connection = sqlite3.connect(os.path.join(os.path.abspath(os.curdir), db_file))

    cur = db_connection.cursor()
    cur.execute("SELECT password FROM employee WHERE email = '%s'" % email)
    db_connection.commit()
    data = cur.fetchone()
    
    # Compare hashed password
    passwordMatches = False
    bytes = password.encode('utf-8') 
    hashedDbPassword = data[0]
    if (bcrypt.checkpw(bytes, hashedDbPassword)):
        passwordMatches = True
    
    if (data and len(data) > 0 and passwordMatches):
        response = jsonify({
                        'passwordMatches': True
                    })
    else:
        response = jsonify({ # TODO: Propagate these error messages
                        'passwordMatches': False,
                        'message': 'Invalid password or no password found with provided email address.'
                    })
    return response

'''
Returns a list of employees as an array of objects from SQLite
'''
@app.route("/employee", methods=['GET'])
def listAllEmployees():
    req_args = request.view_args
    print('req_args: ', req_args)

    db_file = 'database.db'
    os.chdir('../sql-database/')
    db_connection = sqlite3.connect(os.path.join(os.path.abspath(os.curdir), db_file))

    cur = db_connection.cursor()
    cur.execute("SELECT employee_id, name, email, created_date, updated_date FROM employee")
    data = cur.fetchall()
    employees = []
    for i in data:
        employees.append({
            'employee_id': i[0],
            'name': i[1],
            'email': i[2],
            'created_date': i[3],
            'updated_date': i[4]
        })

    if (data and len(data) > 0):
        response = jsonify({ # TODO: I wonder how to improve these to have an object definition interface
                        'object': 'list',
                        'url': '/employee',
                        'data': employees,
                    })
    else:
        response = jsonify({
                        'status': 404,
                        'message': 'No employee found with provided email address.'
                    })
        
    db_connection.close()
    return response

'''
Creates an Employee in the database.
'''
@app.route("/employee", methods=['POST'])
def createEmployee():
    db_file = 'database.db'
    os.chdir('../sql-database/')
    db_connection = sqlite3.connect(os.path.join(os.path.abspath(os.curdir), db_file))

    cur = db_connection.cursor()
    parsedBody = request.json
    name = parsedBody["name"]
    email = parsedBody["email"]
    password = parsedBody["password"]
    
    cur.execute("INSERT INTO employee (name, email, password, deactivated, created_date) VALUES (?, ?, ?, ?, ?)",
                    (name, email.lower(), serverUtils.encrpytPassword(password), False, datetime.datetime.now().isoformat())
                    )
    
    db_connection.commit()
    
    cur.execute("SELECT employee_id, name, email, created_date FROM employee WHERE email = '%s'" % email)
    data = cur.fetchone()    
    
    db_connection.close()

    if (data and len(data) > 0):
        response = jsonify({ # TODO: I wonder how to improve these to have an object definition interface
                        "employee_id": data[0],
                        "name": data[1],
                        "email": data[2],
                        "created_date": data[3]
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
                        'object': 'list',
                        'url': '/device',
                        'data': devices
                    })
    else:
        response = jsonify({
                        'status': 404,
                        'message': 'No scans found with provided query parameters.'
                    })
    return response

@app.route("/scans", methods=['GET'])
def listAllScans():
    db_file = 'database.db'
    os.chdir('../sql-database/')
    db_connection = sqlite3.connect(os.path.join(os.path.abspath(os.curdir), db_file))

    sql = "SELECT scan_id, os_version, app_version, secure, threats, device_id, created_date FROM scan"
    secure = request.args.get('secure')
    if (len(secure) > 0):
        sql = sql + " WHERE secure = %s" % secure

    cur = db_connection.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    scans = []
    for i in data:
        scans.append({
            'scan_id': i[0],
            'os_version': i[1],
            'app_version': i[2],
            'secure': i[3],
            'threats': i[4],
            'device_id': i[5],
            'created_date': i[6]
        })
    if (data and len(data) > 0):
        response = jsonify({ # TODO: I wonder how to improve these to have an object definition interface
                                                'object': 'list',
                        'url': '/scans',
                        'data': scans
                    })
    else:
        response = jsonify({
                        'message': 'No scans found with provided query parameters.'
                    })
    return response

if __name__ == "__main__":
    app.run(debug=True)
    app.run(ssl_context='adhoc') # HTTPS locally