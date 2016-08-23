THIS_FILE := $(lastword $(MAKEFILE_LIST))

CYTHON=cython
CC=gcc
DEPS=LocationPicker.py
BUILD=build
FILES=$(wildcard build/*.c)
EXPRESS=$(wildcard build/expressvpn/*.c)

cython:
	mkdir -p build
	cython --embed Window.py -o build
	$(foreach dep,$(DEPS), $(MAKE) $(dep))
	make -C expressvpn
	mkdir -p build/expressvpn
	cp -v expressvpn/build/* build
	$(MAKE) compile

$(DEPS):
	$(CYTHON) $@ -o build

compile:
	$(CC) -Os -I /usr/include/python3.5m -o expressgui $(FILES) $(EXPRESS) -lpython3.5m -lpthread -lm -lutil -ldl
	
clean:
	rm -R -f build
	rm -f expressgui
	cd expressvpn && $(MAKE) clean