# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a development container configuration project that provides a UBI8-based container with rootless Podman support for Coder workspaces. The project enables container-in-container development environments with proper security configurations.

## Architecture

The project consists of:

- **devcontainer.json**: VS Code devcontainer configuration with special security capabilities
- **Dockerfile**: UBI8-based image configuration with Podman setup and container-in-container compatibility
- The container runs as user `coder` (UID/GID 1000) with sudo access
- Podman is configured for rootless operation with VFS storage driver for KIND compatibility

## Key Container Features

- **Rootful Podman**: Configured to run as root via sudo wrapper to avoid user namespace issues in KIND
- **Container-in-container support**: Uses host networking and disabled user namespaces for compatibility
- **Security configurations**: Disabled seccomp and apparmor profiles for devcontainer use
- **Storage**: VFS driver for better compatibility with nested container scenarios
- **Runtime**: Uses `crun` as the container runtime

## Development Commands

Since this is a container configuration project, primary development involves:

- **Build the devcontainer**: Use VS Code's "Dev Containers: Rebuild Container" command
- **Test Podman functionality**: `podman --version` and `podman run hello-world`
- **Check container config**: Review files in `/etc/containers/` (system-level configuration)
- **Debug Podman setup**: `./debug-podman.sh` to see configuration and directory status
- **Test rootful mode**: `./test-rootful.sh` to verify Podman is running in rootful mode
- **Reset Podman storage**: `./reset-podman.sh` if storage issues occur
- **Force host networking**: `podman run --network host hello-world`

## Container Configuration Files

The Dockerfile creates system-level Podman configuration files:
- `/etc/containers/containers.conf`: Main Podman configuration (rootful mode)
- `/etc/containers/registries.conf`: Registry settings  
- `/etc/containers/storage.conf`: Storage configuration (VFS driver)

## Special Notes

- The container requires privileged capabilities (`SYS_ADMIN`, `NET_ADMIN`, `SETUID`, `SETGID`, `/dev/fuse`)
- Uses VFS storage driver instead of overlay for maximum compatibility
- Host networking is forced to avoid CNI plugin issues in KIND environments
- System container configurations are removed to prevent conflicts with user configurations

## Troubleshooting

### Common Issues in KIND Environments

**Storage overlay errors**: The container is configured to use VFS storage driver specifically to avoid overlay filesystem issues in nested container environments.

**Network bridge creation failures**: The container forces host networking and disables CNI networking entirely to prevent "operation not permitted" errors when creating bridge networks.

**FUSE device access**: The devcontainer.json includes `--device=/dev/fuse` to ensure proper device access for container operations.

**Storage location conflicts**: The configuration explicitly sets user-space storage locations and removes system configurations that might conflict.

**User namespace mapping failures**: In KIND environments, `newuidmap` often fails due to kernel limitations. The container now runs Podman in rootful mode (via sudo) with disabled user namespaces (`userns = ""`) to avoid these issues.

**Temporary directory issues**: Podman requires specific directory structures. The container ensures `/var/lib/containers/storage` (graphroot) and `/run/containers/storage` (runroot) directories exist with proper permissions for rootful operation.

**System migration errors**: The configuration includes `podman system migrate` during initialization to properly set up Podman's internal database and avoid "invalid internal status" errors. The container now uses system-level configuration (`/etc/containers/`) instead of user-space configuration to avoid conflicts between rootful and rootless modes.

**Podman command not found**: If `podman` command is not found, the wrapper script creation may have failed. Use `./debug-podman.sh` to check if `/usr/bin/podman` and `/usr/bin/podman-original` exist. The container build process includes verification steps to ensure the wrapper is created properly.

**Duplicate storage configuration errors**: If you see "Key 'storage' has already been defined" errors, this indicates corrupted configuration files. The container now properly separates the creation of `containers.conf` and `storage.conf` files. Use `./reset-podman.sh` to recreate clean configuration files if needed.

**Cgroup filesystem errors**: In nested container environments like KIND, cgroup management can be problematic. The configuration uses `cgroup_manager = "none"` to completely bypass cgroup management and resource limiting. This allows containers to run without requiring systemd or complex cgroup filesystem setup. While this disables resource constraints, it's the most reliable approach for development containers in KIND environments.