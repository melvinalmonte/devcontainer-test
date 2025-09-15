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

# Create Podman configuration script (runtime configuration like the working template)
RUN cat > /usr/local/bin/setup-podman.sh << 'EOF'
#!/bin/bash
set -e

echo "🐳 Configuring Podman for Kubernetes environment..."

# Create podman configuration directory
mkdir -p /home/coder/.config/containers

# Configure Podman for KIND compatibility
cat > /home/coder/.config/containers/containers.conf << 'PODMAN_CONF'
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
PODMAN_CONF

# Configure registries for Podman
cat > /home/coder/.config/containers/registries.conf << 'REG_CONF'
[registries.search]
registries = ['docker.io', 'quay.io']

[registries.insecure]
registries = []

[registries.block]
registries = []
REG_CONF

# Configure storage for Podman (KIND-compatible configuration)
cat > /home/coder/.config/containers/storage.conf << 'STORAGE_CONF'
[storage]
driver = "vfs"
runroot = "/home/coder/.local/share/containers/runroot"
graphroot = "/home/coder/.local/share/containers/storage"

[storage.options]
# Use VFS driver for KIND compatibility (slower but more reliable)
STORAGE_CONF

# Create necessary directories and set ownership
mkdir -p /home/coder/.local/share/containers/{storage,runroot}
chown -R coder:coder /home/coder/.config
chown -R coder:coder /home/coder/.local

# Reset Podman storage to ensure clean state (like the working template)
echo "🔧 Resetting Podman storage for clean initialization..."
rm -rf /home/coder/.local/share/containers/storage
mkdir -p /home/coder/.local/share/containers/{storage,runroot}
chown -R coder:coder /home/coder/.local

echo "✅ Podman configuration completed"
EOF

RUN chmod +x /usr/local/bin/setup-podman.sh

# Set environment variables for Podman
ENV XDG_RUNTIME_DIR="/home/coder/.local/share/containers/runroot"

# Create a wrapper script for Podman that ensures proper setup
RUN mv /usr/bin/podman /usr/bin/podman-original && \
    cat > /usr/bin/podman << 'WRAPPER_EOF'
#!/bin/bash
# Ensure Podman is configured before first use
if [ ! -f /home/coder/.config/containers/containers.conf ]; then
    /usr/local/bin/setup-podman.sh
fi
exec sudo /usr/bin/podman-original "$@"
WRAPPER_EOF
RUN chmod +x /usr/bin/podman

# Switch to coder user
USER coder
WORKDIR /home/coder

# Verify Podman installation
RUN podman --version

# Set default command
CMD ["/bin/bash"]