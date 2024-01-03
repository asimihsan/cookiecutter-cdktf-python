from typing import Any

from pydantic import BaseModel, model_validator
from boto3.session import Session


def get_aws_regions(partition_name='aws') -> set[str]:
    """
    Get a set of AWS regions.

    This is just a list of AWS regions that the current version of boto3 knows about. This list may not be complete.
    Moreover, AWS accounts are typically not enabled for new regions, even if a region appears in this list there
    may be a manual console action needed to enable it. Finally, this is just for the main 'aws' partition, keep in mind
    that there are other partitions such as 'aws-cn' and 'aws-us-gov' that may have different regions.

    :return: A set of AWS regions
    """
    s = Session()
    return set(s.get_available_regions('dynamodb', partition_name=partition_name))


class AppProps(BaseModel):
    """
    A model representing the properties of an application.

    This class is used to validate and manage the properties of an application, including the project name, region, and
    common tags. It also provides methods to generate the names of the Terraform backend bucket and lock table based
    on the project name and region.

    Usage:
        app_props = AppProps(
            project_name="myproject",
            region="us-east-2",
            common_tags=[{"tags": {"project": "myproject"}}],
        )

    Note:
        This class is not thread-safe. If you need to use it in a multi-threaded context, make sure to add appropriate
        locking.
    """

    # The name of the project.
    project_name: str

    # The AWS region where the project is located.
    region: str

    # A list of common tags for the project. These are applied to all AWS resources created by the project.
    common_tags: dict[str, Any] = dict()

    @model_validator(mode='after')
    def check_project_name_not_empty(self) -> "AppProps":
        if self.project_name == '':
            raise ValueError('project_name must not be empty')
        return self

    @model_validator(mode='after')
    def check_region_is_valid(self) -> "AppProps":
        if self.region not in get_aws_regions():
            raise ValueError(f'region {self.region} is not valid')
        return self

    @model_validator(mode='after')
    def set_default_tags(self) -> "AppProps":
        # Define default tags
        default_tags = {'Terraform': 'true',
                        'Project': self.project_name}
        self.common_tags = default_tags | self.common_tags

        return self

    @property
    def terraform_backend_bucket_name(self) -> str:
        """
        Generate the name of the Terraform backend bucket.

        :return: The name of the Terraform backend bucket.
        """
        return f"{self.project_name}-terraform-state-{self.region}"

    @property
    def terraform_backend_lock_table_name(self) -> str:
        """
        Generate the name of the Terraform backend lock table.

        :return: The name of the Terraform backend lock table.
        """
        return f"{self.project_name}-terraform-state-lock-{self.region}"
