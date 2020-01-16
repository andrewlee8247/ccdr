setup:
	python3 -m venv ~/.ccdr

install:
	#pip3 install --upgrade pip --user &&\
	
	pip3 install -r requirements.txt --user

test:
	python -m pytest -vv --cov=ccdrlib tests/*.py
	python -m pytest --nbval notebook.ipynb


lint:
	pylint --disable=R,C ccdrlib cli web

all: install lint test
