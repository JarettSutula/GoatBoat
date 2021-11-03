run: clean install setup test build
	docker compose up

clean:
	#cleans up cached files
	@(rm -rf ./GoatBoat_Mentoring.egg-info)
	@(rm -rf ./mentor/.mutmut-cache)
	@(rm -rf ./mentor/__pycache__)
	@(rm -rf ./mentor/GoatBoat_Mentoring.egg-info)
	@(rm -rf ./mentor/mentor/__pycache__)
	@(rm -rf ./mentor/mentor/GoatBoat_Mentoring.egg-info)

install:
    #run setup.py to install modules
	python setup.py install

#not sure if we need this if we have setup.py. Will ask Gildein.
setup: requirements.txt
	pip install -r requirements.txt

#run tests
test: 
	python ./mentor/userform/tests.py

#build dist
build:
	python setup.py bdist