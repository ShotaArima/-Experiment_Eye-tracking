FROM ghcr.io/astral-sh/uv:python3.12-bookworm

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    git \
    curl \
    ffmpeg \ 
    && rm -rf /var/lib/apt/lists/*

