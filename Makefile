init:
	python -m venv virtual


update:
	pip install -r requirements.txt
	pip install .

activate:
	source virtual/Scripts/activate


.PHONY: init test