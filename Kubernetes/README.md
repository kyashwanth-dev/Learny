# Kubernetes Complete Guide

## Table of Contents
- [Introduction](#introduction)
- [What is Kubernetes?](#what-is-kubernetes)
- [Key Concepts](#key-concepts)
- [Architecture](#architecture)
- [Installing Kubernetes](#installing-kubernetes)
- [kubectl Basics](#kubectl-basics)
- [Pods](#pods)
- [Deployments](#deployments)
- [Services](#services)
- [ConfigMaps and Secrets](#configmaps-and-secrets)
- [Volumes](#volumes)
- [Namespaces](#namespaces)
- [Labels and Selectors](#labels-and-selectors)
- [Ingress](#ingress)
- [StatefulSets](#statefulsets)
- [DaemonSets](#daemonsets)
- [Jobs and CronJobs](#jobs-and-cronjobs)
- [Best Practices](#best-practices)
- [Real-World Examples](#real-world-examples)
- [Troubleshooting](#troubleshooting)

## Introduction

Kubernetes (K8s) is an open-source container orchestration platform that automates the deployment, scaling, and management of containerized applications. Originally developed by Google, it's now maintained by the Cloud Native Computing Foundation (CNCF).

## What is Kubernetes?

Kubernetes provides:

- **Automated Deployment**: Deploy containers across a cluster
- **Self-Healing**: Automatically restart failed containers
- **Auto-Scaling**: Scale applications based on demand
- **Load Balancing**: Distribute traffic across containers
- **Rolling Updates**: Update applications without downtime
- **Secret Management**: Store and manage sensitive information
- **Storage Orchestration**: Automatically mount storage systems

### Benefits
- ✅ Platform-agnostic (runs on-premises, cloud, hybrid)
- ✅ High availability and fault tolerance
- ✅ Efficient resource utilization
- ✅ Declarative configuration
- ✅ Large ecosystem and community

## Key Concepts

### Cluster
A set of nodes (machines) that run containerized applications managed by Kubernetes.

### Node
A worker machine (physical or virtual) that runs containerized applications.

### Pod
The smallest deployable unit in Kubernetes, containing one or more containers.

### Deployment
Defines the desired state for Pods and ReplicaSets, managing updates and rollbacks.

### Service
An abstract way to expose an application running on a set of Pods as a network service.

### Namespace
Virtual clusters within a physical cluster for resource isolation.

### Label
Key-value pairs attached to objects for identification and selection.

### Selector
Used to filter and select objects based on labels.

## Architecture

### Control Plane Components

#### API Server
- Entry point for all REST commands
- Validates and processes requests
- Updates etcd

#### etcd
- Distributed key-value store
- Stores cluster state and configuration

#### Scheduler
- Assigns Pods to Nodes
- Considers resource requirements and constraints

#### Controller Manager
- Runs controller processes
- Handles node failures, replication, etc.

#### Cloud Controller Manager
- Integrates with cloud provider APIs
- Manages cloud-specific resources

### Node Components

#### kubelet
- Agent running on each node
- Ensures containers are running in Pods

#### kube-proxy
- Network proxy on each node
- Maintains network rules for Pod communication

#### Container Runtime
- Software for running containers (Docker, containerd, CRI-O)

## Installing Kubernetes

### Local Development

#### Minikube
```bash
# Install Minikube (macOS)
brew install minikube

# Install Minikube (Linux)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start cluster
minikube start

# Check status
minikube status

# Stop cluster
minikube stop

# Delete cluster
minikube delete
```

#### kind (Kubernetes in Docker)
```bash
# Install kind
brew install kind  # macOS
# OR
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Create cluster
kind create cluster

# Create cluster with config
kind create cluster --config kind-config.yaml

# Delete cluster
kind delete cluster
```

#### Docker Desktop
- Enable Kubernetes in Docker Desktop settings
- Kubernetes will run alongside Docker

### Install kubectl
```bash
# macOS
brew install kubectl

# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Windows (Chocolatey)
choco install kubernetes-cli

# Verify installation
kubectl version --client
```

### Verify Cluster
```bash
# Check cluster info
kubectl cluster-info

# Check nodes
kubectl get nodes

# Check system pods
kubectl get pods -n kube-system
```

## kubectl Basics

### Configuration
```bash
# View current context
kubectl config current-context

# List all contexts
kubectl config get-contexts

# Switch context
kubectl config use-context minikube

# View config
kubectl config view

# Set namespace preference
kubectl config set-context --current --namespace=my-namespace
```

### Basic Commands
```bash
# Get resources
kubectl get <resource>
kubectl get pods
kubectl get deployments
kubectl get services

# Get with more details
kubectl get pods -o wide

# Get in different formats
kubectl get pods -o yaml
kubectl get pods -o json

# Describe resource (detailed info)
kubectl describe pod my-pod

# Create resource from file
kubectl create -f deployment.yaml

# Apply configuration (create or update)
kubectl apply -f deployment.yaml

# Delete resource
kubectl delete pod my-pod
kubectl delete -f deployment.yaml

# Edit resource
kubectl edit deployment my-deployment

# View logs
kubectl logs pod-name
kubectl logs -f pod-name  # Follow logs

# Execute command in pod
kubectl exec pod-name -- ls /app
kubectl exec -it pod-name -- /bin/bash

# Port forwarding
kubectl port-forward pod-name 8080:80

# Copy files
kubectl cp pod-name:/path/to/file ./local-file
kubectl cp ./local-file pod-name:/path/to/file
```

### Useful Aliases
```bash
# Add to ~/.bashrc or ~/.zshrc
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get services'
alias kgd='kubectl get deployments'
alias kdp='kubectl describe pod'
alias kl='kubectl logs'
alias kex='kubectl exec -it'
```

## Pods

### What is a Pod?
A Pod is the smallest deployable unit that can contain one or more containers that share:
- Network namespace (same IP address)
- Storage volumes
- Configuration

### Pod YAML
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
```

### Creating Pods
```bash
# Create from YAML
kubectl apply -f pod.yaml

# Create imperatively
kubectl run nginx --image=nginx:1.21

# Create with port
kubectl run nginx --image=nginx --port=80
```

### Multi-Container Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
spec:
  containers:
  - name: app
    image: myapp:latest
    ports:
    - containerPort: 8080
  
  - name: sidecar
    image: logging-agent:latest
    volumeMounts:
    - name: shared-logs
      mountPath: /var/log
  
  volumes:
  - name: shared-logs
    emptyDir: {}
```

### Pod with Resource Limits
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: resource-limited-pod
spec:
  containers:
  - name: app
    image: myapp:latest
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

### Pod Commands
```bash
# Get pods
kubectl get pods

# Get pod details
kubectl describe pod nginx-pod

# Get pod logs
kubectl logs nginx-pod

# Follow logs
kubectl logs -f nginx-pod

# Previous container logs (after crash)
kubectl logs nginx-pod --previous

# Execute command
kubectl exec nginx-pod -- ls /usr/share/nginx/html

# Interactive shell
kubectl exec -it nginx-pod -- /bin/bash

# Delete pod
kubectl delete pod nginx-pod
```

## Deployments

### What is a Deployment?
A Deployment provides declarative updates for Pods and ReplicaSets, managing:
- Desired state
- Rolling updates
- Rollbacks
- Scaling

### Basic Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
```

### Creating Deployments
```bash
# Create from YAML
kubectl apply -f deployment.yaml

# Create imperatively
kubectl create deployment nginx --image=nginx:1.21

# Create with replicas
kubectl create deployment nginx --image=nginx:1.21 --replicas=3
```

### Managing Deployments
```bash
# Get deployments
kubectl get deployments

# Describe deployment
kubectl describe deployment nginx-deployment

# Scale deployment
kubectl scale deployment nginx-deployment --replicas=5

# Autoscale
kubectl autoscale deployment nginx-deployment --min=2 --max=10 --cpu-percent=80

# Update image
kubectl set image deployment/nginx-deployment nginx=nginx:1.22

# Check rollout status
kubectl rollout status deployment/nginx-deployment

# View rollout history
kubectl rollout history deployment/nginx-deployment

# Rollback to previous version
kubectl rollout undo deployment/nginx-deployment

# Rollback to specific revision
kubectl rollout undo deployment/nginx-deployment --to-revision=2

# Pause rollout
kubectl rollout pause deployment/nginx-deployment

# Resume rollout
kubectl rollout resume deployment/nginx-deployment

# Delete deployment
kubectl delete deployment nginx-deployment
```

### Deployment with Strategy
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Max pods above desired count
      maxUnavailable: 1  # Max unavailable pods during update
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 15
          periodSeconds: 20
```

## Services

### What is a Service?
A Service is an abstract way to expose an application running on Pods as a network service.

### Service Types

#### ClusterIP (Default)
Exposes service on cluster-internal IP.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: ClusterIP
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
```

#### NodePort
Exposes service on each Node's IP at a static port.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-nodeport
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
    nodePort: 30080  # Optional: 30000-32767
```

#### LoadBalancer
Exposes service externally using cloud provider's load balancer.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-loadbalancer
spec:
  type: LoadBalancer
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
```

#### ExternalName
Maps service to external DNS name.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-db
spec:
  type: ExternalName
  externalName: db.example.com
```

### Service Commands
```bash
# Get services
kubectl get services
kubectl get svc

# Describe service
kubectl describe service nginx-service

# Create service
kubectl expose deployment nginx-deployment --port=80 --type=LoadBalancer

# Delete service
kubectl delete service nginx-service
```

### Headless Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-headless
spec:
  clusterIP: None  # Makes it headless
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
```

## ConfigMaps and Secrets

### ConfigMaps

#### Create ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database_url: "postgresql://localhost:5432/mydb"
  log_level: "info"
  config.json: |
    {
      "api": {
        "version": "v1",
        "timeout": 30
      }
    }
```

#### Create from Command Line
```bash
# From literal values
kubectl create configmap app-config \
  --from-literal=database_url=postgresql://localhost:5432/mydb \
  --from-literal=log_level=info

# From file
kubectl create configmap app-config --from-file=config.json

# From directory
kubectl create configmap app-config --from-file=./config/
```

#### Use ConfigMap in Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
  - name: myapp
    image: myapp:latest
    env:
    # Single value
    - name: DATABASE_URL
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: database_url
    # All values
    envFrom:
    - configMapRef:
        name: app-config
    # As volume
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: app-config
```

### Secrets

#### Create Secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  username: YWRtaW4=  # base64 encoded
  password: cGFzc3dvcmQ=  # base64 encoded
```

#### Create from Command Line
```bash
# From literal values
kubectl create secret generic db-secret \
  --from-literal=username=admin \
  --from-literal=password=password

# From file
kubectl create secret generic db-secret \
  --from-file=username.txt \
  --from-file=password.txt

# TLS secret
kubectl create secret tls tls-secret \
  --cert=path/to/cert.crt \
  --key=path/to/key.key
```

#### Use Secret in Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
  - name: myapp
    image: myapp:latest
    env:
    # Single value
    - name: DB_USERNAME
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: username
    # All values
    envFrom:
    - secretRef:
        name: db-secret
    # As volume
    volumeMounts:
    - name: secret-volume
      mountPath: /etc/secrets
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: db-secret
```

## Volumes

### Volume Types

#### emptyDir
Temporary directory that shares a Pod's lifetime.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-emptydir
spec:
  containers:
  - name: app
    image: myapp:latest
    volumeMounts:
    - name: cache
      mountPath: /app/cache
  volumes:
  - name: cache
    emptyDir: {}
```

#### hostPath
Mounts file or directory from host node.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-hostpath
spec:
  containers:
  - name: app
    image: myapp:latest
    volumeMounts:
    - name: host-volume
      mountPath: /app/data
  volumes:
  - name: host-volume
    hostPath:
      path: /data
      type: Directory
```

#### PersistentVolume and PersistentVolumeClaim

**PersistentVolume (PV):**
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-storage
spec:
  capacity:
    storage: 10Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: standard
  hostPath:
    path: /mnt/data
```

**PersistentVolumeClaim (PVC):**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-storage
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: standard
```

**Use in Pod:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-pvc
spec:
  containers:
  - name: app
    image: myapp:latest
    volumeMounts:
    - name: storage
      mountPath: /app/data
  volumes:
  - name: storage
    persistentVolumeClaim:
      claimName: pvc-storage
```

## Namespaces

### What are Namespaces?
Namespaces provide a way to divide cluster resources between multiple users or teams.

### Default Namespaces
- `default`: Default namespace for objects with no other namespace
- `kube-system`: For objects created by Kubernetes system
- `kube-public`: Readable by all users
- `kube-node-lease`: For node heartbeat data

### Namespace Commands
```bash
# List namespaces
kubectl get namespaces
kubectl get ns

# Create namespace
kubectl create namespace dev

# Create from YAML
kubectl apply -f namespace.yaml

# Delete namespace
kubectl delete namespace dev

# Get resources in namespace
kubectl get pods -n dev
kubectl get all -n dev

# Set default namespace for context
kubectl config set-context --current --namespace=dev
```

### Namespace YAML
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dev
  labels:
    environment: development
```

### Resource with Namespace
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  namespace: dev
spec:
  containers:
  - name: nginx
    image: nginx:1.21
```

### Resource Quotas
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: dev-quota
  namespace: dev
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    pods: "10"
```

## Labels and Selectors

### Labels
Key-value pairs attached to objects for identification.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
    environment: production
    version: v1
spec:
  containers:
  - name: nginx
    image: nginx:1.21
```

### Label Commands
```bash
# Show labels
kubectl get pods --show-labels

# Filter by label
kubectl get pods -l app=nginx
kubectl get pods -l environment=production

# Multiple label selectors
kubectl get pods -l 'app=nginx,environment=production'

# Add label
kubectl label pod nginx-pod tier=frontend

# Update label
kubectl label pod nginx-pod version=v2 --overwrite

# Remove label
kubectl label pod nginx-pod version-
```

### Selectors in Services
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
    environment: production
  ports:
  - port: 80
```

## Ingress

### What is Ingress?
Ingress exposes HTTP and HTTPS routes from outside the cluster to services within the cluster.

### Install Ingress Controller (Nginx)
```bash
# Minikube
minikube addons enable ingress

# Manual installation (recommended: review manifest before applying)
# Download and review the manifest first:
curl -O https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml
# Review the file, then apply:
kubectl apply -f deploy.yaml

# Or apply directly (less secure but faster):
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml
```

### Basic Ingress
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: simple-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

### Ingress with Multiple Paths
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: multi-path-ingress
spec:
  rules:
  - host: example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 8080
      - path: /web
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

### Ingress with TLS
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-ingress
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: tls-secret
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

## StatefulSets

### What is a StatefulSet?
StatefulSet is used for stateful applications that require:
- Stable, unique network identifiers
- Stable, persistent storage
- Ordered, graceful deployment and scaling
- Ordered, automated rolling updates

### StatefulSet Example
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: "postgres"
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 10Gi
```

### Headless Service for StatefulSet
```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres
spec:
  clusterIP: None
  selector:
    app: postgres
  ports:
  - port: 5432
```

## DaemonSets

### What is a DaemonSet?
A DaemonSet ensures that all (or some) Nodes run a copy of a Pod. Typically used for:
- Node monitoring daemons
- Log collection daemons
- Storage daemons

### DaemonSet Example
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: kube-system
spec:
  selector:
    matchLabels:
      name: fluentd
  template:
    metadata:
      labels:
        name: fluentd
    spec:
      containers:
      - name: fluentd
        image: fluentd:latest
        volumeMounts:
        - name: varlog
          mountPath: /var/log
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
```

## Jobs and CronJobs

### Jobs
A Job creates one or more Pods and ensures they successfully terminate.

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: batch-job
spec:
  completions: 3  # Run 3 times
  parallelism: 2  # Run 2 at a time
  template:
    spec:
      containers:
      - name: worker
        image: busybox
        command: ["sh", "-c", "echo Processing && sleep 10"]
      restartPolicy: OnFailure
```

### CronJobs
A CronJob creates Jobs on a repeating schedule.

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup-job
spec:
  schedule: "0 2 * * *"  # Every day at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: backup-tool:latest
            command: ["sh", "-c", "backup.sh"]
          restartPolicy: OnFailure
```

## Best Practices

### 1. Use Namespaces
```bash
# Organize resources by environment
kubectl create namespace production
kubectl create namespace staging
kubectl create namespace development
```

### 2. Resource Limits
```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "250m"
  limits:
    memory: "128Mi"
    cpu: "500m"
```

### 3. Health Checks
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

### 4. Use ConfigMaps and Secrets
- Don't hardcode configuration
- Store sensitive data in Secrets
- Use ConfigMaps for non-sensitive config

### 5. Label Everything
```yaml
metadata:
  labels:
    app: myapp
    version: v1
    environment: production
    team: backend
```

### 6. Use Rolling Updates
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```

### 7. Set Pod Disruption Budgets
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: myapp
```

## Real-World Examples

### Complete Application Stack
```yaml
# Namespace
apiVersion: v1
kind: Namespace
metadata:
  name: myapp

---
# ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: myapp
data:
  LOG_LEVEL: "info"
  DATABASE_URL: "postgresql://db:5432/mydb"

---
# Secret
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
  namespace: myapp
type: Opaque
data:
  db-password: cGFzc3dvcmQ=

---
# Database Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: myapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: db-password
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc

---
# Database Service
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: myapp
spec:
  selector:
    app: postgres
  ports:
  - port: 5432

---
# Application Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
  namespace: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
      - name: webapp
        image: myapp:latest
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secret
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"

---
# Application Service
apiVersion: v1
kind: Service
metadata:
  name: webapp
  namespace: myapp
spec:
  type: LoadBalancer
  selector:
    app: webapp
  ports:
  - port: 80
    targetPort: 8080

---
# Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: webapp-ingress
  namespace: myapp
spec:
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: webapp
            port:
              number: 80
```

## Troubleshooting

### Common Issues

#### Pod Not Starting
```bash
# Check pod status
kubectl get pods

# Describe pod for events
kubectl describe pod pod-name

# Check logs
kubectl logs pod-name

# Check previous logs if crashed
kubectl logs pod-name --previous
```

#### Image Pull Errors
```bash
# Check image name and tag
kubectl describe pod pod-name | grep Image

# Verify image exists
docker pull image-name:tag

# Check imagePullSecrets if using private registry
```

#### Service Not Accessible
```bash
# Check service endpoints
kubectl get endpoints service-name

# Verify selector matches pod labels
kubectl get pods --show-labels

# Test from within cluster
kubectl run test --image=busybox -it --rm -- wget -O- service-name
```

#### Insufficient Resources
```bash
# Check node resources
kubectl top nodes

# Check pod resources
kubectl top pods

# Describe nodes for capacity
kubectl describe nodes
```

### Debugging Commands
```bash
# Get events
kubectl get events --sort-by='.lastTimestamp'

# Check cluster info
kubectl cluster-info dump

# Check component status
kubectl get componentstatuses

# Debug pod with shell
kubectl run debug --image=busybox -it --rm -- sh
```

## Resources

- [Official Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kubernetes By Example](https://kubernetesbyexample.com/)
- [Kubernetes Patterns](https://k8spatterns.io/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Awesome Kubernetes](https://github.com/ramitsurana/awesome-kubernetes)
- [Play with Kubernetes](https://labs.play-with-k8s.com/)

---

**Next Steps**: Learn how to automate your CI/CD pipelines with [Jenkins](../Jenkins/README.md)!
