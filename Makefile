format:
	black -l 79 **/*.py

run-dev:
	FLASK_ENV=development FLASK_APP=feira/app.py flask run

install:
	pip install -r requirements.txt

init_db:
	FLASK_APP=feira/app.py flask create-db

import:
	FLASK_APP=feira/app.py flask import-csv

test:
	FLASK_ENV=test pytest tests/ -v --cov=feira