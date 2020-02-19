setup:
	python3 -m venv ~/.ccdr

install:
	
	pip3 install -r requirements.txt --user

test:
	python -m pytest -vv --cov=appengine &&\
    python -m pytest --nbval notebooks/*.ipynb 

lint:
	pylint --disable=R,C,W0702 **/*.py **/*.py **/**/*.py

all: install lint test
