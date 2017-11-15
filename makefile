.PHONY: lint

lint:
	pylint --rcfile=.pylintrc app -f parseable -r n && \
	pycodestyle app --max-line-length=120 && \
	pydocstyle app
