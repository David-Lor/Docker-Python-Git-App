# Docker Python Git App

[![Docker Hub](https://img.shields.io/badge/%20-DockerHub-blue?logo=docker&style=plastic)](https://hub.docker.com/r/davidlor/python-git-app)
![Build status](https://img.shields.io/github/workflow/status/David-Lor/Docker-Python-Git-App/Build,%20Test%20&%20Push?style=plastic)

A Docker image to deploy a Python app from a Git repository, to avoid building a Docker image for each app.
The container will handle the git clone and requirements installing before the app starts for the first time.

## Features

- Clone from GIT repository
- Choose branch to clone
- Install requirements from `requirements.txt` file
- Multiple tags available, with same names as those in the [official Python image](https://hub.docker.com/_/python/)

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

```bash
docker run -e GIT_REPOSITORY="https://github.com/David-Lor/Python-HelloWorld.git" davidlor/python-git-app
```

## ENV Variables & ARGs

- `GIT_REPOSITORY`: URL of the remote Git repository to get the app from (required)
- `GIT_BRANCH`: set the Branch to clone from the Git repository (optional, default: use default branch)
- `APP_NAME`: name of your app. This name is given to the directory where project is cloned on(optional, default: _PythonApp_)
- (ARG) `USERNAME`: name of the user that is created on Dockerbuild to run the app with (optional, default: _user_)
- (ARG) `BASE_TAG`: tag of the [Python base image](https://hub.docker.com/_/python/) to be used for the build (optional, default: _latest_)

Only required variable is (ENV) `GIT_REPOSITORY`.
The variables marked with (ARG) are [build-args](https://docs.docker.com/engine/reference/commandline/build/#set-build-time-variables---build-arg).

## Available tags

The tags available for the image are a limited selection of tags used in the [official Python image](https://hub.docker.com/_/python/).
The building and publishing of the images into DockerHub is performed by [this Github Actions workflow](https://github.com/David-Lor/Docker-Python-Git-App/blob/cdd45743d323afcea94014305eb5cc177eb96589/.github/workflows/build_test_push.yaml#L36),
where the full list of supported tags is defined.

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

## Useful Make utils

- `make test` - run tests (requires root/sudo & pytest)
- `make test USE_SUDO=0` - run tests without sudo (if current user is root or part of docker group)
- `make test-classic` - run tests sequentially (make test runs in parallel using pytest-xdist)
- `test-install-requirements` - pip install test requirements
- `sudo build BASE_TAG=slim` - build the image with the `python:slim` base image, and tag as `python-git-app:slim`
- `sudo build BASE_TAG=alpine IMAGE_TAG=my-python:latest` - build the image with the `python:alpine` base image, and tag as `my-python:latest`

## Changelog

- 0.2.1
    - Multi-arch support in Github Workflow
- 0.1.1
    - Upload to DockerHub from Github Workflow
    - Fix cmd in Dockerfile, change from `bash` to `sh` (Alpine compatibility)
    - Fix `test-nobuild*` rules in Makefile
    - Fix `image_tag` param on tests
    - Rename `IMAGE_TAG` to `IMAGE_NAME` when refering to the full image name (`name:tag`)
    - Remove Python 2 from tags (not officially supported here)
- 0.0.1
    - Initial release

## TODO

- Allow setting GIT repository through CMD
- Load SSH private key for cloning SSH git repositories (from path or secret)
- Create multi-arch images
- Run as root with an env variable - or another image tag
- Tag & upload images based on official Python image tags, plus versions of this repository
