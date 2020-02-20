
REQUIREMENTS="requirements.txt"
TAG="\n\n\033[0;32m\#\#\# "
END=" \#\#\# \033[0m\n"

all: init

uninstall-apisix:
	@echo $(TAG)Removing existing installation of apisix$(END)
	- pip uninstall --yes apisix >/dev/null
	@echo

uninstall-all: uninstall-apisix
	- pip uninstall --yes -r $(REQUIREMENTS)

init: uninstall-apisix
	@echo $(TAG)Installing requirements$(END)
	pip install --upgrade -r $(REQUIREMENTS)
	@echo $(TAG)Installing apisix$(END)
	pip install --upgrade --editable .
	@echo

test:
	@echo $(TAG)Running tests$(END)
	pip install pytest pytest-cov flake8
	flake8 apisix tests --ignore=E402,E226,E251,E501,F821
	export HOST='http://apisix.iresty.com' && \
	python /usr/local/bin/py.test --cov ./apisix --cov ./tests --verbose ./tests
	@echo

clean:
	@echo $(TAG)Cleaning up$(END)
	rm -rf .tox *.egg dist build .coverage
	find . -name '__pycache__' -delete -print -o -name '*.pyc' -delete -print
	@echo
