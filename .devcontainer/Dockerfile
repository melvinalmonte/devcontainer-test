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

# Create necessary directories for Podman
RUN mkdir -p /home/coder/.config/containers && \
    mkdir -p /home/coder/.local/share/containers/{storage,runroot}

# Configure Podman for KIND/container compatibility
RUN echo '[containers]' > /home/coder/.config/containers/containers.conf && \
    echo '# Disable user namespaces for KIND compatibility' >> /home/coder/.config/containers/containers.conf && \
    echo 'userns = ""' >> /home/coder/.config/containers/containers.conf && \
    echo '# Use host networking by default to avoid network namespace issues' >> /home/coder/.config/containers/containers.conf && \
    echo 'netns = "host"' >> /home/coder/.config/containers/containers.conf && \
    echo '# Disable seccomp and apparmor for KIND compatibility' >> /home/coder/.config/containers/containers.conf && \
    echo 'seccomp_profile = ""' >> /home/coder/.config/containers/containers.conf && \
    echo 'apparmor_profile = ""' >> /home/coder/.config/containers/containers.conf && \
    echo '# Add default security options for container execution' >> /home/coder/.config/containers/containers.conf && \
    echo 'default_sysctls = []' >> /home/coder/.config/containers/containers.conf && \
    echo '' >> /home/coder/.config/containers/containers.conf && \
    echo '[engine]' >> /home/coder/.config/containers/containers.conf && \
    echo '# Disable some features that may not work in KIND' >> /home/coder/.config/containers/containers.conf && \
    echo 'cgroup_manager = "cgroupfs"' >> /home/coder/.config/containers/containers.conf && \
    echo 'events_logger = "file"' >> /home/coder/.config/containers/containers.conf && \
    echo 'runtime = "crun"' >> /home/coder/.config/containers/containers.conf && \
    echo '# Add default runtime options for easier container execution in KIND' >> /home/coder/.config/containers/containers.conf && \
    echo 'runtime_supports_json = ["crun"]' >> /home/coder/.config/containers/containers.conf

# Configure registries for Podman
RUN echo '[registries.search]' > /home/coder/.config/containers/registries.conf && \
    echo "registries = ['docker.io', 'quay.io', 'registry.redhat.io']" >> /home/coder/.config/containers/registries.conf && \
    echo '' >> /home/coder/.config/containers/registries.conf && \
    echo '[registries.insecure]' >> /home/coder/.config/containers/registries.conf && \
    echo 'registries = []' >> /home/coder/.config/containers/registries.conf && \
    echo '' >> /home/coder/.config/containers/registries.conf && \
    echo '[registries.block]' >> /home/coder/.config/containers/registries.conf && \
    echo 'registries = []' >> /home/coder/.config/containers/registries.conf

# Configure storage for Podman (KIND-compatible configuration)
RUN echo '[storage]' > /home/coder/.config/containers/storage.conf && \
    echo 'driver = "vfs"' >> /home/coder/.config/containers/storage.conf && \
    echo 'runroot = "/home/coder/.local/share/containers/runroot"' >> /home/coder/.config/containers/storage.conf && \
    echo 'graphroot = "/home/coder/.local/share/containers/storage"' >> /home/coder/.config/containers/storage.conf && \
    echo '' >> /home/coder/.config/containers/storage.conf && \
    echo '[storage.options]' >> /home/coder/.config/containers/storage.conf && \
    echo '# Use VFS driver for KIND compatibility (slower but more reliable)' >> /home/coder/.config/containers/storage.conf

# Set proper ownership for all coder user files
RUN chown -R coder:coder /home/coder/.config && \
    chown -R coder:coder /home/coder/.local

# Set environment variables for Podman
ENV XDG_RUNTIME_DIR="/home/coder/.local/share/containers/runroot"

# Switch to coder user
USER coder
WORKDIR /home/coder

# Verify Podman installation
RUN podman --version

# Set default command
CMD ["/bin/bash"]