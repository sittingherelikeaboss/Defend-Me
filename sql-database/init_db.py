import sqlite3
import random
import string
import uuid

# Library to generate fake names and email addresses!
from faker import Faker
fake = Faker()

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
    randomString = string.ascii_lowercase +string.digits
    fakeName = fake.name()
    cur.execute("INSERT INTO employee (name, email, password, deactivated) VALUES (?, ?, ?, ?)",
                (fakeName, (fakeName.replace(" ", ".") + "@helloworld.io").lower(), ''.join(random.sample(randomString, 20)), False)
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