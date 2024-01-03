export JSII_SILENCE_WARNING_UNTESTED_NODE_VERSION=1

.PHONY: dev-setup
dev-setup:
	./scripts/dev-setup.sh

.PHONY: lint
lint:
	poetry run black . --diff --check

.PHONY: lint-fix
lint-fix:
	poetry run black .

.PHONY: test
test:
	poetry run pytest

.PHONY: build-lambda
build-lambda:
	./scripts/build-lambda.sh --lambda-folder lambda_go --image-name lambda-go:latest
	./scripts/build-lambda.sh --lambda-folder lambda_python --image-name lambda-python:latest


.PHONY: push-lambda
push-lambda:
	./scripts/push-to-ecr.sh --image-name lambda-go --tag latest --region us-west-2
	./scripts/push-to-ecr.sh --image-name lambda-python --tag latest --region us-west-2

.PHONY: run-lambda-python
run-lambda-python:
	./scripts/run-lambda-python.sh

.PHONY: test-lambda-python
test-lambda-python:
	./scripts/test-lambda-python.sh

.PHONY: cdktf-terraform-backend-deploy
cdktf-terraform-backend-deploy:
	cdktf deploy terraform-backend

.PHONY: cdktf-terraform-ecr-repo-deploy
cdktf-terraform-ecr-repo-deploy:
	cdktf deploy ecr-repo

.PHONY: cdktf-terrform-mystack-deploy
cdktf-terrform-mystack-deploy:
	cdktf deploy ecr-repo mystack

.PHONY: cdktf-output
cdktf-output:
	cdktf output ecr-repo --outputs-file ecr-repo-outputs.json

.PHONY: cdktf-destroy
cdktf-destroy:
	cdktf destroy ecr-repo mystack
