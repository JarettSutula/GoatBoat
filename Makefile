run: setup test 
	#python ./mentor/manage.py runserver
	docker compose up

setup: requirements.txt
	pip install -r requirements.txt

test: 
	python ./mentor/userform/tests.py
	python ./mentor/formtests.py

testDB:
	python ./mentor/userform/dbtests.py
