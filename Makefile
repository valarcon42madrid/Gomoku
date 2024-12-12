
VENV := .venv

# default target, when make executed without arguments
all: venv

$(VENV)/bin/activate:
	python3 -m pip install --user virtualenv
	python3 -m virtualenv $(VENV)
	./$(VENV)/bin/pip install pygame

venv: $(VENV)/bin/activate

run: venv
	@read -p "Pulsa enter para ejecutar con interfáz visual, introduce cualquier carácter para jugar en terminal: " ab; \
	if [ -z "$$ab" ]; then \
		./$(VENV)/bin/python3 mainvisual.py || true; \
	else \
		./$(VENV)/bin/python3 mainsimple.py || true; \
	fi

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

.PHONY: all venv run clean
