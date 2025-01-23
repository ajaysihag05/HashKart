#                                                  HashKart

###### HashKart is one stop destination for all kinds of shopping needs for the customers.

###### Python Version is 3.11.9

## Steps To Setup HashKart Backend

#### 1. Clone the Repository

```bash
git clone https://github.com/ajaysihag05/HashKart.git
cd HashKart
```

#### 2. Create and Activate Virtual Env

###### Windows
```bash
python -m venv env
env/Scripts/activate
```

###### Ubuntu / MacOS
```bash
python -m venv env
source env/bin/activate
```

#### 3. Install Requirements and Initialise DB 
```bash
pip install -r requirements.txt
flask db init
flask db migrate -m "initial migrations"
flask db upgrade
```

#### 4. Run the Project 
```bash
python run.py
```

###### There is SQLlite DB file named "hashkart.db" which has some data in it and also provided the postmant collection named HashKart Backend.postman_collection.json, use that for testing the API's

###### User Credential for login using hashkart.db
"email": "ajay@test.com",
"password": "myname05"

###### For any questions or support, please contact ajsihag@deloitte.com
