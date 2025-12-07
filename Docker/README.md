# Docker Complete Guide

## Table of Contents
- [Introduction](#introduction)
- [What is Docker?](#what-is-docker)
- [Key Concepts](#key-concepts)
- [Installing Docker](#installing-docker)
- [Docker Architecture](#docker-architecture)
- [Working with Images](#working-with-images)
- [Working with Containers](#working-with-containers)
- [Dockerfile](#dockerfile)
- [Docker Compose](#docker-compose)
- [Docker Networking](#docker-networking)
- [Docker Volumes](#docker-volumes)
- [Docker Registry](#docker-registry)
- [Multi-Stage Builds](#multi-stage-builds)
- [Docker Security](#docker-security)
- [Best Practices](#best-practices)
- [Real-World Examples](#real-world-examples)
- [Troubleshooting](#troubleshooting)

## Introduction

Docker is a platform that enables developers to package applications into containers—standardized units that include everything needed to run the application. This ensures consistency across different environments and simplifies deployment.

## What is Docker?

Docker is a **containerization platform** that allows you to:

- **Package applications** with all dependencies
- **Run consistently** across different environments
- **Isolate applications** from each other
- **Deploy faster** than traditional VMs
- **Scale easily** with orchestration tools

### Benefits
- ✅ Lightweight compared to VMs
- ✅ Fast startup times (seconds vs minutes)
- ✅ Consistent environment (dev = staging = production)
- ✅ Easy version control for infrastructure
- ✅ Efficient resource utilization

### Docker vs Virtual Machines

**Virtual Machines:**
- Include full OS
- Slower to start
- More resource-intensive
- Better isolation

**Docker Containers:**
- Share host OS kernel
- Start in seconds
- Lightweight
- Sufficient isolation for most use cases

## Key Concepts

### Container
A lightweight, standalone, executable package that includes everything needed to run a piece of software.

### Image
A read-only template with instructions for creating a container. Think of it as a snapshot or blueprint.

### Dockerfile
A text file containing instructions to build a Docker image.

### Docker Hub
A cloud-based registry service for sharing and storing Docker images.

### Volume
A persistent data storage mechanism that exists outside container lifecycle.

### Network
Allows containers to communicate with each other and the outside world.

## Installing Docker

### Windows
```bash
# Download Docker Desktop from https://www.docker.com/products/docker-desktop

# Using Chocolatey
choco install docker-desktop
```

### macOS
```bash
# Download Docker Desktop from https://www.docker.com/products/docker-desktop

# Using Homebrew
brew install --cask docker
```

### Linux (Ubuntu/Debian)
```bash
# Update package index
sudo apt-get update

# Install prerequisites
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set up stable repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

# Add user to docker group (optional - grants root-equivalent privileges)
# Note: This allows running Docker without sudo but has security implications
# Alternative: Use sudo for Docker commands or configure rootless Docker
sudo usermod -aG docker $USER
# Log out and back in for group membership to take effect
```

### Verify Installation
```bash
docker --version
docker run hello-world
```

## Docker Architecture

### Components

1. **Docker Client**: CLI tool for interacting with Docker
2. **Docker Daemon**: Background service managing containers
3. **Docker Registry**: Stores Docker images
4. **Docker Objects**: Images, containers, networks, volumes

### How It Works
```
[Docker Client] → [Docker Daemon] → [Containers]
                         ↓
                  [Docker Registry]
```

## Working with Images

### Searching Images
```bash
# Search Docker Hub
docker search nginx

# Search with filters
docker search --filter stars=100 nginx
```

### Pulling Images
```bash
# Pull latest version
docker pull nginx

# Pull specific version
docker pull nginx:1.21

# Pull from specific registry
docker pull ghcr.io/owner/image:tag
```

### Listing Images
```bash
# List all images
docker images

# List with details
docker images -a

# List image IDs only
docker images -q
```

### Removing Images
```bash
# Remove specific image
docker rmi nginx:latest

# Remove by ID
docker rmi abc123def456

# Remove all unused images
docker image prune

# Remove all images
docker rmi $(docker images -q)
```

### Inspecting Images
```bash
# View image details
docker inspect nginx:latest

# View image history
docker history nginx:latest
```

### Tagging Images
```bash
# Tag an image
docker tag nginx:latest myregistry.com/nginx:v1

# Create multiple tags
docker tag myapp:latest myapp:1.0.0
docker tag myapp:latest myapp:production
```

## Working with Containers

### Running Containers

#### Basic Run
```bash
# Run container in foreground
docker run nginx

# Run in detached mode (background)
docker run -d nginx

# Run with custom name
docker run --name my-nginx -d nginx

# Run and remove after exit
docker run --rm nginx
```

#### Port Mapping
```bash
# Map container port to host port
docker run -d -p 8080:80 nginx

# Map to random host port
docker run -d -P nginx

# Map multiple ports
docker run -d -p 8080:80 -p 8443:443 nginx
```

#### Environment Variables
```bash
# Pass single variable
docker run -e API_KEY=abc123 myapp

# Pass multiple variables
docker run -e VAR1=value1 -e VAR2=value2 myapp

# Load from file
docker run --env-file .env myapp
```

#### Volume Mounting
```bash
# Mount host directory
docker run -v /host/path:/container/path nginx

# Mount named volume
docker run -v myvolume:/app/data nginx

# Read-only mount
docker run -v /host/path:/container/path:ro nginx
```

### Managing Containers

#### List Containers
```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# List only container IDs
docker ps -q
```

#### Start/Stop Containers
```bash
# Stop container
docker stop container-name

# Start stopped container
docker start container-name

# Restart container
docker restart container-name

# Pause container
docker pause container-name

# Unpause container
docker unpause container-name
```

#### Remove Containers
```bash
# Remove stopped container
docker rm container-name

# Force remove running container
docker rm -f container-name

# Remove all stopped containers
docker container prune

# Remove all containers
docker rm $(docker ps -aq)
```

### Interacting with Containers

#### Execute Commands
```bash
# Execute command in running container
docker exec container-name ls -la

# Open interactive shell
docker exec -it container-name bash

# Run as specific user
docker exec -u root -it container-name bash
```

#### View Logs
```bash
# View logs
docker logs container-name

# Follow logs (like tail -f)
docker logs -f container-name

# Show last 100 lines
docker logs --tail 100 container-name

# Show logs with timestamps
docker logs -t container-name
```

#### Inspect Containers
```bash
# View container details
docker inspect container-name

# View specific field
docker inspect --format='{{.NetworkSettings.IPAddress}}' container-name
```

#### Copy Files
```bash
# Copy from container to host
docker cp container-name:/path/in/container /host/path

# Copy from host to container
docker cp /host/path container-name:/path/in/container
```

#### View Resource Usage
```bash
# View live resource stats
docker stats

# View stats for specific container
docker stats container-name

# View stats once (no streaming)
docker stats --no-stream
```

## Dockerfile

### Basic Dockerfile Structure
```dockerfile
# Base image
FROM ubuntu:20.04

# Maintainer information (optional)
LABEL maintainer="your-email@example.com"

# Set working directory
WORKDIR /app

# Copy files
COPY package.json .

# Install dependencies
RUN apt-get update && apt-get install -y nodejs npm

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Set environment variables
ENV NODE_ENV=production

# Define entrypoint
ENTRYPOINT ["node"]

# Default command
CMD ["server.js"]
```

### Dockerfile Instructions

#### FROM
```dockerfile
# Use official image
FROM node:18-alpine

# Use specific version
FROM python:3.11-slim

# Multi-stage build
FROM node:18 AS builder
```

#### RUN
```dockerfile
# Execute command
RUN apt-get update && apt-get install -y curl

# Multiple commands
RUN npm install && \
    npm run build && \
    npm prune --production
```

#### COPY vs ADD
```dockerfile
# COPY - simple file copy
COPY package.json /app/

# ADD - can extract archives and download URLs
ADD https://example.com/file.tar.gz /tmp/
ADD archive.tar.gz /app/
```

#### WORKDIR
```dockerfile
# Set working directory (creates if doesn't exist)
WORKDIR /app

# Subsequent commands run in this directory
COPY . .
RUN npm install
```

#### ENV
```dockerfile
# Set environment variable
ENV NODE_ENV=production
ENV PORT=3000

# Multiple variables
ENV API_URL=https://api.example.com \
    DEBUG=false
```

#### EXPOSE
```dockerfile
# Document which ports the container listens on
EXPOSE 3000
EXPOSE 8080 8443
```

#### VOLUME
```dockerfile
# Create mount point
VOLUME /app/data

# Multiple volumes
VOLUME ["/var/log", "/var/db"]
```

#### USER
```dockerfile
# Run as non-root user
RUN adduser -D myuser
USER myuser
```

#### ARG
```dockerfile
# Build-time variable
ARG VERSION=latest
FROM node:${VERSION}

ARG BUILD_DATE
LABEL build-date=$BUILD_DATE
```

#### ENTRYPOINT vs CMD
```dockerfile
# ENTRYPOINT - main command (not easily overridden)
ENTRYPOINT ["python", "app.py"]

# CMD - default arguments (can be overridden)
CMD ["--port", "8000"]

# Together: python app.py --port 8000
```

### Building Images
```bash
# Build image from Dockerfile
docker build -t myapp:latest .

# Build with custom Dockerfile name
docker build -f Dockerfile.dev -t myapp:dev .

# Build with build arguments
docker build --build-arg VERSION=1.0 -t myapp:1.0 .

# Build without cache
docker build --no-cache -t myapp:latest .

# Build with specific target (multi-stage)
docker build --target production -t myapp:prod .
```

### Example: Node.js Application
```dockerfile
FROM node:18-alpine

# Create app directory
WORKDIR /usr/src/app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001
USER nodejs

# Expose port
EXPOSE 3000

# Start application
CMD ["node", "server.js"]
```

### Example: Python Application
```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1001 appuser
USER appuser

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "app.py"]
```

## Docker Compose

### What is Docker Compose?
Docker Compose is a tool for defining and running multi-container Docker applications using a YAML file.

### docker-compose.yml Structure
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - db
    volumes:
      - ./src:/app/src
    networks:
      - app-network

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: myapp
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - app-network

volumes:
  db-data:

networks:
  app-network:
    driver: bridge
```

### Docker Compose Commands
```bash
# Start services
docker-compose up

# Start in detached mode
docker-compose up -d

# Build and start
docker-compose up --build

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View logs
docker-compose logs

# Follow logs for specific service
docker-compose logs -f web

# List running services
docker-compose ps

# Execute command in service
docker-compose exec web bash

# Scale service
docker-compose up -d --scale web=3
```

### Complete Example: MERN Stack
```yaml
version: '3.8'

services:
  # MongoDB
  mongodb:
    image: mongo:6
    container_name: mongodb
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: secret
    volumes:
      - mongo-data:/data/db
    networks:
      - mern-network

  # Backend (Node.js + Express)
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: backend
    environment:
      - NODE_ENV=production
      - MONGODB_URI=mongodb://admin:secret@mongodb:27017/myapp?authSource=admin
    ports:
      - "5000:5000"
    depends_on:
      - mongodb
    networks:
      - mern-network

  # Frontend (React)
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    networks:
      - mern-network

volumes:
  mongo-data:

networks:
  mern-network:
    driver: bridge
```

## Docker Networking

### Network Types

#### Bridge (Default)
```bash
# Create bridge network
docker network create my-bridge-network

# Run container on network
docker run -d --network my-bridge-network nginx
```

#### Host
```bash
# Use host network (no isolation)
docker run -d --network host nginx
```

#### None
```bash
# No network access
docker run -d --network none nginx
```

### Network Commands
```bash
# List networks
docker network ls

# Create network
docker network create my-network

# Inspect network
docker network inspect my-network

# Connect container to network
docker network connect my-network container-name

# Disconnect container from network
docker network disconnect my-network container-name

# Remove network
docker network rm my-network

# Remove unused networks
docker network prune
```

### Container Communication
```yaml
# docker-compose.yml
services:
  app:
    image: myapp
    networks:
      - frontend
      - backend
  
  db:
    image: postgres
    networks:
      - backend

networks:
  frontend:
  backend:
```

## Docker Volumes

### Volume Types

#### Named Volumes
```bash
# Create volume
docker volume create my-volume

# Use in container
docker run -v my-volume:/app/data nginx
```

#### Bind Mounts
```bash
# Mount host directory
docker run -v /host/path:/container/path nginx

# Current directory
docker run -v $(pwd):/app nginx
```

#### tmpfs Mounts
```bash
# Temporary file storage in memory
docker run --tmpfs /app/cache nginx
```

### Volume Commands
```bash
# List volumes
docker volume ls

# Create volume
docker volume create my-volume

# Inspect volume
docker volume inspect my-volume

# Remove volume
docker volume rm my-volume

# Remove unused volumes
docker volume prune

# Remove all volumes
docker volume rm $(docker volume ls -q)
```

### Volume Example
```yaml
# docker-compose.yml
services:
  app:
    image: myapp
    volumes:
      # Named volume
      - app-data:/app/data
      # Bind mount
      - ./config:/app/config:ro
      # Anonymous volume
      - /app/logs

volumes:
  app-data:
    driver: local
```

## Docker Registry

### Docker Hub

#### Login
```bash
# Login to Docker Hub
docker login

# Login with username
docker login -u username
```

#### Push Images
```bash
# Tag image
docker tag myapp:latest username/myapp:latest

# Push to Docker Hub
docker push username/myapp:latest

# Push all tags
docker push username/myapp --all-tags
```

#### Pull Images
```bash
# Pull from Docker Hub
docker pull username/myapp:latest
```

### Private Registry

#### Run Local Registry
```bash
# Start registry
docker run -d -p 5000:5000 --name registry registry:2

# Tag for local registry
docker tag myapp localhost:5000/myapp

# Push to local registry
docker push localhost:5000/myapp

# Pull from local registry
docker pull localhost:5000/myapp
```

## Multi-Stage Builds

### Benefits
- Smaller final images
- Separate build and runtime dependencies
- Improved security (no build tools in production)

### Example: Node.js Multi-Stage Build
```dockerfile
# Stage 1: Build
FROM node:18 AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY --from=builder /app/dist ./dist

USER node

EXPOSE 3000

CMD ["node", "dist/server.js"]
```

### Example: Go Multi-Stage Build
```dockerfile
# Stage 1: Build
FROM golang:1.21 AS builder

WORKDIR /app

COPY go.* ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Stage 2: Production
FROM alpine:latest

RUN apk --no-cache add ca-certificates

WORKDIR /root/

COPY --from=builder /app/main .

EXPOSE 8080

CMD ["./main"]
```

## Docker Security

### Best Practices

#### 1. Use Official Images
```dockerfile
# Good: Official image
FROM node:18-alpine

# Avoid: Unknown source
FROM random-user/node
```

#### 2. Run as Non-Root User
```dockerfile
FROM node:18-alpine

# Create user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001

USER nodejs
```

#### 3. Scan Images for Vulnerabilities
```bash
# Scan image
docker scan myapp:latest

# Use Trivy
trivy image myapp:latest
```

#### 4. Use Specific Tags
```dockerfile
# Good: Specific version
FROM node:18.17.0-alpine3.18

# Avoid: Latest tag
FROM node:latest
```

#### 5. Minimize Image Layers
```dockerfile
# Good: Combined commands
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Avoid: Multiple RUN commands
RUN apt-get update
RUN apt-get install -y curl
```

#### 6. Don't Store Secrets in Images
```dockerfile
# Bad: Hardcoded secrets
ENV API_KEY=secret123

# Good: Use runtime secrets
# Pass secrets at runtime via -e or --secret
```

#### 7. Use .dockerignore
```dockerignore
# .dockerignore
node_modules
npm-debug.log
.git
.env
.DS_Store
*.md
```

## Best Practices

### 1. Optimize Layer Caching
```dockerfile
# Copy dependency files first
COPY package*.json ./
RUN npm ci

# Copy source code last (changes frequently)
COPY . .
```

### 2. Use Alpine Images
```dockerfile
# Smaller image size
FROM node:18-alpine
FROM python:3.11-alpine
```

### 3. Clean Up in Same Layer
```dockerfile
RUN apt-get update && \
    apt-get install -y package && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### 4. Health Checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost/ || exit 1
```

### 5. Use COPY Instead of ADD
```dockerfile
# Preferred
COPY . .

# Only use ADD for tar extraction or URLs
ADD archive.tar.gz /app/
```

### 6. Leverage Build Cache
```bash
# Use cache from registry
docker build --cache-from myapp:latest -t myapp:new .
```

## Real-World Examples

### Microservices Application
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api
      - frontend

  frontend:
    build: ./frontend
    expose:
      - "3000"

  api:
    build: ./api
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - db-data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data

volumes:
  db-data:
  redis-data:
```

## Troubleshooting

### Common Issues

#### Container Exits Immediately
```bash
# Check logs
docker logs container-name

# Run interactively
docker run -it myapp /bin/sh
```

#### Port Already in Use
```bash
# Find process using port
lsof -i :8080

# Use different port
docker run -p 8081:80 nginx
```

#### Permission Denied
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in
```

#### Out of Disk Space
```bash
# Clean up everything
docker system prune -a

# Remove specific items
docker container prune
docker image prune
docker volume prune
docker network prune
```

### Debugging Commands
```bash
# View container processes
docker top container-name

# View container resource usage
docker stats container-name

# Inspect container
docker inspect container-name

# Export container filesystem
docker export container-name > container.tar
```

## Resources

- [Official Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Play with Docker](https://labs.play-with-docker.com/)

---

**Next Steps**: Learn how to orchestrate containers at scale with [Kubernetes](../Kubernetes/README.md)!
