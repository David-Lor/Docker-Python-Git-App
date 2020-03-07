GIT_CLONE_FAILED_ERROR = "Error! Git Clone failed!"
PIP_INSTALL_FAILED_ERROR = "Error! Pip requirements install failed!"
OUTPUT_SUCCESS = "Hello World!"

REPOSITORY = "https://github.com/David-Lor/Python-HelloWorld.git"
MASTER_BRANCH = "master"
REQUIREMENTS_FAIL_BRANCH = "requirements-fail"
UNEXISTING_REPOSITORY = "https://github.com/David-Lor/Non-Existing-Repository.git"
UNEXISTING_BRANCH = "non-existing-branch"

USERNAME = "custom_username_for_testing"

with open("tools/built_image_name.txt") as file:
    IMAGE_NAME = file.read().strip()

DEFAULT_IMAGE_TAG = "latest"
DEFAULT_USE_SUDO = 1
