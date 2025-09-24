# Minimal UBI8 Base Image with Buildah for Coder Workspaces
FROM registry.access.redhat.com/ubi8/ubi:latest

LABEL maintainer="Coder Workspace" \
      description="Minimal UBI8 image with Buildah for container building" \
      version="2.0-minimal"

# Set environment variables
ENV USER=coder \
    HOME=/home/coder \
    XDG_RUNTIME_DIR=/home/coder/.local/share/containers/runroot \
    BUILDAH_ISOLATION=chroot

# Create coder user with specific UID/GID for consistency
RUN useradd -m -s /bin/bash -u 1000 coder && \
    echo "coder ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Install minimal required packages only (exactly matching template)
RUN dnf update -y && \
    dnf install -y \
        git \
        curl \
        buildah \
        fuse-overlayfs \
        slirp4netns \
        procps-ng \
    && dnf clean all

# Configure subuid and subgid for rootless containers
RUN echo "coder:100000:65536" >> /etc/subuid && \
    echo "coder:100000:65536" >> /etc/subgid && \
    chmod 644 /etc/subuid /etc/subgid

# Create necessary directories for coder user
RUN mkdir -p /home/coder/.config/containers && \
    mkdir -p /home/coder/.local/share/containers/{storage,runroot} && \
    chown -R coder:coder /home/coder

# Configure Buildah for the coder user
USER coder
WORKDIR /home/coder

# Create Buildah configuration files
RUN mkdir -p ~/.config/containers

# Configure containers.conf for Buildah (minimal - matching template)
RUN echo '[containers]' > ~/.config/containers/containers.conf && \
    echo 'netns = "host"' >> ~/.config/containers/containers.conf && \
    echo 'userns = "host"' >> ~/.config/containers/containers.conf

# Configure registries.conf
RUN echo '[registries.search]' > ~/.config/containers/registries.conf && \
    echo "registries = ['registry.access.redhat.com', 'registry.redhat.io', 'docker.io', 'quay.io']" >> ~/.config/containers/registries.conf && \
    echo '' >> ~/.config/containers/registries.conf && \
    echo '[registries.insecure]' >> ~/.config/containers/registries.conf && \
    echo 'registries = []' >> ~/.config/containers/registries.conf && \
    echo '' >> ~/.config/containers/registries.conf && \
    echo '[registries.block]' >> ~/.config/containers/registries.conf && \
    echo 'registries = []' >> ~/.config/containers/registries.conf

# Configure storage.conf for VFS driver and ignore chown errors
RUN echo '[storage]' > ~/.config/containers/storage.conf && \
    echo 'driver = "vfs"' >> ~/.config/containers/storage.conf && \
    echo '[storage.options]' >> ~/.config/containers/storage.conf && \
    echo 'ignore_chown_errors = "true"' >> ~/.config/containers/storage.conf

# Configure Buildah policy (minimal - matching template)
RUN echo '{' > ~/.config/containers/policy.json && \
    echo '    "default": [{"type": "insecureAcceptAnything"}]' >> ~/.config/containers/policy.json && \
    echo '}' >> ~/.config/containers/policy.json

# Set up minimal shell environment
RUN echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc && \
    echo 'export XDG_RUNTIME_DIR=/home/coder/.local/share/containers/runroot' >> ~/.bashrc && \
    echo 'export BUILDAH_ISOLATION=chroot' >> ~/.bashrc

# Install code-server for VS Code in browser
RUN curl -fsSL https://code-server.dev/install.sh | sh -s -- --method=standalone --prefix=/home/coder/.local

# Create a minimal welcome script
RUN echo '#!/bin/bash' > ~/welcome-buildah.sh && \
    echo 'echo "🎉 UBI8 + Buildah workspace ready!"' >> ~/welcome-buildah.sh && \
    echo 'echo "📦 Installed: Buildah $(buildah --version | head -1)"' >> ~/welcome-buildah.sh && \
    echo 'echo "📍 Example: buildah from registry.access.redhat.com/ubi8/ubi:latest"' >> ~/welcome-buildah.sh

RUN chmod +x ~/welcome-buildah.sh

# Verify Buildah installation
RUN buildah --version

# Set working directory and default user
WORKDIR /home/coder
USER coder

# Default command
CMD ["/bin/bash"]
