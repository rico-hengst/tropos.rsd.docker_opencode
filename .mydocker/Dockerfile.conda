# Dockerfile for Python project analysis with opencode
FROM continuumio/anaconda3:latest

# Get key during build and store to ENV
ARG SAIA_API_KEY
ENV SAIA_API_KEY=${SAIA_API_KEY}

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/conda/bin:${PATH}"
ENV CONDA_ENV_NAME="py3.11_docker"
ENV CONDA_ENV_FILE="environment.yml"

# Install basic utilities
RUN apt-get update && apt-get install -y \
    curl \
    git \
    sudo \
    vim \
    nano \
    build-essential \
    linux-headers-generic \
    && rm -rf /var/lib/apt/lists/*

# Create user "user" with sudo privileges FIRST
RUN useradd -m -s /bin/bash user \
    && echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
    && chown -R user:user /opt/conda

# Switch to user
USER user
WORKDIR /home/user

# Copy environment.yml file
ARG ENV_FILE=environment.yml
COPY --chown=user:user ${ENV_FILE} /home/user/environment.yml

# Create conda environment from environment.yml
RUN conda env create -f /home/user/environment.yml --name py3.11_docker 

# Add conda initialization to .bashrc for interactive shells
RUN echo 'source /opt/conda/etc/profile.d/conda.sh' >> /home/user/.bashrc \
    && echo 'conda activate py3.11_docker' >> /home/user/.bashrc

# RUN conda activate py3.11_docker

# Install opencode
RUN curl -fsSL https://opencode.ai/v2/install | bash

# Add opencode to PATH
ENV PATH="/home/user/.opencode/bin:${PATH}"

# Create workspace directory using sudo
RUN sudo mkdir -p /workspace && sudo chown -R user:user /workspace

# Create entrypoint script that activates conda environment
RUN echo '#!/bin/bash\n\
source /opt/conda/etc/profile.d/conda.sh\n\
conda activate py3.11_docker\n\
exec "$@"' > /home/user/entrypoint.sh \
    && chmod +x /home/user/entrypoint.sh \
    && chown user:user /home/user/entrypoint.sh

# Set working directory
WORKDIR /workspace

# Set entrypoint (automatically activates conda environment)
ENTRYPOINT ["/home/user/entrypoint.sh"]

# Default command
CMD ["bash"]
