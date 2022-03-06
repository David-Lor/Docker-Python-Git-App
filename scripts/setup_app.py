#!/usr/bin/env python

"""SETUP APP Script
"""

import os
import subprocess
from datetime import datetime
from contextlib import suppress


class Settings:
    FIRST_RUN_FILENAME = ".setup_app_done"
    REQUIREMENTS_FILENAME = "requirements.txt"

    def __init__(self):
        try:
            self.app_name = os.environ["APP_NAME"]
            self.git_repository = os.environ["GIT_REPOSITORY"]
        except KeyError as error:
            raise Exception("Environment variable \"{}\" not defined!".format(error))
        
        self.base_dir = os.path.expanduser("~")
        self.first_run_file = self.join_home(self.FIRST_RUN_FILENAME)
        self.app_dir = self.join_home(self.app_name)
        self.requirements_file = self.join_app(self.REQUIREMENTS_FILENAME)
        self.git_branch = os.getenv("GIT_BRANCH")

    def join_home(self, path):
        return os.path.join(self.base_dir, path)

    def join_app(self, path):
        return os.path.join(self.app_dir, path)


def log(message):
    """Print log line with the current datetime
    """
    print("[{date}] {msg}".format(
        date=datetime.now().strftime("%y/%m/%d %H:%M:%S"),
        msg=message
    ))


def is_first_run(settings):
    """Return True if this is the first time the container runs
    """
    return not os.path.isfile(settings.first_run_file)


def save_setup_done(settings):
    """Store a file to mark this container already ran
    """
    os.mknod(settings.first_run_file)
    log("Saved 'App installed' status")


def clear_output_dir(settings):
    """Clear output directories
    """
    with suppress(FileNotFoundError):
        os.rmdir(settings.app_dir)
        log("Cleared output directories")


def clone(settings):
    """Clone the app through Git
    """
    log("Cloning app through Git...")
    branch_settings = []
    if settings.git_branch:
        branch_settings = ["--branch", settings.git_branch]

    result = subprocess.call(["git", "clone", *branch_settings, settings.git_repository, settings.app_dir])
    if result > 0:
        # TODO capture git output when fail
        raise Exception("Git Clone failed!")
    
    log("App cloned through Git!")


def install_requirements(settings):
    """Install Python package requirements through git, from requirements file
    """
    if os.path.isfile(settings.requirements_file):
        log("Installing requirements through Pip...")
        result = subprocess.call(["pip", "install", "--user", "-r", settings.requirements_file])
        if result > 0:
            raise Exception("Pip requirements install failed!")

        log("Requirements installed through Pip!")
    else:
        log("No requirements.txt file found")


def run():
    """Main run function
    """
    try:
        settings = Settings()
        args = (settings,)

        if is_first_run(*args):
            log("This is container first run, running app installing process...")
            clear_output_dir(*args)
            clone(*args)
            install_requirements(*args)
            save_setup_done(*args)
            log("Setup completed! Ready to run the app!")

        else:
            log("App already installed")

    except Exception as ex:
        log("Error! {}".format(ex))
        exit(1)


if __name__ == "__main__":
    run()
