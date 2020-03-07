# Docker Python Git App

A Docker image to deploy a Python app from a Git repository, to avoid building a Docker image for each app.
The container will handle the git clone and requirements installing before the app starts for the first time.

## Features

- Clone from GIT repository
- Choose branch to clone
- Install requirements from `requirements.txt` file

## Important! Required Python project structure

The entrypoint script expects the cloned repository to have the following structure:

```txt
ProjectRoot (cloned through Git)
│-  __main__.py (app entrypoint that will run)
|-  requirements.txt (if required)
│-  ...and all the other project files/directories
```

Some examples of projects compliant with this structure are:

- [Python-HelloWorld](https://github.com/David-Lor/Python-HelloWorld) (used as Git repository for testing this image)
- [MQTT2ETCD](https://github.com/David-Lor/MQTT2ETCD)
- [VigoBusAPI](https://github.com/David-Lor/Python_VigoBusAPI)

## Getting started

This image is WIP and not published yet on Docker Hub.

```bash
git clone https://github.com/David-Lor/Docker-Python-Autoclonable-App.git DockerPythonClonable
docker build DockerPythonClonable -t docker-python-git-app
docker run -e GIT_REPOSITORY="https://github.com/David-Lor/Python-HelloWorld.git" docker-python-git-app
```

## ENV Variables & ARGs

- `GIT_REPOSITORY`: URL of the remote Git repository to get the app from (required)
- `GIT_BRANCH`: set the Branch to clone from the Git repository (optional, default: use default branch)
- `APP_NAME`: name of your app. This name is given to the directory where project is cloned on(optional, default: _PythonApp_)
- (ARG) `USERNAME`: name of the user that is created on Dockerbuild to run the app with (optional, default: _user_)
- (ARG) `BASE_TAG`: tag of the [Python base image](https://hub.docker.com/_/python/) to be used for the build (optional, default: _latest_)

Only required variable is (ENV) `GIT_REPOSITORY`.
The variables marked with (ARG) are [build-args](https://docs.docker.com/engine/reference/commandline/build/#set-build-time-variables---build-arg).

## Building

If you want to build this image (required in order to change default username, base image tag or building
for unsupported architedtures), you must do on host machine:

- Clone this repository
- Build a new Docker image using the repository directory - you can optionally set these ARGs:
  - a custom username using the `USERNAME` ARG
  - a custom [Python base image](https://hub.docker.com/_/python/) tag using the `BASE_TAG` ARG (example: `alpine` or `slim`)
- Create a new container, setting up the desired ENV variables

```bash
git clone https://github.com/David-Lor/Docker-Python-Autoclonable-App.git DockerPythonClonable
docker build DockerPythonClonable --build-arg USERNAME=user --build-arg BASE_TAG=slim -t yourname/yourtag:yourversion
docker run [...] yourname/yourtag:yourversion
```

## Entrypoint pipeline

The steps that run when the container starts are:

- If this is the first time the container runs:
    1. clear output directory
    2. git clone
    3. pip install requirements.txt
    4. create a status file to mark the container already ran this setup process
- Start the cloned app

## Make utils

- `make test` - run tests (requires root/sudo and pytest)
- `make test USE_SUDO=0` - run tests without sudo (if current user is root or part of docker group)
- `make test-classic` - run tests sequentially (make test runs in parallel using pytest-xdist)
- `test-install-requirements` - pip install test requirements
- `sudo build BASE_TAG=slim` - build the image with the `python:slim` base image, and tag as `docker-python-git-app:slim`
- `sudo build BASE_TAG=alpine IMAGE_TAG=my-python:latest` - build the image with the `python:alpine` base image, and tag as `my-python:latest`

## Changelog

- 0.0.1 - Initial release

## TODO

- Allow setting GIT repository through CMD
- Load SSH private key for cloning SSH git repositories (from path or secret)
- Create Github Actions to build, test and push multiple tags to DockerHub (if possible all the tags available on the Python base image)
- Create multi-arch images
- Run as root with an env variable - or another image tag
