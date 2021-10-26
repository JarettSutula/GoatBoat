run: setup test clean
	#python ./mentor/manage.py runserver
	docker compose up

setup: requirements.txt
	pip install -r requirements.txt
clean:
	if [ -a ./mentor/__pycache__ ] ; \
	then \
     		rm -r ./mentor/__pycache__ ; \
	fi;

test: 
	python ./mentor/userform/tests.py

testDB:
	python ./mentor/userform/dbtests.py
