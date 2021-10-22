run: setup testDB clean
	python ./mentor/manage.py runserver

setup: requirements.txt
	pip install -r requirements.txt
clean:
	if [ -a ./mentor/__pycache__ ] ; \
	then \
     		rm -r ./mentor/__pycache__ ; \
	fi;


testDB:
	python ./mentor/userform/dbtests.py
