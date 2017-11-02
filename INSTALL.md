# Emergency Force System

## Contents
- [Installation and setup](#1-quick-installation-and-setup)
- [Get the code](#2-get-the-sg-emergency-force-system-code)
- [Install dependencies](#3-install-dependencies)
- [Create the database](#3-create-the-database)
- [Sync code with database](#4-sync-code-with-database)
- [Starting the server](#5-starting-the-server)
- [Finally...](#6-finally...)

#### 1. Quick installation and setup
- Install postgres (pgadmin)
- Install python 3
- Install pip
- Install virtual environment

#### 2. Get the SG Emergency Force System Code

```
        git clone git@github.com:sohjunjie/eforce.git
```


#### 3. Install dependencies
Make sure to have virtual environment installed using `pip install virtualenv`. Create a virtual environemnt using `virtualenv venv` and activate the virtual environment.

Now change directory to `eforce` folder in the cloned project code and install the related packages using the following command on `command line`
```
        $ pip install -r requirements.txt
```
For more information about python virtual environment, refer to this [link](https://docs.python.org/3/library/venv.html)


#### 4. Create the database
Create a database on postgres on the `postgres` console using the following command
```
# CREATE USER eforceapp WITH PASSWORD 'qwe123qwe123';
# CREATE DATABASE eforce OWNER eforceapp;
# ALTER ROLE eforceapp superuser;
# ALTER ROLE eforceapp SET client_encoding TO 'utf8';
# ALTER ROLE eforceapp SET default_transaction_isolation TO 'read committed';
# ALTER ROLE eforceapp SET timezone TO 'UTC';
# GRANT ALL PRIVILEGES ON DATABASE eforce TO eforceapp;
```

#### 5. Sync code with database
You need to run migrations in `command line` to create the database schemas in the `postgres` database. The schemas to be created is found [here](eforce_api/models.py)
```
        $ python manage.py makemigrations
        $ python manage.py migrate
```

#### 6. Starting the server
Start the server on your local machine with
```
        $ python manage.py runserver
```
You can create your database objects such as users manually from http://127.0.0.1:8000/admin after running the server instance with ur local machine. Note that you need to execute the redis-server before `step 5`.

#### 7. Finally...
You might not be able to run the server successfully. This is because the required environment variables is not present in the eforce directory. Rename the [dot.env](dot.env) to simply `.env` to solve the issue.

Note that for this web application, we used third party services including AMAZON S3 and Google Map Services. API Keys need to be supplied for these services for it to be fully functional.
