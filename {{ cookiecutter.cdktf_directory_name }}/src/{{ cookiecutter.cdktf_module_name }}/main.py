#!/usr/bin/env python

from typing import Any

from cdktf import App
from cdktf_cdktf_provider_aws.s3_bucket import S3Bucket
from constructs import Construct
from pydantic import BaseModel

from {{ cookiecutter.cdktf_module_name }}.stack.base import BaseStack, BaseStackProps
from {{ cookiecutter.cdktf_module_name }}.stack.terraform_backend import (
    TerraformBackendStack,
    TerraformBackendStackProps,
)


class {{ cookiecutter.project_slug_title_case }}StackProps(BaseStackProps):
    project_name: str
    bucket_name: str


class {{ cookiecutter.project_slug_title_case }}Stack(BaseStack):
    def __init__(self, scope: Construct, id: str, props: {{ cookiecutter.project_slug_title_case }}StackProps):
        super().__init__(scope, id, props)

        # See: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket?lang=python
        S3Bucket(
            self,
            "mybucket",
            bucket=f"${props.bucket_name}-bucket",
            acl="private",
        )


class {{ cookiecutter.project_slug_title_case }}Props(BaseModel):
    project_name: str
    region: str
    common_tags: list[dict[str, Any]]
    bucket_name: str


def main():
    app = App()
    app_props = {{ cookiecutter.project_slug_title_case }}Props(
        project_name="myproject",
        region="{{ cookiecutter.aws_region }}",
        common_tags=[{"tags": {"project": "myproject"}}],
        bucket_name="mybucket",
    )

    backend_stack = TerraformBackendStack(
        app,
        "terraform-backend",
        TerraformBackendStackProps(
            project_name=app_props.project_name,
            region=app_props.region,
            common_tags=app_props.common_tags,
        ),
    )

    {{ cookiecutter.project_slug_title_case }}Stack(
        app,
        "{{ cookiecutter.project_slug_hyphens }}",
        {{ cookiecutter.project_slug_title_case }}StackProps(
            project_name=app_props.project_name,
            region=app_props.region,
            terraform_backend_bucket_name=backend_stack.state_bucket_name,
            terraform_backend_lock_table_name=backend_stack.lock_table_name,
            common_tags=[{"tags": {"project": "myproject"}}],

            bucket_name=app_props.bucket_name,
        ),
    )

    app.synth()


if __name__ == "__main__":
    main()
