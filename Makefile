.DEFAULT_GOAL := help

USERNAME := "user"
FROM_IMAGE := "python:latest"
TO_TAG := "latest"
TO_IMAGE := "python-git-app:$(TO_TAG)"
PUSH_IMAGE := "davidlor/python-git-app:$(TO_TAG)"
BUILDX_PUSH := "false"
ARCH := "amd64"

build: ## build the image. env variables: USERNAME, FROM_IMAGE, TO_TAG/TO_IMAGE
	docker build . --pull \
		--build-arg USERNAME=${USERNAME} \
		--build-arg FROM_IMAGE=${FROM_IMAGE} \
		-t ${TO_IMAGE}

buildx: ## build the image with docker buildx; push optionally. env variables: USERNAME, FROM_IMAGE, TO_TAG/TO_IMAGE, ARCH, BUILDX_PUSH
	docker buildx build . --file=./Dockerfile --pull \
		--build-arg USERNAME=${USERNAME} \
		--build-arg FROM_IMAGE=${FROM_IMAGE} \
		--platform=${ARCH} \
		--tag=${PUSH_IMAGE} \
		--output type=image,push=${BUILDX_PUSH}

test: ## run tests in parallel
	pytest -sv -n auto tools/tests

test-classic: ## run tests sequentially (without parallelization)
	pytest -sv tools/tests

test-build: ## run build tests in parallel
	pytest -sv -n auto tools/tests/test_build.py

test-build-classic: ## run build tests sequentially (without parallelization)
	pytest -sv tools/tests/test_build.py

test-nobuild: ## run non-build tests in parallel
	pytest -sv -n auto tools/tests --ignore=tools/tests/test_build.py

test-nobuild-classic: ## run non-build tests sequentially (without parallelization)
	pytest -sv tools/tests --ignore=tools/tests/test_build.py

test-install-requirements: ## pip install requirements for tests
	pip install -r tools/tests/requirements.txt

push: ## push built image to dockerhub
	docker tag ${TO_IMAGE} ${PUSH_IMAGE}
	docker push ${PUSH_IMAGE}

pull-base: ## pull base image from dockerhub
	docker pull ${FROM_IMAGE}

help: ## show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
