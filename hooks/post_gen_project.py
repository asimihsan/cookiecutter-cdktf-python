import subprocess
import sys


def run(args: list[str]) -> None:
    """Run a command and exit if it fails.

    Args:
        args (list[str]): The command and arguments to run.
    """

    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)


def main():
    run(["poetry", "install"])
    run(["git", "init"])
    run(["make", "dev-setup"])


if __name__ == "__main__":
    main()
