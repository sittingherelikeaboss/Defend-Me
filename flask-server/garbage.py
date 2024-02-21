import os

os.chdir('../sql-database/')
print(os.path.join(os.path.abspath(os.curdir), 'db.sql'))