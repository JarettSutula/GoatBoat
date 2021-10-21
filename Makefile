run: setup clean
	python ./mentor/manage.py runserver

setup: requirements.txt
	pip install -r requirements.txt

clean:
	rm -r mentor/__pycache__
