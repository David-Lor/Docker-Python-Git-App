from .helpers import BaseTest
from .const import *


class TestBuild(BaseTest):
    def test_build_default(self):
        """Test building the image with default parameters, then running the container, thus running the app
        """
        image, output = self.build_image()
        assert image in output
        
        output = self.run_container(image=image)
        assert OUTPUT_SUCCESS in output

    def test_build_username(self):
        """Test building the image changing the username
        """
        image, output = self.build_image(user=USERNAME)
        assert image in output
        
        output = self.run_container(image=image, final_args=["pwd"])
        assert "/home/{}".format(USERNAME) in output

    def test_build_tag_alpine(self):
        """Test building the image using the 'alpine' base tag
        """
        image, output = self.build_image(base_tag="alpine")
        assert image in output

        output = self.run_container(image=image, args=["--entrypoint", "which"], final_args=["apk"])
        assert "/sbin/apk" in output
