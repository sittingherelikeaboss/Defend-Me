import sqlite3
import random
import string
import uuid
import bcrypt

# Library to generate fake names and email addresses!
from faker import Faker
fake = Faker()

def generateEncryptedPassword():
    randomString = string.ascii_lowercase + string.digits
    password = ''.join(random.sample(randomString, 20))
    
    # converting password to array of bytes 
    bytes = password.encode('utf-8') 
    
    # generating the salt 
    salt = bcrypt.gensalt() 
    
    # Hashing the password 
    hash = bcrypt.hashpw(bytes, salt)
    
    return hash

def initialiseDatabase():
    schema_file = 'schema.sql'
    with open(schema_file, 'r') as sql_file:
        sql_script = sql_file.read()

    db_file = 'database.db'
    db_connection = sqlite3.connect(db_file)
    cur = db_connection.cursor()
    cur.executescript(sql_script)

    print('\nInitialising database with schema from %s!' % (schema_file))

    # We want to seed Faker for unit testing so it is always generates the same data set.
    # Seed 100 employees
    for i in range(100):
        Faker.seed(i)
        fakeName = fake.name()
        cur.execute("INSERT INTO employee (name, email, deactivated) VALUES (?, ?, ?)",
                    (fakeName, (fakeName.replace(" ", ".") + "@helloworld.io").lower(), False)
                    )
        
    # Seed user admin roles -- NOT ALL EMPLOYEES!
    # Make the first 5 employees as admin for simplicity... although not a thing in reality lol
    for i in range(5):
        Faker.seed(i)
        fakeName = fake.name()
        cur.execute("INSERT INTO administrator (email, password) VALUES (?, ?)",
                    ((fakeName.replace(" ", ".") + "@helloworld.io").lower(), generateEncryptedPassword())
                    )
        
    # Seed employee to admin relationship table
    # We know from previous INSERT that first 5 employees are administrators
    for i in range(1,6):
        cur.execute("INSERT INTO admin_access (admin_id, employee_id) VALUES (?, ?)",
                    (i, i)
                    )

    # Seed 1,000 devices
    devices = ["Apple iPhone 15 Pro", "Apple iPhone 15", "Apple iPad Pro", "Apple iPad Mini", "Google Pixel 8 Pro", "Google Pixel 8"]
    for i in range(1000):
        random.seed(i)
        cur.execute("INSERT INTO device (model, unique_device_identifier, employee_id) VALUES (?, ?, ?)",
                    (random.choice(devices), str(uuid.uuid4()), random.choice(range(100)))
        )

    # Seed 10,000 scans
    threats = [None, 'Cryptomining malware', 'Ransomware', 'Bank trojans', 'Remote access tools']
    androidVersion = ['Android 11', 'Android 12']
    iOSVersion = ['iOS 16', 'iOS 17']
    appVersion = ['1.0.0', '1.1.0', '1.1.1']
    for i in range(10000):
        random.seed(i)
        threatType = random.choices(threats, weights=(98.5,0.5,0.25,0.25,0.5))
        deviceId = random.choice(range(1, 1000))

        cur.execute("SELECT model FROM device WHERE device_id = ?", (deviceId,))
        device = cur.fetchall()[0][0] # Weird list and tuple things returned so we do this

        osVersion = device.find('Apple')
        if osVersion == -1:
            osVersion = random.choice(androidVersion)
        else:
            osVersion = random.choice(iOSVersion)
        cur.execute("INSERT INTO scan (os_version, app_version, secure, threats, device_id) VALUES (?, ?, ?, ?, ?)",
                    (osVersion, random.choice(appVersion), threatType[0] == None, threatType[0], deviceId)
                    )

    print('\nStarting table creation and insertion validation...')

    # Validate employees inserted into database
    print("\nSELECT COUNT(*) FROM employee")
    cur.execute("SELECT COUNT(*) FROM employee")
    print(cur.fetchone()[0]) # We do this weird thing cause we get back a tuple
    
    # Validate administrator inserted into database
    print("\nSELECT COUNT(*) FROM administrator")
    cur.execute("SELECT COUNT(*) FROM administrator")
    print(cur.fetchone()[0]) # We do this weird thing cause we get back a tuple
    
    # Validate admin_access inserted into database
    print("\nSELECT COUNT(*) FROM admin_access")
    cur.execute("SELECT COUNT(*) FROM admin_access")
    print(cur.fetchone()[0]) # We do this weird thing cause we get back a tuple

    # Validate device inserted into database
    print("\nSELECT COUNT(*) FROM device")
    cur.execute("SELECT COUNT(*) FROM device")
    print(cur.fetchone()[0]) # We do this weird thing cause we get back a tuple

    # Validate scans inserted into database
    print("\nSELECT COUNT(*) FROM scan")
    cur.execute("SELECT COUNT(*) FROM scan")
    print(cur.fetchone()[0]) # We do this weird thing cause we get back a tuple

    print('\nFinished table creation and insertion validation!')

    db_connection.commit()
    db_connection.close()

    print('\nDatabase initialised!')
    
initialiseDatabase()