  FROM ubuntu

  RUN apt-get update
  RUN apt-get install vim sudo curl wget git -y

  # Install Go
  RUN wget -O go.tar.gz https://go.dev/dl/go1.21.5.linux-amd64.tar.gz && \
      tar -C /usr/local -xzf go.tar.gz && \
      rm go.tar.gz

  # Add Go to PATH for all users
  RUN echo 'export PATH=$PATH:/usr/local/go/bin' >> /etc/environment
  RUN echo 'export PATH=$PATH:/usr/local/go/bin' >> /etc/bash.bashrc

  RUN useradd -m -s /bin/bash -G sudo coder

  # Let's add a fancy prompt and Go PATH for coder user
  RUN echo "PS1='🐳 \[\033[1;36m\]\h \[\033[1;34m\]\W\[\033[0;35m\] \[\033[1;36m\]# \[\033[0m\]'" > /home/coder/.bashrc && \
      echo 'export PATH=$PATH:/usr/local/go/bin' >> /home/coder/.bashrc && \
      echo 'export GOPATH=$HOME/go' >> /home/coder/.bashrc && \
      echo 'export PATH=$PATH:$GOPATH/bin' >> /home/coder/.bashrc && \
      chown coder:coder /home/coder/.bashrc

  USER coder