#!/usr/bin/env python

from cdktf import App

from cdktf_python_empty.app_props import AppProps
from cdktf_python_empty.stack.ecr_repo import EcrRepositoryStack, EcrRepositoryStackProps
from cdktf_python_empty.stack.main import MyStack, MyStackProps
from cdktf_python_empty.stack.terraform_backend import (
    TerraformBackendStack,
    TerraformBackendStackProps,
)


def main():
    app = App()
    app_props = AppProps(
        project_name="{{ cookiecutter.project_slug_title_case }}",
        region="us-west-2",
        common_tags={"custom_tag": "custom_value"},
    )

    TerraformBackendStack(
        app,
        "terraform-backend",
        TerraformBackendStackProps(
            project_name=app_props.project_name,
            region=app_props.region,
            common_tags=app_props.common_tags,
        ),
    )

    ecr_repo_stack = EcrRepositoryStack(
        app,
        "ecr-repo",
        EcrRepositoryStackProps(
            project_name=app_props.project_name,
            region=app_props.region,
            terraform_backend_bucket_name=app_props.terraform_backend_bucket_name,
            terraform_backend_lock_table_name=app_props.terraform_backend_lock_table_name,
            common_tags=app_props.common_tags,
        ),
    )

    MyStack(app, "mystack", MyStackProps(
        project_name=app_props.project_name,
        region=app_props.region,
        terraform_backend_bucket_name=app_props.terraform_backend_bucket_name,
        terraform_backend_lock_table_name=app_props.terraform_backend_lock_table_name,
        common_tags=app_props.common_tags,
        ecr_repository_url=ecr_repo_stack.repository_url,
        lambda_python_image_name='lambda-python-latest',
        lambda_go_image_name='lambda-go-latest',
    ))

    app.synth()


if __name__ == "__main__":
    main()
