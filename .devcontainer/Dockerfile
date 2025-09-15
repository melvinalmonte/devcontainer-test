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

# Create Podman configuration script (using echo commands for better compatibility)
RUN echo '#!/bin/bash' > /usr/local/bin/setup-podman.sh && \
    echo 'echo "🐳 Configuring Podman for Kubernetes environment..."' >> /usr/local/bin/setup-podman.sh && \
    echo 'mkdir -p /home/coder/.config/containers' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "[containers]" > /home/coder/.config/containers/containers.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "userns = \"\"" >> /home/coder/.config/containers/containers.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "netns = \"host\"" >> /home/coder/.config/containers/containers.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "seccomp_profile = \"\"" >> /home/coder/.config/containers/containers.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "apparmor_profile = \"\"" >> /home/coder/.config/containers/containers.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "default_sysctls = []" >> /home/coder/.config/containers/containers.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "" >> /home/coder/.config/containers/containers.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "[engine]" >> /home/coder/.config/containers/containers.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "cgroup_manager = \"cgroupfs\"" >> /home/coder/.config/containers/containers.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "events_logger = \"file\"" >> /home/coder/.config/containers/containers.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "runtime = \"crun\"" >> /home/coder/.config/containers/containers.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "runtime_supports_json = [\"crun\"]" >> /home/coder/.config/containers/containers.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "[registries.search]" > /home/coder/.config/containers/registries.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "registries = ['"'"'docker.io'"'"', '"'"'quay.io'"'"']" >> /home/coder/.config/containers/registries.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "" >> /home/coder/.config/containers/registries.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "[registries.insecure]" >> /home/coder/.config/containers/registries.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "registries = []" >> /home/coder/.config/containers/registries.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "" >> /home/coder/.config/containers/registries.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "[registries.block]" >> /home/coder/.config/containers/registries.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "registries = []" >> /home/coder/.config/containers/registries.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "[storage]" > /home/coder/.config/containers/storage.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "driver = \"vfs\"" >> /home/coder/.config/containers/storage.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "runroot = \"/home/coder/.local/share/containers/runroot\"" >> /home/coder/.config/containers/storage.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "graphroot = \"/home/coder/.local/share/containers/storage\"" >> /home/coder/.config/containers/storage.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "" >> /home/coder/.config/containers/storage.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "[storage.options]" >> /home/coder/.config/containers/storage.conf' >> /usr/local/bin/setup-podman.sh && \
    echo 'mkdir -p /home/coder/.local/share/containers/{storage,runroot}' >> /usr/local/bin/setup-podman.sh && \
    echo 'chown -R coder:coder /home/coder/.config' >> /usr/local/bin/setup-podman.sh && \
    echo 'chown -R coder:coder /home/coder/.local' >> /usr/local/bin/setup-podman.sh && \
    echo 'rm -rf /home/coder/.local/share/containers/storage' >> /usr/local/bin/setup-podman.sh && \
    echo 'mkdir -p /home/coder/.local/share/containers/{storage,runroot}' >> /usr/local/bin/setup-podman.sh && \
    echo 'chown -R coder:coder /home/coder/.local' >> /usr/local/bin/setup-podman.sh && \
    echo 'echo "✅ Podman configuration completed"' >> /usr/local/bin/setup-podman.sh && \
    chmod +x /usr/local/bin/setup-podman.sh

# Set environment variables for Podman
ENV XDG_RUNTIME_DIR="/home/coder/.local/share/containers/runroot"

# Create a wrapper script for Podman that ensures proper setup
RUN mv /usr/bin/podman /usr/bin/podman-original && \
    echo '#!/bin/bash' > /usr/bin/podman && \
    echo 'if [ ! -f /home/coder/.config/containers/containers.conf ]; then' >> /usr/bin/podman && \
    echo '    /usr/local/bin/setup-podman.sh' >> /usr/bin/podman && \
    echo 'fi' >> /usr/bin/podman && \
    echo 'exec sudo /usr/bin/podman-original "$@"' >> /usr/bin/podman && \
    chmod +x /usr/bin/podman

# Switch to coder user
USER coder
WORKDIR /home/coder

# Verify Podman installation
RUN podman --version

# Set default command
CMD ["/bin/bash"]