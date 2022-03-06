ARG FROM_IMAGE=python:latest
FROM ${FROM_IMAGE}

# ENV variables
ENV GIT_REPOSITORY="" \
    APP_NAME="App" \
    GIT_BRANCH=""
ARG USERNAME=user

# Add a non-root user
RUN useradd -ms /bin/bash ${USERNAME} || (addgroup ${USERNAME} && adduser ${USERNAME} -D -G ${USERNAME})

# Install git if not installed
RUN which git || ((apt-get -yq update && apt-get -yq install git && rm -rf /var/lib/apt/lists/*) || (apk update --no-cache && apk add --no-cache git))

# Change user and working directory
USER ${USERNAME}
WORKDIR /home/${USERNAME}

# Copy scripts
COPY --chown=${USERNAME}:${USERNAME} scripts/* ./scripts/
RUN chmod +x ./scripts/entrypoint.sh

# Run entrypoint as default command
ENTRYPOINT ["./scripts/entrypoint.sh"]
