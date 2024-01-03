from cdktf import TerraformOutput
from cdktf_cdktf_provider_aws.ecr_repository import EcrRepository
from constructs import Construct

from cdktf_python_empty.stack.base import BaseStack, BaseStackProps


class EcrRepositoryStackProps(BaseStackProps):
    project_name: str


class EcrRepositoryStack(BaseStack):
    repository_url: str

    def __init__(self, scope: Construct, id: str, props: EcrRepositoryStackProps):
        super().__init__(scope, id, props)

        repository = EcrRepository(
            self,
            "ECRRepository",
            name=f"{props.project_name}-ecr-repo",
            image_tag_mutability="MUTABLE",
            image_scanning_configuration={"scan_on_push": True},
        )

        self.repository_url = repository.repository_url
        TerraformOutput(self, 'ecr_repo_repository_url', value=repository.repository_url)
