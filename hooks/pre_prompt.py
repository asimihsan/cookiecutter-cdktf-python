import subprocess
import sys

from dataclasses import dataclass


def is_program_installed(args: list[str]) -> bool:
    """Check if a program is installed on the system.

    Args:
        args (list[str]): The program and arguments to run.

    Returns:
        bool: True if the program is installed, False otherwise.
    """

    try:
        subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


@dataclass
class Dependency:
    name: str
    args: list[str]
    install_url: str


dependencies: dict[str, Dependency] = {
    "docker": Dependency(
        name="docker",
        args=["docker", "--version"],
        install_url="https://docs.docker.com/engine/install/",
    ),
    "node": Dependency(
        name="node",
        args=["node", "--version"],
        install_url="https://nodejs.org/en/download/package-manager/",
    ),
    "poetry": Dependency(
        name="poetry",
        args=["poetry", "--version"],
        install_url="https://python-poetry.org/docs/#installation",
    ),
    "terraform": Dependency(
        name="terraform",
        args=["terraform", "--version"],
        install_url="https://learn.hashicorp.com/tutorials/terraform/install-cli",
    ),
    "cdktf": Dependency(
        name="cdktf",
        args=["cdktf", "--version"],
        install_url="https://learn.hashicorp.com/tutorials/terraform/cdktf-install",
    ),
}


def main() -> int:
    missing_dependencies: list[Dependency] = []

    for dependency in dependencies.values():
        if not is_program_installed(dependency.args):
            missing_dependencies.append(dependency)

    if missing_dependencies:
        print("The following dependencies are missing:")
        for dependency in missing_dependencies:
            print(f" - {dependency.name}")
            print(f"   Install instructions: {dependency.install_url}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
