# Defend Me

## Table of Contents

- [Description](#description)
- [Functionality](#functionality)


## Description

This is a take-home project for a technical interview for a company.

This application is written in Python for the backend and React for the frontend.

## Functionality

A smartphone application that scans a fictional company's employee devices for known and unknown malware.

## Instructions

### Local

#### Windows (Bash)

1. Ensure you have Node.js and npm installed in your machine. Check by running the following commands.

```
npm -v
node -v
```

If you do not have Node.js, install from [here](https://nodejs.org/en/download).

2. Once you have Node.js and npm installed, go ahead and install the dependencies for **Defend Me**.

```
npm install
```

3. Run the commands below to start the backend server.

```
cd /flask-server
python3 server.py
```

4. Run the commands below to start the frontend in another terminal.

```
cd client
npm start
```

5. Ensure you have Python installed.

```
python --version
```

or

```
python3 --version
```

If you do not have Python, go ahead and install it from [here](https://www.python.org/).

6. If you have Python3 installed, run the commands below to initialise the database.

```
cd sql-database
```

```
python init_db.sql

or

python3 init_db.sql
```
