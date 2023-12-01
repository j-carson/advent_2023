.PHONY: setup clean

.venv:
	python3 -m venv `pwd`/.venv

setup: .venv
	. .venv/bin/activate && pip install --upgrade pip setuptools wheel
	. .venv/bin/activate && pip install -e .
	. .venv/bin/activate && nodeenv -p --node=lts
	. .venv/bin/activate && npm i -g @jakzo/aoc pyright
	cp wip.py .venv/lib/node_modules/\@jakzo/aoc/templates/python/
	. .venv/bin/activate && pre-commit install

clean:
	/bin/rm -rf .venv
