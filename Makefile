# Makefile for globomap-driver-sample

PROJECT_HOME = "`pwd`"

help:
	@echo
	@echo "Please use 'make <target>' where <target> is one of"
	@echo

	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

setup: ## Install project dependencies
	@pip install -r $(PROJECT_HOME)/requirements_test.txt

clean: ## Clear *.pyc files, etc
	@rm -rf build dist *.egg-info
	@find . \( -name '*.pyc' -o  -name '__pycache__' -o -name '**/*.pyc' -o -name '*~' \) -delete

tests: clean ## Make tests
	@nosetests --verbose --rednose  --nocapture --cover-package=globomap_driver_sample --with-coverage; coverage report -m

deploy: ## Make deploy
	@tsuru app-deploy -a $(project) globomap_driver_sample Procfile requirements.txt scheduler.py run_loader.py .python-version

clone:
	@mkdir /tmp/bk; cd ../; cp -R globomap-driver-sample/ /tmp/bk/; cd /tmp/bk; mv globomap_driver_sample $(package); rm -rf .git/; sed -i .bak "s/globomap_driver_sample/$(package)/g" ./scheduler.py; sed -i .bak "s/globomap_driver_sample/$(package)/g" ./run_loader.py; sed -i .bak "s/globomap_driver_sample/$(package)/g" Makefile; sed -i .bak 's/Makefile for globomap-driver-sample/Makefile for $(package)/g' Makefile; rm -rf *.bak;
	@mv /tmp/bk/ ../$(project)/
