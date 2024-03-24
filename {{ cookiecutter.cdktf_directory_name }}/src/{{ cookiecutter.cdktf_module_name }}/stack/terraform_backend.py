from typing import Any

from cdktf import TerraformStack
from cdktf_cdktf_provider_aws.dynamodb_table import DynamodbTable
from cdktf_cdktf_provider_aws.provider import AwsProvider, AwsProviderDefaultTags
from cdktf_cdktf_provider_aws.s3_bucket import S3Bucket
from cdktf_cdktf_provider_aws.s3_bucket_acl import S3BucketAcl
from constructs import Construct
from pydantic import BaseModel


class TerraformBackendStackProps(BaseModel):
    project_name: str
    region: str
    common_tags: dict[str, Any]


class TerraformBackendStack(TerraformStack):
    lock_table_name: str
    state_bucket_name: str

    def __init__(self, scope: Construct, id: str, props: TerraformBackendStackProps):
        super().__init__(scope, id)

        AwsProvider(self, "aws",
                    region=props.region,
                    default_tags=[AwsProviderDefaultTags(tags=props.common_tags)])

        self.lock_table_name = f"{props.project_name}-terraform-state-lock-{props.region}"
        DynamodbTable(
            self,
            "terraform_state_lock",
            name=self.lock_table_name,
            attribute=[{"name": "LockID", "type": "S"}],
            hash_key="LockID",
            billing_mode="PAY_PER_REQUEST",
        )

        self.state_bucket_name = f"{props.project_name}-terraform-state-{props.region}"
        bucket = S3Bucket(self, "terraform_state_bucket", bucket=self.state_bucket_name)
        S3BucketAcl(
            self,
            "terraform-state-bucket-acl",
            bucket=bucket.id,
            acl="private",
        )        
