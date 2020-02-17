# AdminPortal
Simple admin portal for an admin to create users and assign roles and permissions

### Available Endpoints:
| Http Method | Endpoint Route | Endpoint Functionality |
| :---         |     :---       |          :--- |
| POST   | /api/users     | Creates a user account    |
| GET     | /api/users/all        | Fetch all users     |
| GET/PUT/DELETE     | /api/user/int:id      | Get, Update, delete user      |
| POST     | /api/users/login/        | Login endpoint     |
| PUT     | /api/users/password_update/:token      |Updating a password       |
|POST/GET    |/api/groups|Create or list user groups
| GET/PUT/DELETE     | api/groups/int:id        | Get, Update, delete a group      |




### Prerequisites
```
  * pip
  * virtualenv
  * python 3 or python 2.7
  * postgresql
  * PgAdmin (Optional)
```
### Setting up database
#### To create the databases through the command line:
  ```
  $ psql postgres
  postgres=# CREATE DATABASE test
  
  ```
 ### Alternatively use PgAdmin:
  Open Postgres PgAdmin and create 2 databases test_store_db and store_manager
### Installation
clone the repo

``` 
git clone https://github.com/charitymarani/AdminPortal.git

```

create a virtual environment

```
virtualenv <environment name>

```

activate the environment:

```
$source <Your env name>/bin/activate

```
install dependencies:

```
$pip install -r requirements.txt

```

Run the app, and your ready to go!

```
python manage.py runserver

```
