import pytest
from cdktf_python_empty.app_props import AppProps


# Mock the get_aws_regions function to return a fixed set of regions for testing
@pytest.fixture
def mock_get_aws_regions(mocker):
    mocker.patch('cdktf_python_empty.app_props.get_aws_regions', return_value={'us-east-1', 'us-west-2'})


# Test the creation of AppProps with valid data
def test_appprops_creation_valid(mock_get_aws_regions):
    app_props = AppProps(
        project_name="myproject",
        region="us-east-1",
        common_tags={"key": "project", "value": "myproject"},
    )
    assert app_props.project_name == "myproject"
    assert app_props.region == "us-east-1"
    assert app_props.common_tags == {"Project": "myproject",
                                     "Terraform": "true",
                                     "key": "project",
                                     "value": "myproject"}


# Test the creation of AppProps with an empty project name
def test_appprops_creation_empty_project_name():
    with pytest.raises(ValueError) as excinfo:
        AppProps(
            project_name="",
            region="us-east-1",
            common_tags={"key": "project", "value": "myproject"}
        )
    assert "project_name must not be empty" in str(excinfo.value)


# Test the creation of AppProps with an invalid region
def test_appprops_creation_invalid_region(mock_get_aws_regions):
    with pytest.raises(ValueError) as excinfo:
        AppProps(
            project_name="myproject",
            region="invalid-region",
            common_tags={"key": "project", "value": "myproject"}
        )
    assert "region invalid-region is not valid" in str(excinfo.value)


# Test the default tags are set correctly
def test_appprops_default_tags(mock_get_aws_regions):
    app_props = AppProps(
        project_name="myproject",
        region="us-east-1",
    )
    assert app_props.common_tags == {"Project": "myproject",
                                     "Terraform": "true"}


# Test the Terraform backend bucket name generation
def test_terraform_backend_bucket_name(mock_get_aws_regions):
    app_props = AppProps(
        project_name="myproject",
        region="us-east-1",
    )
    assert app_props.terraform_backend_bucket_name == "myproject-terraform-state-us-east-1"


# Test the Terraform backend lock table name generation
def test_terraform_backend_lock_table_name(mock_get_aws_regions):
    app_props = AppProps(
        project_name="myproject",
        region="us-east-1",
    )
    assert app_props.terraform_backend_lock_table_name == "myproject-terraform-state-lock-us-east-1"
