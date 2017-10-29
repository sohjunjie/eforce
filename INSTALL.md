# Emergency Force System

## Quick installation start
- Install postgres (pgadmin)
- Install python 3
- Install pip
- Install virtual environment

#### 1. Activate virtual environment and change directory to `eforce` folder and install related packages using the following command on `command prompt`
```
        $ pip install -r requirements.txt
```

#### 2. Create a database on postgres on the `postgres` console using the following command
```
# CREATE USER eforceapp WITH PASSWORD 'qwe123qwe123';
# CREATE DATABASE eforce OWNER eforceapp;
# ALTER ROLE eforceapp superuser;
# ALTER ROLE eforceapp SET client_encoding TO 'utf8';
# ALTER ROLE eforceapp SET default_transaction_isolation TO 'read committed';
# ALTER ROLE eforceapp SET timezone TO 'UTC';
# GRANT ALL PRIVILEGES ON DATABASE eforce TO eforceapp;
```

#### 3. Run migrations to create the database schemas
```
        $ python manage.py makemigrations
        $ python manage.py migrate
```

#### 4. Start the server on your local machine with
```
        $ python manage.py runserver
```
You can create your database objects such as users manually from http://127.0.0.1:8000/admin after running the server instance with ur local machine.
