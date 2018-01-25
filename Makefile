# Makefile for globomap-driver-sample

help:
	@echo
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  deploy     to deploy project in Tsuru"
	@echo "  test       to execute all tests"
	@echo

deploy:
	@tsuru app-deploy -a $(project) globomap_driver_sample Procfile requirements.txt scheduler.py run_loader.py

test:
	@coverage run --source=globomap_driver_sample -m unittest2 discover; coverage report -m

clone:
	@mkdir /tmp/bk; cd ../; cp -R globomap-driver-sample/ /tmp/bk/; cd /tmp/bk; mv globomap_driver_sample $(package); rm -rf .git/; sed -i .bak "s/globomap_driver_sample/$(package)/g" ./scheduler.py; sed -i .bak "s/globomap_driver_sample/$(package)/g" ./run_loader.py; sed -i .bak 's/Makefile for globomap-driver-sample/Makefile for $(package)/g' Makefile; rm -rf *.bak;
	@mv /tmp/bk/ ../$(project)/
