# About

Vending machine backend.

Technical stack:
- FastAPI (uvicorn, SQLAlchemy, Pydantic, Swagger)
- DataBase SQLite

DataBase is created on the start if it doesn't exist. The same DB is used for development and testing.

Once server started the documentation is available on the page http://localhost:8000/docs/

Two users are created if they don't exists in DB:
1. Login: John, password: John, role: buyer
1. Login: Olivier, password: Olivier, role: seller

Tokens JWT are used for the authorizations.

File .env was added to git repository intentionally. For security reasons it should not be in git repository for real applications.

# Getting started

### Create a virtual environment Python
```
python3 -m venv env
```

### Activate the virtual environment
#### Windows
```
.\env\Scripts\activate
```
#### Linux
```
source env/bin/activate
```

### Install requirements
```
pip install -r requirements.txt
```

### Start uvicorn server
```
python3 -m uvicorn app.main:app --reload --proxy-headers --host 0.0.0.0 --port 8000
```

# Testing
Execute the command
```
python -m pytest app/tests/
```
