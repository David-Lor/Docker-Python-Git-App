# Docker Python Git App

[![Docker Hub](https://img.shields.io/badge/%20-DockerHub-blue?logo=docker&style=plastic)](https://hub.docker.com/r/davidlor/python-git-app)
![Build status](https://img.shields.io/github/workflow/status/David-Lor/Docker-Python-Git-App/Build,%20Test%20&%20Push?style=plastic)

A Docker image to deploy a Python app from a Git repository, to avoid building a Docker image for each app.
The container will handle the git clone and requirements installing before the app starts for the first time.

## Features

- Clone from GIT repository
- Choose branch to clone
- Install requirements from `requirements.txt` file
- [Multiple base images & tags available](images.json)
- Multi-arch buildings: `linux/amd64`, `linux/arm/v7`
- Automatic builds on monday, wednesday and friday, for keeping images updated with the official base Python images

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
- [TelegramBot-Webhook-Updates-Receiver-Service](https://github.com/David-Lor/TelegramBot-Webhook-Updates-Receiver-Service)

## Getting started

```bash
docker run -it --rm -e GIT_REPOSITORY="https://github.com/David-Lor/Python-HelloWorld.git" davidlor/python-git-app
```

## ENV Variables & ARGs

- `GIT_REPOSITORY`: URL of the remote Git repository to get the app from (required)
- `GIT_BRANCH`: set the Branch to clone from the Git repository (optional, default: use default branch)
- `APP_NAME`: name of your app. This name is given to the directory where project is cloned on(optional, default: _PythonApp_)
- (ARG) `USERNAME`: name of the user that is created on Dockerbuild to run the app with (optional, default: _user_)
- (ARG) `FROM_IMAGE`: base full image name to be used for the build (optional, default: _python:latest_)

Only required variable is (ENV) `GIT_REPOSITORY`.
The variables marked with (ARG) are [build-args](https://docs.docker.com/engine/reference/commandline/build/#set-build-time-variables---build-arg), used on image build.

If your Python script/app is CLI-based and requires to be called with arguments (for example `python . worker --instances=10`), you can provide them as Docker command arguments, like following:

```bash
docker run -it --rm -e GIT_REPOSITORY="https://github.com/David-Lor/Python-HelloWorld.git" -e GIT_BRANCH="args" davidlor/python-git-app worker --instances=10
# This command will clone an existing branch on the example repository, and print out the custom commands provided
```

## Available tags

- The tags available for the image are a limited selection of tags used in base images, such as the [official Python images](https://hub.docker.com/_/python/).
- The list of currently supported base images and output tags, used for periodic auto-builds, are available on the [images.json](images.json) file.
- Older images no longer supported may remain in [DockerHub](https://hub.docker.com/r/davidlor/python-git-app/tags?page=1&ordering=-last_updated).

## Building

If you want to build this image (required in order to change default username, base image tag or building
for unsupported architedtures), you must do on host machine:

- Clone this repository
- Build a new Docker image using the repository directory - you can optionally set these ARGs:
  - a custom username using the `USERNAME` ARG
  - a custom base image using the `FROM_IMAGE` ARG (example: `python:alpine` or `python:slim`)
- Create a new container, setting up the desired ENV variables

```bash
git clone https://github.com/David-Lor/Docker-Python-Autoclonable-App.git DockerPythonClonable
docker build DockerPythonClonable --build-arg USERNAME=user --build-arg FROM_IMAGE=python:slim -t yourname/yourtag:yourversion
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

## Caching requirements

The startup process of new containers may be lighten up by persisting the local cache (and even the installed libraries) in volumes.
This way, multiple containers, or the same container when being recreated for upgrading or reinstalling the running application, can skip the download and/or installing process.
The two directories that can be bind to volumes are:

- `/home/user/.cache`: cached libraries; mounting this volume will avoid downloading requirements
- `/home/user/.local`: installed libraries; mounting this volume will avoid installing requirements

**It is important that the mounted directories are owned by UID:GID 1000:1000**, since the container runs as a non-root user.

Example:

```bash
# Create the volumes, unless using binds
docker volume create pythongitapp-cache
docker volume create pythongitapp-local

# Change ownership
docker run -it --rm -v pythongitapp-local:/mnt/local -v pythongitapp-cache:/mnt/cache alpine sh -c "chown 1000:1000 /mnt/*"

# Run
docker run -it --rm -e GIT_REPOSITORY="https://github.com/David-Lor/Python-HelloWorld.git" -e GIT_BRANCH="fastapi" -v pythongitapp-local:/home/user/.local -v pythongitapp-cache:/home/user/.cache davidlor/python-git-app

# Ctrl+C to stop it (container will be removed)
# "docker run" again for verifying that requirements are not downloaded/installed again
```

## Useful Make utils

- `make test` - run tests (requires root/sudo & pytest)
- `make test USE_SUDO=0` - run tests without sudo (if current user is root or part of docker group)
- `make test-classic` - run tests sequentially (make test runs in parallel using pytest-xdist)
- `make test-install-requirements` - pip install test requirements
- `sudo make build FROM_IMAGE=python:slim TO_TAG=slim` - build the image with the `python:slim` base image, and tag as `python-git-app:slim`
- `sudo make build FROM_IMAGE=python:alpine TO_IMAGE=my-python:latest` - build the image with the `python:alpine` base image, and tag as `my-python:latest`

## Changelog

- 0.6.1
  - Exec Python on entrypoint to force PID=1
- 0.5.1
  - Add arm64 support for all images
  - Remove unsupported pyston armv7 arch
- 0.4.1:
  - Allow passing arguments to Python script/app (for example, for calling CLI-like apps)
- 0.3.1
  - Add new tags: pyston (based on [pyston/pyston](https://hub.docker.com/r/pyston/pyston)), pypy (based on [pypy](https://hub.docker.com/_/pypy))
  - Refactor tags.json into images.json, referencing complete source images, target tags and archs for each supported tag
  - Refactor multiple variables for new images.json format on Makefile, tests and workflow
- 0.2.4
  - Update Build-Test-Push workflow: reduce cron frequency to 3 days per week; only test&build when changing files involving the image
  - Add new workflows: Tag from PR, Update license year
- 0.2.3
  - Add new tags: slim-buster, rc, rc-buster, rc-slim, rc-slim-buster, rc-alpine, 3.9, 3.9-slim, 3.9-alpine, 3.8, 3.8-slim, 3.8-alpine, 3.7, 3.7-slim, 3.7-alpine, 3.6-slim
  - Delete tags: 3.7.9-buster, 3.7.9-alpine, 3.7-slim-stretch, 3.6-slim-stretch, 3.5-slim-stretch
- 0.2.2
    - Avoid triggering Github Workflow on tag push
    - Cache Docker builds on Github Workflow
    - Refactor Github Workflow for running "Test No-Build" and "Build&Push" jobs separately
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
- Allow disabling pip cache
- Allow running arbitrary command for app initialization
- Load SSH private key for cloning SSH git repositories (from path or secret)
- Run as root with an env variable - or another image tag
- Tag & upload images based on official Python image tags, plus versions of this repository
