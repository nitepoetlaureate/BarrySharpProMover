# Barry Sharp Pro Mover - Production Dockerfile
# Multi-stage build for optimized image size

# Stage 1: Build environment
FROM python:3.11-slim as builder

LABEL maintainer="Barry Sharp Development Team"
LABEL description="Barry Sharp Pro Mover - Game Boy Color Action RPG Development Environment"

# Install build dependencies
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (for GB Studio CLI)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./
COPY requirements.txt* ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e ".[dev]"

# Stage 2: Runtime environment
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    nodejs \
    make \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash barrysharp

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=barrysharp:barrysharp . /app

# Create necessary directories
RUN mkdir -p /app/build /app/memory /app/staging && \
    chown -R barrysharp:barrysharp /app

# Switch to non-root user
USER barrysharp

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/scripts:${PATH}"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; sys.exit(0)"

# Default command (can be overridden)
CMD ["python3", "--version"]

# Expose ports (if running web services)
# EXPOSE 8000

# Labels
LABEL org.opencontainers.image.source="https://github.com/nitepoetlaureate/BarrySharpProMover"
LABEL org.opencontainers.image.description="Game Boy Color Action RPG with AI-Powered Development Workflow"
LABEL org.opencontainers.image.licenses="MIT"
