setup:
	python3 -m venv ~/.ccdr

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv --cov=ccdrlib tests/*.py
	python -m pytest --nbval notebook.ipynb


lint:
	pylint --disable=R,C ccdrlib cli web

all: install lint test
