# UBI8-based image with rootless Podman for Coder workspaces
FROM registry.access.redhat.com/ubi8/ubi:latest

# Set labels
LABEL maintainer="Coder Template" \
      description="UBI8 with rootless Podman for development workspaces" \
      version="1.0"

# Create coder user with proper UID/GID for Kubernetes
RUN useradd -m -u 1000 -g 1000 -s /bin/bash coder

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
RUN cat > /home/coder/.config/containers/containers.conf << EOF
[containers]
# Disable user namespaces for KIND compatibility
userns = ""
# Use host networking by default to avoid network namespace issues
netns = "host"
# Disable seccomp and apparmor for KIND compatibility
seccomp_profile = ""
apparmor_profile = ""
# Add default security options for container execution
default_sysctls = []

[engine]
# Disable some features that may not work in KIND
cgroup_manager = "cgroupfs"
events_logger = "file"
runtime = "crun"
# Add default runtime options for easier container execution in KIND
runtime_supports_json = ["crun"]
EOF

# Configure registries for Podman
RUN cat > /home/coder/.config/containers/registries.conf << EOF
[registries.search]
registries = ['docker.io', 'quay.io', 'registry.redhat.io']

[registries.insecure]
registries = []

[registries.block]
registries = []
EOF

# Configure storage for Podman (KIND-compatible configuration)
RUN cat > /home/coder/.config/containers/storage.conf << EOF
[storage]
driver = "vfs"
runroot = "/home/coder/.local/share/containers/runroot"
graphroot = "/home/coder/.local/share/containers/storage"

[storage.options]
# Use VFS driver for KIND compatibility (slower but more reliable)
EOF

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