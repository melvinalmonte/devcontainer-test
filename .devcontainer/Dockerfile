# UBI8-based image with rootless Podman for Coder workspaces
FROM registry.access.redhat.com/ubi8/ubi:latest

# Set labels
LABEL maintainer="Coder Template" \
      description="UBI8 with rootless Podman for development workspaces" \
      version="1.0"

# Create coder user with proper UID/GID for Kubernetes
RUN groupadd -g 1000 coder && \
    useradd -m -u 1000 -g 1000 -s /bin/bash coder

# Install required packages
RUN dnf update -y && \
    dnf install -y \
        podman \
        crun \
        fuse-overlayfs \
        curl \
        git \
        sudo \
        which \
        procps-ng \
        shadow-utils && \
    dnf clean all

# Configure subuid and subgid for rootless operation
RUN echo "coder:100000:65536" >> /etc/subuid && \
    echo "coder:100000:65536" >> /etc/subgid && \
    chmod 644 /etc/subuid /etc/subgid

# Configure sudo for coder user (needed for some operations)
RUN echo "coder ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Configure registries for system-level Podman
RUN echo '[registries.search]' > /etc/containers/registries.conf && \
    echo "registries = ['docker.io', 'quay.io', 'registry.redhat.io']" >> /etc/containers/registries.conf && \
    echo '' >> /etc/containers/registries.conf && \
    echo '[registries.insecure]' >> /etc/containers/registries.conf && \
    echo 'registries = []' >> /etc/containers/registries.conf && \
    echo '' >> /etc/containers/registries.conf && \
    echo '[registries.block]' >> /etc/containers/registries.conf && \
    echo 'registries = []' >> /etc/containers/registries.conf

# Set environment variables for Podman (rootful mode uses system locations)
ENV TMPDIR="/tmp"

# Create necessary system directories for Podman
RUN mkdir -p /var/lib/containers/storage && \
    mkdir -p /run/containers/storage && \
    chmod 1777 /tmp && \
    chmod 755 /var/lib/containers && \
    chmod 755 /run/containers

# Create a wrapper script for Podman to run as root
RUN if [ -f /usr/bin/podman ]; then \
        mv /usr/bin/podman /usr/bin/podman-original; \
    else \
        echo "Warning: /usr/bin/podman not found, looking for alternatives..."; \
        find /usr -name "*podman*" -type f 2>/dev/null || true; \
    fi && \
    echo '#!/bin/bash' > /usr/bin/podman && \
    echo '# Ensure required directories exist for rootful Podman' >> /usr/bin/podman && \
    echo 'sudo mkdir -p /var/lib/containers/storage /run/containers/storage' >> /usr/bin/podman && \
    echo 'sudo chmod 1777 /tmp' >> /usr/bin/podman && \
    echo '# Run Podman as root' >> /usr/bin/podman && \
    echo 'exec sudo /usr/bin/podman-original "$@"' >> /usr/bin/podman && \
    chmod +x /usr/bin/podman

# Create system-level Podman configuration for rootful mode
RUN mkdir -p /etc/containers && \
    echo '[containers]' > /etc/containers/containers.conf && \
    echo 'netns = "host"' >> /etc/containers/containers.conf && \
    echo 'userns = ""' >> /etc/containers/containers.conf && \
    echo 'seccomp_profile = ""' >> /etc/containers/containers.conf && \
    echo 'apparmor_profile = ""' >> /etc/containers/containers.conf && \
    echo 'default_network = "host"' >> /etc/containers/containers.conf && \
    echo 'network_backend = "none"' >> /etc/containers/containers.conf && \
    echo '' >> /etc/containers/containers.conf && \
    echo '[engine]' >> /etc/containers/containers.conf && \
    echo 'cgroup_manager = "cgroupfs"' >> /etc/containers/containers.conf && \
    echo 'events_logger = "file"' >> /etc/containers/containers.conf && \
    echo 'runtime = "crun"' >> /etc/containers/containers.conf && \
    echo '' >> /etc/containers/containers.conf && \
    echo '[storage]' >> /etc/containers/storage.conf && \
    echo 'driver = "vfs"' >> /etc/containers/storage.conf && \
    echo 'runroot = "/run/containers/storage"' >> /etc/containers/storage.conf && \
    echo 'graphroot = "/var/lib/containers/storage"' >> /etc/containers/storage.conf

# Switch to coder user
USER coder
WORKDIR /home/coder

# Create debugging and helper scripts
RUN echo '#!/bin/bash' > /home/coder/debug-podman.sh && \
    echo 'echo "=== Podman Debug Information ==="' >> /home/coder/debug-podman.sh && \
    echo 'echo "User: $(whoami)"' >> /home/coder/debug-podman.sh && \
    echo 'echo "Podman wrapper location:"' >> /home/coder/debug-podman.sh && \
    echo 'ls -la /usr/bin/podman* 2>/dev/null || echo "No podman binaries found in /usr/bin/"' >> /home/coder/debug-podman.sh && \
    echo 'echo "Podman version (if available):"' >> /home/coder/debug-podman.sh && \
    echo 'if [ -f /usr/bin/podman-original ]; then' >> /home/coder/debug-podman.sh && \
    echo '    sudo /usr/bin/podman-original --version 2>/dev/null || echo "Failed to get version from podman-original"' >> /home/coder/debug-podman.sh && \
    echo 'elif [ -f /usr/bin/podman ]; then' >> /home/coder/debug-podman.sh && \
    echo '    /usr/bin/podman --version 2>/dev/null || echo "Failed to get version from podman wrapper"' >> /home/coder/debug-podman.sh && \
    echo 'else' >> /home/coder/debug-podman.sh && \
    echo '    echo "No podman binary found"' >> /home/coder/debug-podman.sh && \
    echo 'fi' >> /home/coder/debug-podman.sh && \
    echo 'echo "Directory structure:"' >> /home/coder/debug-podman.sh && \
    echo 'ls -la /var/lib/containers/ 2>/dev/null || echo "/var/lib/containers/ not found"' >> /home/coder/debug-podman.sh && \
    echo 'ls -la /run/containers/ 2>/dev/null || echo "/run/containers/ not found"' >> /home/coder/debug-podman.sh && \
    echo 'ls -la /etc/containers/ 2>/dev/null || echo "/etc/containers/ not found"' >> /home/coder/debug-podman.sh && \
    echo 'echo "PATH: $PATH"' >> /home/coder/debug-podman.sh && \
    chmod +x /home/coder/debug-podman.sh

RUN echo '#!/bin/bash' > /home/coder/reset-podman.sh && \
    echo 'echo "Resetting Podman storage and reinitializing..."' >> /home/coder/reset-podman.sh && \
    echo 'sudo rm -rf /var/lib/containers/storage/* 2>/dev/null || true' >> /home/coder/reset-podman.sh && \
    echo 'sudo rm -rf /run/containers/storage/* 2>/dev/null || true' >> /home/coder/reset-podman.sh && \
    echo 'sudo mkdir -p /var/lib/containers/storage /run/containers/storage' >> /home/coder/reset-podman.sh && \
    echo 'sudo /usr/bin/podman-original system reset --force 2>/dev/null || true' >> /home/coder/reset-podman.sh && \
    echo 'sudo /usr/bin/podman-original system migrate 2>/dev/null || true' >> /home/coder/reset-podman.sh && \
    echo 'echo "Podman storage reset and migration complete"' >> /home/coder/reset-podman.sh && \
    chmod +x /home/coder/reset-podman.sh

# Verify Podman installation and wrapper
RUN echo "Checking Podman installation..." && \
    ls -la /usr/bin/podman* && \
    cat /usr/bin/podman && \
    echo "Testing Podman wrapper..." && \
    /usr/bin/podman --version || echo "Podman wrapper test failed"

# Initialize Podman storage with proper migration
RUN sudo /usr/bin/podman-original system migrate 2>/dev/null || true

# Set default command
CMD ["/bin/bash"]