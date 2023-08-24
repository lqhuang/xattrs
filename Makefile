
SHELL := /bin/bash




docs:
	@echo "Building docs"
	$(MAKE) -C ./docs html
