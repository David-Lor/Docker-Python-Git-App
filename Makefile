.DEFAULT_GOAL := help

USERNAME := "user"
BASE_TAG := "latest"
IMAGE_TAG := "$(shell cat tools/built_image_name.txt):$BASE_TAG"
PUSH_IMAGE_TAG := "davidlor/python-git-app:$BASE_TAG"

build: ## build the image. env variables: USERNAME, BASE_TAG, IMAGE_TAG
	docker build . \
		--build-arg USERNAME=${USERNAME} \
		--build-arg BASE_TAG=${BASE_TAG} \
		-t ${IMAGE_TAG}

test: ## run tests in parallel
	pytest -sv -n auto tools/tests

test-classic: ## run tests sequentially (without parallelization)
	pytest -sv tools/tests

test-build: ## run build tests in parallel
	pytest -sv -n auto tools/tests/test_build.py

test-build-classic: ## run build tests sequentially (without parallelization)
	pytest -sv tools/tests/test_build.py

test-nobuild: ## run non-build tests in parallel
	pytest -sv -n auto tools/tests --ignore=test_build.py

test-nobuild-classic: ## run non-build tests sequentially (without parallelization)
	pytest -sv tools/tests --ignore=test_build.py

test-install-requirements: ## pip install requirements for tests
	pip install -r tools/tests/requirements.txt

push: ## push built image to dockerhub
	docker tag ${IMAGE_TAG} ${PUSH_IMAGE_TAG}
	docker push ${PUSH_IMAGE_TAG}

help: ## show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
