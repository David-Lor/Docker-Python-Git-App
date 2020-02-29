import subprocess
from uuid import uuid4
from os import getenv
from .const import *

__all__ = ("BaseTest",)

DEFAULT_REPOSITORY = getenv("DEFAULT_REPOSITORY", REPOSITORY)
USE_SUDO = bool(int(getenv("USE_SUDO", 1)))


class BaseTest:
    created_images: set

    @classmethod
    def setup_class(cls):
        cls.created_images = set()

    @classmethod
    def teardown_class(cls):
        for image in cls.created_images:
            cls.delete_image(image)

    @staticmethod
    def delete_image(image):
        cmd = ["docker", "image", "rm", image]
        if USE_SUDO:
            cmd = ["sudo", *cmd]

        subprocess.call(cmd)

    @staticmethod
    def run_container(repository=DEFAULT_REPOSITORY, branch=None, args=None, image=IMAGE_NAME, final_args=None):
        """
        :param repository: Git repository URL
        :param branch: Git branch
        :param args: args for Docker Run command to use in the middle (before defining the image)
        :param image: image to use
        :param final_args: args for Docker Run command to use at the end (after defining the image)
        :return: command output
        """
        if args is None:
            args = []

        if branch:
            args.extend(["-e", "GIT_BRANCH={}".format(branch)])

        args.extend(["-e", "GIT_REPOSITORY={}".format(repository)])

        cmd = ["docker", "run", "--rm", *args, image]
        if USE_SUDO:
            cmd = ["sudo", *cmd]

        if final_args:
            cmd.extend(final_args)

        try:
            return subprocess.check_output(cmd).decode()
        except subprocess.CalledProcessError as error:
            return error.output.decode()

    @classmethod
    def build_image(cls, image=None, args=None, base_tag=None, user=None):
        """
        :param image: image name (if not defined, use a random uuid4 as name)
        :param args: args for Docker Build command
        :param base_tag: set IMAGE_TAG build Arg
        :param user: set USERNAME build Arg
        :return: [image name, command output]
        """
        if args is None:
            args = []

        if image is None:
            image = str(uuid4())

        if base_tag:
            args.extend(["--build-arg", "IMAGE_TAG={}".format(base_tag)])

        if user:
            args.extend(["--build-arg", "USERNAME={}".format(user)])

        args.extend(["-t", image])

        try:
            cmd = ["docker", "build", *args, "."]
            if USE_SUDO:
                cmd = ["sudo", *cmd]

            output = subprocess.check_output(cmd).decode()
            cls.created_images.add(image)

            return image, output

        except subprocess.CalledProcessError as error:
            return image, error.output.decode()
