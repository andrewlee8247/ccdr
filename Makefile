setup:
	python3 -m venv ~/.ccdr

install:
	
	pip3 install -r requirements.txt --user

test:
	python -m pytest -vv --cov=ccdrlib tests ccdr_appengine/main ccdr_appengine/test/*.py
	python -m pytest --nbval *.ipynb &&\
    python -m pytest --nbval  /home/alee66831/ccdr/raw_data_test/*ipynb


lint:
	pylint --disable=R,C *.py **/*.py

all: install lint test
