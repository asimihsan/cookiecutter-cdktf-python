# {{ cookiecutter.cdktf_directory_name }}

## Getting started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Node.js](https://nodejs.org/en/download/package-manager/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- [CDKTF](https://learn.hashicorp.com/tutorials/terraform/cdktf-install)

#### AWS credentials

You will need AWS credentials set up. The easiest way to do this is to
use [aws-vault](https://github.com/99designs/aws-vault). For example if you put the following into `~/.aws/config`:

```ini
[profile retail-common]
region = {{ cookiecutter.aws_region }}
mfa_serial = arn:aws:iam::012345678901:mfa/mfa-device

[profile retail-admin]
include_profile = retail-common
role_arn = arn:aws:iam::012345678901:role/Administrator

[default]
credential_process = aws-vault exec retail-admin --region {{ cookiecutter.aws_region }} --json
```

- The `default` -> `credential_process` will cause `aws-vault` to be used for all AWS CLI commands transparently.
- The `role_arn` will cause `aws-vault` to assume the `Administrator` role in the `retail` account.
- The `mfa_serial` is the ARN of the MFA device for the `mfa-device` IAM user in the `retail` account.

If instead you use SSO (e.g. you log in using AWS Organizations), you can use the following:

```ini
[profile retail-common]
region = {{ cookiecutter.aws_region }}
sso_start_url = https://retail.awsapps.com/start

[profile retail-admin]
include_profile = retail-common
sso_account_id = 012345678901
sso_role_name = Administrator

[default]
credential_process = aws-vault exec retail-admin --region {{ cookiecutter.aws_region }} --json
```

For `sso_start_url` note that `region` must be the region of the SSO start URL, not the region of the account you are
logging into. In this example, we are logging into the `retail` account, which is in `{{ cookiecutter.aws_region }}`, but the SSO start URL
is in `{{ cookiecutter.aws_region }}`.

See https://github.com/99designs/aws-vault/blob/master/USAGE.md for detailed usage instructions.

### First-time setup

This will set up pre-commit hooks and install dependencies.

```shell
make dev-setup
```

This will deploy the Terraform backend to S3 and DynamoDB. You only need to do this once.

```shell
make cdktf-terraform-backend-deploy
```

### Deploying

There are two CDKTF stacks. The first is for the ECR repository, to which we push the AWS Lambda container image.

```shell
make cdktf-terraform-ecr-repo-deploy
```

In order to deploy the second stack, which contains AWS Lambda functions whose code are in container images, we
need to push the initial image version before we can deploy the stack.

```shell
make build-lambda-python
```

This Make command runs:

```shell
./scripts/build-lambda.sh --lambda-folder lambda_python --image-name lambda-python:latest
```

So you can add more container-based Lambda functions and similarly build them.

Then you need to first get CDKTF outputs (to get the ECR repo URL):

```shell
make cdktf-output
```

Then you can push the Lambda image

```shell
make push-lambda-python
```

Again, this just runs the following shell script that will let you push other images:

```shell
./scripts/push-to-ecr.sh --image-name lambda-python --tag latest --region {{ cookiecutter.aws_region }}
```

Then you can synthesize the main stack:

```shell
make cdktf-terrform-mystack-deploy
```

Once this works we can curl our AWS Lambda function URLs. Recall they are IAM authenticated so we need
to have AWS credentials available, which we get using `aws-vault`, and we need to SigV4 sign the HTTP
request, which `awscurl` does:

```shell
aws-vault exec retail-admin --region {{ cookiecutter.aws_region }} -- \
    awscurl --service lambda \
        https://mkvoargijs5s3obx6cyodfridi0zqhtf.lambda-url.{{ cookiecutter.aws_region }}.on.aws/ \
        --data '{"name": "World"}'
```
