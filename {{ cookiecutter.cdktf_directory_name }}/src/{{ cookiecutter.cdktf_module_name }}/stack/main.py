from cdktf_cdktf_provider_aws.s3_bucket import S3Bucket
from constructs import Construct

from cdktf_python_empty.construct.lambda_construct import LambdaConstruct, LambdaConstructProps
from cdktf_python_empty.stack.base import BaseStackProps, BaseStack


class MyStackProps(BaseStackProps):
    project_name: str
    ecr_repository_url: str
    lambda_python_image_name: str
    lambda_go_image_name: str


class MyStack(BaseStack):
    def __init__(self, scope: Construct, id: str, props: MyStackProps):
        super().__init__(scope, id, props)

        S3Bucket(
            self,
            "mybucket",
            bucket_prefix=f"{props.project_name}-bucket-{props.region}",
            acl="private",
        )

        LambdaConstruct(
            self,
            "lambda-python",
            LambdaConstructProps(
                project_name=props.project_name,
                region=props.region,
                common_tags=props.common_tags,
                ecr_repository_url=props.ecr_repository_url,
                image_name=props.lambda_python_image_name,
            ),
        )

        LambdaConstruct(
            self,
            "lambda-go",
            LambdaConstructProps(
                project_name=props.project_name,
                region=props.region,
                common_tags=props.common_tags,
                ecr_repository_url=props.ecr_repository_url,
                image_name=props.lambda_go_image_name,
            ),
        )
