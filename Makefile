python_version := 3.6

.PHONY: test
test: virtual
	virtual/bin/pytest --verbose

virtual: requirements.txt
	python$(python_version) -m venv virtual
	virtual/bin/pip install --upgrade pip
	virtual/bin/pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf virtual
