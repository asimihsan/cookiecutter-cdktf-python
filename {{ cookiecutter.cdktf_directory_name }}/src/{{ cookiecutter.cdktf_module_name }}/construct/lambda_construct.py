import json

from cdktf import TerraformOutput
from cdktf_cdktf_provider_aws.iam_role import IamRole, IamRoleInlinePolicy
from cdktf_cdktf_provider_aws.lambda_function import LambdaFunction, LambdaFunctionEnvironment
from cdktf_cdktf_provider_aws.lambda_function_url import LambdaFunctionUrl
from constructs import Construct

from cdktf_python_empty.stack.base import BaseConstructProps


class LambdaConstructProps(BaseConstructProps):
    project_name: str
    ecr_repository_url: str
    image_name: str


class LambdaConstruct(Construct):
    function_url: LambdaFunctionUrl

    def __init__(self, scope: Construct, id: str, props: LambdaConstructProps):
        super().__init__(scope, id)

        id_ = f"{props.project_name}-{id}"

        lambda_role = IamRole(
            self,
            f"{id_}-execution-role",
            name=f"{id_}-execution-role",
            assume_role_policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "lambda.amazonaws.com"
                        },
                        "Action": "sts:AssumeRole"
                    }
                ]
            }),
            inline_policy=[IamRoleInlinePolicy(
                name=f"{id_}-policy",
                policy=json.dumps({
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",

                            # To call s3:ListBuckets, the corresponding IAM action is s3:ListAllMyBuckets.
                            "Action": [
                                "s3:ListBuckets",
                                "s3:ListAllMyBuckets",
                            ],

                            "Resource": "*",
                        },
                    ]
                })
            )],
        )

        image_uri = f"{props.ecr_repository_url}:{props.image_name}"
        lambda_function = LambdaFunction(
            self,
            "LambdaFunction",
            function_name=f"{id_}-function",
            package_type="Image",
            image_uri=image_uri,
            architectures=["arm64"],
            memory_size=128,
            timeout=5,
            role=lambda_role.arn,
            environment=LambdaFunctionEnvironment(
                variables={
                    "REGION": props.region,
                },
            ),
        )

        self.function_url = LambdaFunctionUrl(
            self,
            "LambdaFunctionUrl",
            function_name=lambda_function.function_name,
            authorization_type="AWS_IAM",
        )

        TerraformOutput(self, 'lambda_function_url', value=self.function_url.function_url)
