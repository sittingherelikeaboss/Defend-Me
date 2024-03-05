import logging
from flask import Flask, request, jsonify, render_template, send_from_directory, make_response
from flask_cors import CORS, cross_origin
from functools import wraps
import sqlite3
import os
import bcrypt
from datetime import timedelta
from flask_login import LoginManager
import passwordUtils
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager, \
                                   set_access_cookies, create_refresh_token


app = Flask(__name__)
login = LoginManager(app)
app.config["JWT_SECRET_KEY"] = "please-remember-to-change-me" #TODO: Change this!!!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_COOKIE_SECURE"] = True # Send JWT over HTTPS only
jwt = JWTManager(app)

# Fix Cross Origin Resource Sharing issues with Python Flask
CORS(app)

# Serve React app
@app.route("/")
def serve():
    return send_from_directory('.', 'index.html')

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html") 

@app.errorhandler(401)
def custom_401(e):
    return jsonify({"message: Token has expired"}), 401

@app.route('/token', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    access_token = create_access_token(identity=email)
    response = jsonify({"message": "login successful"})
    set_access_cookies(response, access_token)
    # add this access_token to the session table in the db
    return response, 200

'''
Validates an employee email and password (credentials).

Returns true when employee exists and password matches.
'''
@app.route("/login", methods=['POST', 'OPTIONS'])                                                                                                                                                                                                                                                                                                                                                                                                           
def login():
    print("server::login()")
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "POST": # The actual request following the preflight
        parsedBody = request.json
        
        db_file = 'database.db'
        oldpwd = os.getcwd()
        os.chdir("..")
        os.chdir(os.path.join(os.path.abspath(os.curdir), 'sql-database'))
        print("Current directory now:" , os.getcwd()) 
        db_connection = sqlite3.connect(os.path.join(os.path.abspath(os.curdir), db_file))
        os.chdir(oldpwd)

        cur = db_connection.cursor()
        cur.execute("SELECT password FROM administrator WHERE email = '%s'" % parsedBody['email'])
        db_connection.commit()
        data = cur.fetchone()
        db_connection.close()
        
        # Compare hashed password
        passwordMatches = False
        bytes = parsedBody['password'].encode('utf-8') 
        hashedDbPassword = data[0]
        
        if (bcrypt.checkpw(bytes, hashedDbPassword)):
            passwordMatches = True
        
        if (data and len(data) > 0 and passwordMatches):
            email = request.json.get("email", None)
            access_token = create_access_token(identity=email, fresh=True)
            response = jsonify(access_token=access_token)
            return _corsify_actual_response(response), 200
        else:
            response = jsonify({ # TODO: Propagate these error messages
                            'message': 'Invalid password or no password found with provided email address.'
                        })
            return _corsify_actual_response(response), 400
    else:
        raise RuntimeError("We don't know how to handle this type of method sorry...")

@app.route("/logout", methods=["POST"])
def logout():
    # Delete this token from the session table in the db
    response = jsonify({"message": "logout successful"})
    unset_jwt_cookies(response)
    return response, 200

# If we are refreshing a token here we have not verified the users password in
# a while, so mark the newly created access token as not fresh
@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)

@app.route("/protected", methods=["GET"])
@jwt_required()
def testProtected():
    return jsonify("message: You are viewing a protected route"), 200








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
Returns a list of employees as an array of objects from SQLite
'''
@app.route("/employee", methods=['GET'])
def listAllEmployees():
    req_args = request.view_args
    print('req_args: ', req_args)

    db_file = 'database.db'
    oldpwd = os.getcwd()
    os.chdir("..")
    os.chdir(os.path.join(os.path.abspath(os.curdir), 'sql-database'))
    print("Current directory now:" , os.getcwd()) 
    db_connection = sqlite3.connect(os.path.join(os.path.abspath(os.curdir), db_file))
    os.chdir(oldpwd)

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
                        'count': len(data)
                    })
    else:
        response = jsonify({
                        'status': 404,
                        'message': 'No employee found with provided email address.'
                    })
        
    db_connection.close()
    return response

'''
Creates an Organization Administrator in the database.
'''
@app.route("/administrator", methods=['POST'])
def createAdministrator():
    db_file = 'database.db'
    oldpwd = os.getcwd()
    os.chdir("..")
    os.chdir(os.path.join(os.path.abspath(os.curdir), 'sql-database'))
    print("Current directory now:" , os.getcwd()) 
    db_connection = sqlite3.connect(os.path.join(os.path.abspath(os.curdir), db_file))
    os.chdir(oldpwd)

    cur = db_connection.cursor()
    parsedBody = request.json
    email = parsedBody["email"]
    password = parsedBody["password"]
    
    try:
        cur.execute("INSERT INTO administrator (email, password) VALUES (?, ?)",
                        (email.lower(), passwordUtils.encrpytPassword(password))
                        )
    except:
        return jsonify({
            'message': 'Administrator already exists.'}), 409
    
    db_connection.commit()
    
    # Relationship tables
    try:
        cur.execute("SELECT a.administrator_id, e.employee_id from administrator a inner join employee e on e.employee_id = a.administrator_id where a.email = '%s'" % email)
        data = cur.fetchone()
        admin_id = data[0]
        employee_id = data[1]
    except:
        return jsonify({
            'message': 'Employee email does not exist.'}), 400
    
    cur.execute("INSERT INTO admin_access (admin_id, employee_id) VALUES (?, ?)",
                    (admin_id, employee_id)
                    )
    
    db_connection.commit()
    
    cur.execute("SELECT administrator_id, email, created_date from administrator where email = '%s'" % email)
    data = cur.fetchone()
    administrator_id = data[0]
    email = data[1]
    created_date = data[2]
    
    db_connection.close()

    if (data and len(data) > 0):
        return jsonify({ # TODO: I wonder how to improve these to have an object definition interface
                        "administrator_id": administrator_id,
                        "email": email,
                        "created_date": created_date
                    }), 200
    else:
        return jsonify({
                        'message': 'Failed to create administrator.'
                    }), 422

@app.route("/device", methods=['GET'])
def listAllDevices():
    req_args = request.view_args
    print('req_args: ', req_args)

    db_file = 'database.db'
    oldpwd = os.getcwd()
    os.chdir("..")
    os.chdir(os.path.join(os.path.abspath(os.curdir), 'sql-database'))
    print("Current directory now:" , os.getcwd()) 
    db_connection = sqlite3.connect(os.path.join(os.path.abspath(os.curdir), db_file))
    os.chdir(oldpwd)

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

@app.route("/scan", methods=['GET'])
@cross_origin
def listAllScans():
    print("server::listAllScans()")
    db_file = 'database.db'
    oldpwd = os.getcwd()
    print("Current directory now:" , oldpwd) 
    os.chdir("..")
    os.chdir(os.path.join(os.path.abspath(os.curdir), 'sql-database'))
    print("Current directory now:" , os.getcwd()) 
    db_connection = sqlite3.connect(os.path.join(os.path.abspath(os.curdir), db_file))
    os.chdir(oldpwd)

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

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))