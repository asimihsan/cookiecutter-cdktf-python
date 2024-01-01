from typing import Any

from cdktf import S3Backend
from cdktf import TerraformStack
from cdktf_cdktf_provider_aws.provider import AwsProvider
from constructs import Construct
from pydantic import BaseModel


class BaseStackProps(BaseModel):
    region: str
    terraform_backend_bucket_name: str
    terraform_backend_lock_table_name: str
    common_tags: list[dict[str, Any]]


# Define a class for the base stack
class BaseStack(TerraformStack):
    def __init__(self, scope: Construct, id: str, props: BaseStackProps):
        super().__init__(scope, id)

        # Initialize the AWS provider
        AwsProvider(self, "aws", region=props.region, default_tags=props.common_tags)

        # Configure the S3 backend for Terraform state
        S3Backend(
            self,
            bucket=props.terraform_backend_bucket_name,
            key=f"terraform/{props.region}/{id}.tfstate",
            region=props.region,
            encrypt=True,
            dynamodb_table=props.terraform_backend_lock_table_name,
        )
