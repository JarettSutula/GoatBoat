run: clean install setup test
	docker compose up

#not sure if we need this if we have setup.py. Will ask Gildein.
setup: requirements.txt
	pip install -r requirements.txt

test: 
	python ./mentor/userform/tests.py

testDB:
	python ./mentor/userform/dbtests.py

install:
	python setup.py install

clean:
	#cleans up cached files
	@(rm -rf ./GoatBoat_Mentoring.egg-info)
	@(rm -rf ./mentor/.mutmut-cache)
	@(rm -rf ./mentor/__pycache__)
	@(rm -rf ./mentor/GoatBoat_Mentoring.egg-info)
	@(rm -rf ./mentor/mentor/__pycache__)
	@(rm -rf ./mentor/mentor/GoatBoat_Mentoring.egg-info)
