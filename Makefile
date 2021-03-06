all: fmt

fmt:
	black packages/calculator
	isort packages/calculator

init:
	pip install -r packages/calculator/requirements.txt
	pip install black isort

deploy:
	doctl serverless deploy . --remote-build

undeploy:
	doctl serverless undeploy calculator/convert

.PHONY: all fmt init deploy undeploy
