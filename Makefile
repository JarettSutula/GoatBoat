run: clean install setup check test mutatetest build
	docker compose up

#cleans up cached files
clean:
	@(rm -rf ./GoatBoat_Mentoring.egg-info)
	@(rm -rf ./mentor/.mutmut-cache)
	@(rm -rf ./mentor/__pycache__)
	@(rm -rf ./mentor/GoatBoat_Mentoring.egg-info)
	@(rm -rf ./mentor/mentor/__pycache__)
	@(rm -rf ./mentor/mentor/GoatBoat_Mentoring.egg-info)

install:
    #run setup.py to install modules
	python setup.py install --user

#not sure if we need this if we have setup.py. Will ask Gildein.
setup: requirements.txt
	pip install -r requirements.txt

#run tests
test: 
	python ./mentor/tests.py

#build dist
build:
	python setup.py bdist

mutatetest:
	-cd mentor && python -m mutmut run --paths-to-mutate=utils.py --runner "python -m unittest formtests.py"

check:
	python -m safety check -r requirements.txt
	-python -m liccheck -s authorized_licenses.ini -r requirements.txt
	