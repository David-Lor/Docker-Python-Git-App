from .helpers import BaseTest
from .const import *


class TestBuild(BaseTest):
    """Test building the image
    """

    def test_build_default(self):
        """Test building the image with default parameters, then running the container, thus running the app
        """
        image, output = self.build_image()
        assert image in output
        
        output = self.run_container(image_name=image)
        assert OUTPUT_SUCCESS in output

    def test_build_username(self):
        """Test building the image changing the username
        """
        image, output = self.build_image(user=USERNAME)
        assert image in output
        
        output = self.run_container(image_name=image, final_args=["pwd"])
        assert "/home/{}".format(USERNAME) in output

    def test_build_tag_alpine(self):
        """Test building the image using the 'alpine' base tag
        """
        image, output = self.build_image(base_tag="alpine")
        assert image in output

        output = self.run_container(image_name=image, args=["--entrypoint", "which"], final_args=["apk"])
        assert "/sbin/apk" in output

    def test_build_python_27(self):
        """Test building the image using the '2.7-alpine' base tag
        """
        image, output = self.build_image(base_tag="2.7-alpine")
        assert image in output

        output = self.run_container(image_name=image, final_args=["python", "-V"])
        assert output.startswith("Python 2.7")
