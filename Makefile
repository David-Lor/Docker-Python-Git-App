.DEFAULT_GOAL := default

test:
	pytest -sv -n auto tools/tests

test-classic:
	pytest -sv tools/tests

test-install-requirements:
	pip install -r tools/tests/requirements.txt

default:
	echo "No target specified!" && exit 1
