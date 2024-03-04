# ⚔️ Defend Me

## 📚 Table of Contents

1. [Description](#description)
2. [Functionality](#functionality)
    - [Security Considerations](#security-considerations)
    - [Login Screen](#login-screen)
    - [Enterprise Dashboard](#enterprise-dashboard)
3. [Developer Instructions](#developer-instructions)
    - [Local](#local)
        - [Windows](#windows-bash)
        - [Troubleshooting](#troubleshooting)
            - [Cross-Origin Request Blocked and CORS issues](#cross-origin-request-blocked-and-cors-issues)
4. [Credits](#credits)

## 📖 Description

This is a take-home project for a technical interview for a company.

This application is written in Python for the Flask backend and React.js for the frontend.

## Functionality

A smartphone application that scans a fictional company's employee devices for known and unknown malware.

### Security Considerations

1. Hashed email and password in the frontend.
2. Hashed passwords in the database in case a database is stolen, the passwords are hashed and salted.
3. React website is HTTPS and so is the backend.

### 🔑 Login Screen

The user is greeted with a login screen. This prevents anyone from accessing the Defend Me enterprise dashboard as it contains [PII](https://en.wikipedia.org/wiki/Personal_data) such as employee name, email and sensitive information.

![login screen](./demo/screenshots/LoginScreen.PNG)

### Enterprise Dashboard

🚧 Work in progress 🚧

## 👩‍💻 Developer Instructions

### Local

#### 🖥️ Windows

> [!IMPORTANT]
> Most of the commands below are ran using Git Bash so please install it from [here](https://git-scm.com/download/win) if you do not have it yet.

1. Ensure you have Node.js and npm installed in your machine. Check by running the following commands.

```
npm -v
```

```
node -v
```

If you do not have Node.js, install from [here](https://nodejs.org/en/download).

2. Ensure you have Python installed.

```
python --version
```

or

```
python3 --version
```

If you do not have Python, go ahead and install it from [here](https://www.python.org/).

3. Ensure you have `pip` installed.

```
pip --version
```

If you do not have `pip`, go ahead and refer to this [documentation](https://pypi.org/project/pip/).

4. You will need to install Apache 24 into your local machine. Follow instructions [here](https://httpd.apache.org/docs/current/platform/windows.html#down). **Troubleshooting:** If you get this error `AH00558: httpd.exe: Could not reliably determine the server's fully qualified domain name, using ::1. Set the 'ServerName' directive globally to suppress this message`, try these commands:
    - `sql-database/schema.sql`
    - Update in the `httpd.conf` file to `ServerName localhost`. It will be commented so you have to uncomment it.
    - Once the config is updated, you will need to restart the Apache24 server.
    - `cd C:\Apache24\bin`
    - `./httpd.exe -k install`
    - `./httpd.exe -k restart`

5. Follow steps below to modify Apache configurations. 
    - Run `mod_wsgi-express module-config`. 
    - Copy and paste the output of the terminal and add it to `C:\Apache24\conf\httpd.conf` file. 
    - You will need to restart the Apache server after updating the config `./httpd.exe -k restart`.
    - Start the Apache server `mod_wsgi-express start-server`.
    - On your browser go to [http://localhost:8000/](http://localhost:8000/).


6. You will need to create an SSL certificate in your local machine if you have not already with [mkcert using Chocolatey](https://github.com/FiloSottile/mkcert?tab=readme-ov-file#windows). If you **do not** have Chocolatey, install using Powershell using command [here](https://chocolatey.org/install). Ensure the `cert.pem` and `key.pem` files are created at the top level directory of `\defend-me\react-client`.


7. Once you have Python installed, you will need these following Python packages in `requirements.txt`. Run the following command to install them.

```
pip install -r requirements.txt
```

8. Run the commands below to initialise the database with seeded data.

```
cd sql-database
```

```
python init_db.sql
```

<details>

<summary>You should see the validation print to the console. Ensure it matches like in the sample here.</summary>

```
Initialising database with schema from schema.sql!

Starting table creation and insertion validation...

SELECT COUNT(*) FROM employee
100

SELECT COUNT(*) FROM administrator
5

SELECT COUNT(*) FROM admin_access
5

SELECT COUNT(*) FROM device
1000

SELECT COUNT(*) FROM scan
10000

Finished table creation and insertion validation!

Database initialised!
```

</details>

9. Run the commands below to start the backend server.

```
cd flask-server/
```

```
python server.py
```

10. Run the commands below to install the dependencies for React and start the frontend in another bash terminal.

```
cd react-client/
```

```
npm install
```

```
npm start
```

#### Troubleshooting

##### Cross-Origin Request Blocked and CORS issues
    - On Google Chrome enter `chrome://flags/#allow-insecure-localhost` and allow invalid certificates on localhost. This should be okay since it's just in our local dev environment with a self-signed SSL certificate.

## Credits

1. [Deep AI Image Generator](https://deepai.org/machine-learning-model/text2img) for the login screen background.
2. [React Icons](https://react-icons.github.io/react-icons/) for icons used within the website.
3. [Login Form](https://www.youtube.com/watch?v=kghwFYOJiNg) for the template.