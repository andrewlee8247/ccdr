setup:
	python3 -m venv ~/.ccdr

install:
	
	pip3 install -r requirements.txt --user

test:
	python -m pytest -vv --cov=appengine **/*.py &&\
    python -m pytest --show-capture=no --nbval notebooks/*.ipynb 

lint:
	pylint --disable=R,C,W0702,W0613,W0611,W0104,W0621,W0125,E1101,W0106,W0212,W0402,W0603,E0401,W0703 \
    **/*.py **/*.py **/**/*.py

all: install lint test
