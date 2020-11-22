format:
	black -l 79 **/*.py

run:
	FLASK_ENV=development FLASK_APP=feira/app.py 
	make init_db
	flask run

install:
	pip install -r requirements.txt

init_db:
	FLASK_APP=feira/app.py flask feira create_db

import:
	FLASK_APP=feira/app.py flask feira import_csv

test:
	FLASK_ENV=test pytest tests/ -v --cov-report html --cov=feira