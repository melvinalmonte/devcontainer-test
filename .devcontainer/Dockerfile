# Use Ubuntu as base image
FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install essential packages
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    unzip \
    build-essential \
    python3 \
    python3-pip \
    nodejs \
    npm \
    openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

# Install Go
ARG GO_VERSION=1.21.7
RUN curl -fsSL https://golang.org/dl/go${GO_VERSION}.linux-amd64.tar.gz | tar -xzC /usr/local \
    && ln -s /usr/local/go/bin/go /usr/local/bin/go \
    && ln -s /usr/local/go/bin/gofmt /usr/local/bin/gofmt

# Create directory for pre-downloaded VS Code extensions
RUN mkdir -p /opt/vscode-extensions

# Download VS Code extensions and save them in the container
WORKDIR /opt/vscode-extensions

# Python extensions
RUN curl -L -o python.vsix "https://open-vsx.org/api/ms-python/python/2025.4.0/file/ms-python.python-2025.4.0.vsix"
RUN curl -L -o pylint.vsix "https://open-vsx.org/api/ms-python/pylint/2024.2.0/file/ms-python.pylint-2024.2.0.vsix"
RUN curl -L -o black.vsix "https://open-vsx.org/api/ms-python/black-formatter/2024.6.0/file/ms-python.black-formatter-2024.6.0.vsix"
RUN curl -L -o jupyter.vsix "https://open-vsx.org/api/ms-toolsai/jupyter/2025.7.0/file/ms-toolsai.jupyter-2025.7.0.vsix"

# Java extensions
RUN curl -L -o java.vsix "https://open-vsx.org/api/redhat/java/1.45.2025081408/file/redhat.java-1.45.2025081408.vsix"
RUN curl -L -o java-debug.vsix "https://open-vsx.org/api/vscjava/vscode-java-debug/0.58.2/file/vscjava.vscode-java-debug-0.58.2.vsix"
RUN curl -L -o java-test.vsix "https://open-vsx.org/api/vscjava/vscode-java-test/0.43.1/file/vscjava.vscode-java-test-0.43.1.vsix"
RUN curl -L -o maven.vsix "https://open-vsx.org/api/vscjava/vscode-maven/0.44.0/file/vscjava.vscode-maven-0.44.0.vsix"

# Go extensions
RUN curl -L -o go.vsix "https://open-vsx.org/api/golang/Go/0.48.0/file/golang.Go-0.48.0.vsix"

# General purpose extensions
RUN curl -L -o terraform.vsix "https://open-vsx.org/api/hashicorp/terraform/web/2.34.5/file/hashicorp.terraform-2.34.5@web.vsix"
RUN curl -L -o gitlab.vsix "https://open-vsx.org/api/GitLab/gitlab-workflow/6.36.0/file/GitLab.gitlab-workflow-6.36.0.vsix"

# Verify downloaded extensions exist
RUN ls -la /opt/vscode-extensions/

# Set workspace folder
WORKDIR /workspace

# Add Go to PATH
ENV PATH="/usr/local/go/bin:${PATH}"

# Create a non-root user (following security best practices)
RUN groupadd --gid 1000 vscode \
    && useradd --uid 1000 --gid 1000 -m vscode \
    && chown -R vscode:vscode /opt/vscode-extensions

USER vscode