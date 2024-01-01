export JSII_SILENCE_WARNING_UNTESTED_NODE_VERSION=1

.PHONY: lint
lint:
	poetry run black . --diff --check

.PHONY: lint-fix
lint-fix:
	poetry run black .

.PHONY: cdktf-terraform-backend-deploy
cdktf-terraform-backend-deploy:
	cdktf deploy terraform-backend
