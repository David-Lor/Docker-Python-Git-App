from .helpers import BaseTest
from .const import *


class TestBuild(BaseTest):
    """Test building the image"""

    def test_build_default(self):
        """Test building the image with default parameters, then running the container, thus running the app"""
        image, output = self.build_image()
        assert image in output

        output = self.run_container(image=image)
        assert OUTPUT_SUCCESS in output

    def test_build_username(self):
        """Test building the image changing the username"""
        image, output = self.build_image(user=USERNAME)
        assert image in output

        output = self.run_container(image=image, args=["--entrypoint", "pwd"])
        assert "/home/{}".format(USERNAME) in output

    def test_build_from_alpine(self):
        """Test building the image using the 'python:alpine' base image"""
        image, output = self.build_image(from_image="python:alpine")
        assert image in output

        output = self.run_container(image=image, args=["--entrypoint", "which"], final_args=["apk"])
        assert "/sbin/apk" in output

    def test_build_from_pyston(self):
        """Test building the image using the 'pyston/pyston' base image"""
        image, output = self.build_image(from_image="pyston/pyston")
        assert image in output

        output = self.run_container(image=image, args=["--entrypoint", "python"], final_args=["-V"])
        assert "[Pyston " in output

    def test_build_from_pypy(self):
        """Test building the image using the 'pypy' base image"""
        image, output = self.build_image(from_image="pypy")
        assert image in output

        output = self.run_container(image=image, args=["--entrypoint", "python"], final_args=["-V"])
        assert "[PyPy " in output
