.DEFAULT_GOAL := help

USERNAME := "user"
BASE_TAG := "latest"
IMAGE_NAME := "$(shell cat tools/built_image_name.txt):$(BASE_TAG)"
PUSH_IMAGE_NAME := "davidlor/python-git-app:$(BASE_TAG)"

build: ## build the image. env variables: USERNAME, BASE_TAG, IMAGE_TAG
	docker build . \
		--build-arg USERNAME=${USERNAME} \
		--build-arg BASE_TAG=${BASE_TAG} \
		-t ${IMAGE_NAME}

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
	docker tag ${IMAGE_NAME} ${PUSH_IMAGE_NAME}
	docker push ${PUSH_IMAGE_NAME}

generate-ssh-key: ## create a new public and private key set in current directory
	ssh-keygen -b 2048 -t rsa -f ./ssh_key -q -N ""
	mv ./ssh_key ./ssh_key.pem

help: ## show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
