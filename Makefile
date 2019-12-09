init:
	pip install -r requirements.txt
	pip install .

activate:
	echo "hi"


.PHONY: init test