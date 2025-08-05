FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    vim \
    sudo \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create user with sudo privileges
RUN useradd -m -s /bin/bash -G sudo coder && \
    echo 'coder ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Set up fancy prompt and useful aliases
RUN echo "PS1='🐳 \[\033[1;36m\]\h \[\033[1;34m\]\W\[\033[0;35m\] \[\033[1;36m\]$ \[\033[0m\]'" > /home/coder/.bashrc && \
    echo "alias ll='ls -la'" >> /home/coder/.bashrc && \
    echo "alias python=python3" >> /home/coder/.bashrc && \
    echo "alias pip=pip3" >> /home/coder/.bashrc && \
    chown coder:coder /home/coder/.bashrc

# Set working directory
WORKDIR /workspace

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Switch to non-root user
USER coder