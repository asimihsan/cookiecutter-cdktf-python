#!/usr/bin/env python

from cdktf import App

from {{ cookiecutter.cdktf_module_name }}.app_props import AppProps
from {{ cookiecutter.cdktf_module_name }}.stack.ecr_repo import EcrRepositoryStack, EcrRepositoryStackProps
from {{ cookiecutter.cdktf_module_name }}.stack.main import MyStack, MyStackProps
from {{ cookiecutter.cdktf_module_name }}.stack.terraform_backend import (
    TerraformBackendStack,
    TerraformBackendStackProps,
)


def main():
    app = App()
    app_props = AppProps(
        project_name="{{ cookiecutter.project_slug }}",
        region="{{ cookiecutter.aws_region }}",
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
