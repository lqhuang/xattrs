
SHELL := /bin/bash




docs:
	@echo "Building docs"
	$(MAKE) -C ./docs html

live-docs:
	@echo "Start a server for docs live preview ..."
	$(MAKE) -C ./docs live-html
