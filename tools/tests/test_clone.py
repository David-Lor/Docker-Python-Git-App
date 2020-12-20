from .helpers import BaseTest
from .const import *


class TestClone(BaseTest):
    """Test the repository cloning, thus running the app
    """

    def test_clone_existing_repository(self):
        """Test cloning from an existing repository
        """
        output = self.run_container()
        assert OUTPUT_SUCCESS in output

    def test_clone_unexisting_repository(self):
        """Test cloning from a repository that does not exist
        """
        output = self.run_container(repository=UNEXISTING_REPOSITORY)
        assert GIT_CLONE_FAILED_ERROR in output

    def test_clone_existing_branch_fail_pip_install(self):
        """Test cloning from an existing repository, an existing branch
        (the requirements-fail branch, that will fail pip install)
        """
        # TODO Create another branch on Python-HelloWorld repository that won't fail but output something different
        output = self.run_container(branch=REQUIREMENTS_FAIL_BRANCH)
        assert PIP_INSTALL_FAILED_ERROR in output

    def test_clone_unexisting_branch(self):
        """Test cloning from an existing repository, a branch that does not exist
        """
        output = self.run_container(branch="non-existing-branch")
        assert GIT_CLONE_FAILED_ERROR in output
