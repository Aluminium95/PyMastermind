PY = python3
MAIN = main
DOCDIR = ./Documentation/PyDoc/

.PHONY: all clean doc conf

all: clean
	$(PY) "$(MAIN).py"
	make clean

clean:
	rm -rf *.pyc
	rm -rf *~

doc: clean
	pydoc2 -w ./
	mv *.html $(DOCDIR)

conf: clean
	$(PY) configuration.py
