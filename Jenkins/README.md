# Jenkins Complete Guide

## Table of Contents
- [Introduction](#introduction)
- [What is Jenkins?](#what-is-jenkins)
- [Key Concepts](#key-concepts)
- [Installing Jenkins](#installing-jenkins)
- [Jenkins Architecture](#jenkins-architecture)
- [Getting Started](#getting-started)
- [Jenkins Jobs](#jenkins-jobs)
- [Jenkins Pipeline](#jenkins-pipeline)
- [Jenkinsfile](#jenkinsfile)
- [Plugins](#plugins)
- [Credentials Management](#credentials-management)
- [Jenkins with Docker](#jenkins-with-docker)
- [Jenkins with Kubernetes](#jenkins-with-kubernetes)
- [Distributed Builds](#distributed-builds)
- [Best Practices](#best-practices)
- [Real-World Examples](#real-world-examples)
- [Troubleshooting](#troubleshooting)

## Introduction

Jenkins is an open-source automation server that enables developers to build, test, and deploy their software reliably. It's one of the most popular CI/CD tools used in DevOps practices.

## What is Jenkins?

Jenkins provides:

- **Continuous Integration**: Automatically build and test code changes
- **Continuous Delivery**: Automate the entire release process
- **Extensibility**: 1800+ plugins for integration with various tools
- **Distributed Builds**: Scale builds across multiple machines
- **Pipeline as Code**: Define CI/CD pipelines in version control
- **Easy Configuration**: Web-based interface for setup

### Benefits
- ✅ Free and open-source
- ✅ Large community and ecosystem
- ✅ Highly customizable with plugins
- ✅ Supports all major version control systems
- ✅ Platform-agnostic (Windows, Linux, macOS)
- ✅ Can orchestrate complex workflows

## Key Concepts

### Job/Project
A runnable task in Jenkins (e.g., build, test, deploy).

### Build
A single execution of a job.

### Pipeline
A suite of plugins that supports implementing CI/CD pipelines.

### Node/Agent
A machine that executes Jenkins builds.

### Executor
A slot for executing builds on a node.

### Workspace
A directory where builds are executed.

### Plugin
Extensions that add functionality to Jenkins.

### Stage
A logical group of steps in a pipeline.

### Step
A single task in a pipeline (e.g., shell command, build step).

## Installing Jenkins

### Prerequisites
- Java 11 or Java 17 installed
- Minimum 256 MB RAM (1 GB+ recommended)
- 10 GB disk space

### Install on Linux (Ubuntu/Debian)

```bash
# Update system
sudo apt update

# Install Java
sudo apt install openjdk-11-jdk -y

# Add Jenkins repository key (download and verify before adding)
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key -o jenkins-key.asc
# Review the key file, then install
sudo cp jenkins-key.asc /usr/share/keyrings/jenkins-keyring.asc

# Add Jenkins repository
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install Jenkins
sudo apt update
sudo apt install jenkins -y

# Start Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Check status
sudo systemctl status jenkins
```

### Install on macOS

```bash
# Using Homebrew
brew install jenkins-lts

# Start Jenkins
brew services start jenkins-lts
```

### Install on Windows

```bash
# Download MSI installer from https://www.jenkins.io/download/

# Or use Chocolatey
choco install jenkins
```

### Install with Docker

```bash
# Pull Jenkins image
docker pull jenkins/jenkins:lts

# Run Jenkins container
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts

# Get initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### Initial Setup

1. Open browser: `http://localhost:8080`
2. Enter initial admin password:
   ```bash
   # Linux/Mac
   sudo cat /var/lib/jenkins/secrets/initialAdminPassword
   
   # Docker
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```
3. Install suggested plugins
4. Create admin user
5. Configure Jenkins URL

## Jenkins Architecture

### Master-Agent Architecture

**Jenkins Master:**
- Schedules build jobs
- Dispatches builds to agents
- Monitors agents
- Records and presents build results
- Manages configuration

**Jenkins Agent (Slave):**
- Executes builds dispatched by master
- Can run on different platforms
- Provides scalability

### Components

```
┌─────────────────────┐
│   Jenkins Master    │
│  - Web UI           │
│  - Job Scheduler    │
│  - Build Monitor    │
└──────────┬──────────┘
           │
    ┌──────┴──────┬──────────┐
    │             │          │
┌───▼───┐   ┌────▼────┐  ┌──▼────┐
│Agent 1│   │ Agent 2 │  │Agent 3│
│Linux  │   │ Windows │  │ macOS │
└───────┘   └─────────┘  └───────┘
```

## Getting Started

### Create Your First Job

1. Click "New Item"
2. Enter name: "my-first-job"
3. Select "Freestyle project"
4. Click "OK"

### Configure Build Steps

**Execute Shell (Linux/Mac):**
```bash
echo "Hello from Jenkins!"
date
pwd
ls -la
```

**Execute Windows Batch:**
```batch
echo Hello from Jenkins!
date /t
dir
```

### Build Triggers

- **Build periodically**: Cron-like scheduling
  ```
  H/15 * * * *  # Every 15 minutes
  H 2 * * *     # Daily at 2 AM
  H 0 * * 0     # Weekly on Sunday
  ```

- **Poll SCM**: Check for changes in repository
  ```
  H/5 * * * *   # Check every 5 minutes
  ```

- **GitHub hook trigger**: Webhook from GitHub

- **Build after other projects**: Chain jobs together

### Post-Build Actions

- Archive artifacts
- Publish test results
- Email notifications
- Trigger downstream projects
- Deploy to servers

## Jenkins Jobs

### Freestyle Project

Simple job type with GUI configuration.

**Example Configuration:**
- **Source Code Management**: Git
  - Repository URL: `https://github.com/user/repo.git`
  - Branch: `*/main`
  - Credentials: Add GitHub credentials

- **Build Triggers**: GitHub hook trigger

- **Build Steps**: Execute shell
  ```bash
  npm install
  npm test
  npm run build
  ```

- **Post-Build Actions**: Archive artifacts
  - Files to archive: `dist/**/*`

### Maven Project

For building Maven projects.

```xml
<!-- Build -->
Root POM: pom.xml
Goals: clean install
```

### Pipeline Project

Define build pipeline as code (recommended).

## Jenkins Pipeline

### What is a Pipeline?

A pipeline is a suite of plugins supporting CI/CD pipelines defined as code.

### Pipeline Benefits

- **Code**: Pipelines in version control
- **Durable**: Survives Jenkins restarts
- **Pausable**: Can wait for human input
- **Versatile**: Supports complex workflows
- **Extensible**: Custom steps via plugins

### Pipeline Types

#### Declarative Pipeline (Recommended)

Simpler syntax, structured format.

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                sh 'npm install'
            }
        }
        
        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'npm test'
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                sh 'npm run deploy'
            }
        }
    }
}
```

#### Scripted Pipeline

More flexible, Groovy-based.

```groovy
node {
    stage('Build') {
        echo 'Building...'
        sh 'npm install'
    }
    
    stage('Test') {
        echo 'Testing...'
        sh 'npm test'
    }
    
    stage('Deploy') {
        echo 'Deploying...'
        sh 'npm run deploy'
    }
}
```

## Jenkinsfile

### What is a Jenkinsfile?

A text file containing pipeline definition, typically stored in source control.

### Basic Jenkinsfile

```groovy
pipeline {
    agent any
    
    environment {
        // Environment variables
        NODE_ENV = 'production'
        API_URL = 'https://api.example.com'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building application...'
                sh 'npm ci'
                sh 'npm run build'
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'npm test'
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo 'Deploying to production...'
                sh './deploy.sh'
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
        always {
            cleanWs()
        }
    }
}
```

### Advanced Jenkinsfile Features

#### Parallel Execution

```groovy
pipeline {
    agent any
    
    stages {
        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh 'npm run test:unit'
                    }
                }
                stage('Integration Tests') {
                    steps {
                        sh 'npm run test:integration'
                    }
                }
                stage('E2E Tests') {
                    steps {
                        sh 'npm run test:e2e'
                    }
                }
            }
        }
    }
}
```

#### Conditional Execution

```groovy
pipeline {
    agent any
    
    stages {
        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                sh './deploy-staging.sh'
            }
        }
        
        stage('Deploy to Production') {
            when {
                allOf {
                    branch 'main'
                    environment name: 'DEPLOY', value: 'true'
                }
            }
            steps {
                sh './deploy-production.sh'
            }
        }
    }
}
```

#### Input Steps

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'npm run build'
            }
        }
        
        stage('Approval') {
            steps {
                input message: 'Deploy to production?', 
                      ok: 'Deploy'
            }
        }
        
        stage('Deploy') {
            steps {
                sh './deploy.sh'
            }
        }
    }
}
```

#### Using Credentials

```groovy
pipeline {
    agent any
    
    environment {
        // Username/password credential
        DOCKER_CREDS = credentials('docker-hub-credentials')
        
        // Secret text
        API_KEY = credentials('api-key')
    }
    
    stages {
        stage('Login') {
            steps {
                // Using --password-stdin is the secure way to pass passwords to docker login
                sh 'echo $DOCKER_CREDS_PSW | docker login -u $DOCKER_CREDS_USR --password-stdin'
            }
        }
        
        stage('Build') {
            steps {
                sh 'docker build -t myapp:latest .'
            }
        }
        
        stage('Push') {
            steps {
                sh 'docker push myapp:latest'
            }
        }
    }
}
```

#### Matrix Builds

```groovy
pipeline {
    agent none
    
    stages {
        stage('Build') {
            matrix {
                agent any
                axes {
                    axis {
                        name 'PLATFORM'
                        values 'linux', 'windows', 'mac'
                    }
                    axis {
                        name 'NODE_VERSION'
                        values '14', '16', '18'
                    }
                }
                stages {
                    stage('Test') {
                        steps {
                            echo "Testing on ${PLATFORM} with Node ${NODE_VERSION}"
                            sh 'npm test'
                        }
                    }
                }
            }
        }
    }
}
```

## Plugins

### Essential Plugins

#### Version Control
- **Git Plugin**: Git integration
- **GitHub Plugin**: GitHub integration
- **Bitbucket Plugin**: Bitbucket integration

#### Build Tools
- **Maven Integration**: Maven project support
- **Gradle Plugin**: Gradle build support
- **Node.js Plugin**: Node.js installation

#### Pipeline
- **Pipeline**: Core pipeline functionality
- **Pipeline: Stage View**: Visualize pipeline stages
- **Blue Ocean**: Modern UI for pipelines

#### Notifications
- **Email Extension**: Advanced email notifications
- **Slack Notification**: Slack integration
- **Microsoft Teams Notification**: Teams integration

#### Cloud & Containers
- **Docker Plugin**: Docker integration
- **Kubernetes Plugin**: Kubernetes agent provisioning
- **Amazon EC2 Plugin**: EC2 cloud agents

#### Testing & Quality
- **JUnit Plugin**: Publish test results
- **Code Coverage API**: Code coverage reports
- **SonarQube Scanner**: Code quality analysis

### Installing Plugins

**Via Web UI:**
1. Manage Jenkins → Manage Plugins
2. Available tab
3. Search for plugin
4. Check box and click "Install without restart"

**Via Jenkins CLI:**
```bash
java -jar jenkins-cli.jar -s http://localhost:8080/ install-plugin plugin-name
```

## Credentials Management

### Adding Credentials

1. Manage Jenkins → Manage Credentials
2. Select domain (e.g., Global)
3. Add Credentials

### Credential Types

#### Username with Password
```groovy
environment {
    CREDS = credentials('my-credentials-id')
}
steps {
    sh 'echo $CREDS_USR'  // Username
    sh 'echo $CREDS_PSW'  // Password
}
```

#### Secret Text
```groovy
environment {
    API_KEY = credentials('api-key-id')
}
steps {
    sh 'curl -H "Authorization: Bearer $API_KEY" https://api.example.com'
}
```

#### SSH Username with Private Key
```groovy
sshagent(['ssh-credentials-id']) {
    sh 'ssh user@server "deploy.sh"'
}
```

#### Secret File
```groovy
withCredentials([file(credentialsId: 'config-file-id', variable: 'CONFIG')]) {
    sh 'cat $CONFIG'
}
```

## Jenkins with Docker

### Docker Agent

```groovy
pipeline {
    agent {
        docker {
            image 'node:18-alpine'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
    }
}
```

### Multi-Container Pipeline

```groovy
pipeline {
    agent none
    
    stages {
        stage('Build') {
            agent {
                docker {
                    image 'node:18'
                }
            }
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
        
        stage('Test') {
            agent {
                docker {
                    image 'node:18'
                }
            }
            steps {
                sh 'npm test'
            }
        }
        
        stage('Build Docker Image') {
            agent any
            steps {
                script {
                    docker.build("myapp:${env.BUILD_NUMBER}")
                }
            }
        }
    }
}
```

### Docker Compose

```groovy
pipeline {
    agent any
    
    stages {
        stage('Test') {
            steps {
                sh 'docker-compose up -d'
                sh 'docker-compose exec -T web npm test'
            }
        }
    }
    
    post {
        always {
            sh 'docker-compose down -v'
        }
    }
}
```

## Jenkins with Kubernetes

### Kubernetes Plugin Configuration

```groovy
pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: node
    image: node:18
    command:
    - sleep
    args:
    - infinity
  - name: docker
    image: docker:latest
    command:
    - sleep
    args:
    - infinity
    volumeMounts:
    - name: dockersock
      mountPath: /var/run/docker.sock
  volumes:
  - name: dockersock
    hostPath:
      path: /var/run/docker.sock
'''
        }
    }
    
    stages {
        stage('Build') {
            steps {
                container('node') {
                    sh 'npm install'
                    sh 'npm run build'
                }
            }
        }
        
        stage('Docker Build') {
            steps {
                container('docker') {
                    sh 'docker build -t myapp:latest .'
                }
            }
        }
    }
}
```

## Distributed Builds

### Setting Up Agent

**On Master:**
1. Manage Jenkins → Manage Nodes and Clouds
2. New Node
3. Enter name and select "Permanent Agent"
4. Configure:
   - Remote root directory: `/home/jenkins`
   - Labels: `linux docker`
   - Launch method: Via SSH

**On Agent Machine:**
```bash
# Create jenkins user
sudo useradd -m jenkins

# Install Java
sudo apt install openjdk-11-jdk

# Set up SSH key authentication
```

### Using Agents in Pipeline

```groovy
pipeline {
    agent none
    
    stages {
        stage('Build on Linux') {
            agent {
                label 'linux'
            }
            steps {
                sh 'make build'
            }
        }
        
        stage('Build on Windows') {
            agent {
                label 'windows'
            }
            steps {
                bat 'build.bat'
            }
        }
    }
}
```

## Best Practices

### 1. Use Jenkinsfile

Store pipeline definition in source control alongside code.

```groovy
// Jenkinsfile in repository root
pipeline {
    agent any
    // ...
}
```

### 2. Use Declarative Pipeline

Simpler syntax, better error handling.

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                // Build steps
            }
        }
    }
}
```

### 3. Parameterize Builds

```groovy
pipeline {
    agent any
    
    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Branch to build')
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'prod'], description: 'Environment')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Run tests?')
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: "${params.BRANCH}", url: 'https://github.com/user/repo.git'
            }
        }
    }
}
```

### 4. Handle Failures Gracefully

```groovy
pipeline {
    agent any
    
    stages {
        stage('Test') {
            steps {
                script {
                    try {
                        sh 'npm test'
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error "Tests failed: ${e.message}"
                    }
                }
            }
        }
    }
    
    post {
        failure {
            emailext(
                subject: "Build Failed: ${env.JOB_NAME}",
                body: "Build failed. Check console output.",
                to: "team@example.com"
            )
        }
    }
}
```

### 5. Clean Workspace

```groovy
post {
    always {
        cleanWs()
    }
}
```

### 6. Archive Artifacts

```groovy
post {
    success {
        archiveArtifacts artifacts: 'dist/**/*', fingerprint: true
    }
}
```

### 7. Use Timeouts

```groovy
pipeline {
    agent any
    
    options {
        timeout(time: 1, unit: 'HOURS')
    }
    
    stages {
        stage('Build') {
            options {
                timeout(time: 30, unit: 'MINUTES')
            }
            steps {
                sh 'npm run build'
            }
        }
    }
}
```

### 8. Implement Security

- Use credentials for sensitive data
- Restrict access with role-based permissions
- Enable CSRF protection
- Use HTTPS for Jenkins URL
- Regular security updates

## Real-World Examples

### Node.js Application CI/CD

```groovy
pipeline {
    agent any
    
    tools {
        nodejs 'NodeJS 18'
    }
    
    environment {
        DOCKER_REGISTRY = 'docker.io'
        IMAGE_NAME = 'username/myapp'
        DOCKER_CREDS = credentials('docker-hub-credentials')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh 'npm ci'
            }
        }
        
        stage('Lint') {
            steps {
                sh 'npm run lint'
            }
        }
        
        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh 'npm run test:unit'
                    }
                }
                stage('Integration Tests') {
                    steps {
                        sh 'npm run test:integration'
                    }
                }
            }
            post {
                always {
                    junit 'reports/**/*.xml'
                }
            }
        }
        
        stage('Build') {
            steps {
                sh 'npm run build'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}:${env.BUILD_NUMBER}")
                    docker.build("${IMAGE_NAME}:latest")
                }
            }
        }
        
        stage('Push Docker Image') {
            when {
                branch 'main'
            }
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-hub-credentials') {
                        docker.image("${IMAGE_NAME}:${env.BUILD_NUMBER}").push()
                        docker.image("${IMAGE_NAME}:latest").push()
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                sh '''
                    kubectl set image deployment/myapp \
                        myapp=${IMAGE_NAME}:${BUILD_NUMBER} \
                        -n staging
                '''
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to production?', ok: 'Deploy'
                sh '''
                    kubectl set image deployment/myapp \
                        myapp=${IMAGE_NAME}:${BUILD_NUMBER} \
                        -n production
                '''
            }
        }
    }
    
    post {
        success {
            slackSend(
                color: 'good',
                message: "Build Successful: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
        failure {
            slackSend(
                color: 'danger',
                message: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
        always {
            cleanWs()
        }
    }
}
```

### Multi-Branch Pipeline

```groovy
// Jenkinsfile for multi-branch pipeline
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                echo "Building branch: ${env.BRANCH_NAME}"
                sh 'npm run build'
            }
        }
        
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    if (env.BRANCH_NAME == 'main') {
                        sh './deploy-production.sh'
                    } else if (env.BRANCH_NAME == 'develop') {
                        sh './deploy-staging.sh'
                    } else {
                        echo 'No deployment for feature branches'
                    }
                }
            }
        }
    }
}
```

## Troubleshooting

### Common Issues

#### Jenkins Won't Start
```bash
# Check service status
sudo systemctl status jenkins

# Check logs
sudo journalctl -u jenkins -n 50

# Check Java version
java -version
```

#### Build Fails with Permission Denied
```bash
# Add Jenkins user to docker group
sudo usermod -aG docker jenkins

# Restart Jenkins
sudo systemctl restart jenkins
```

#### Agent Disconnected
- Check network connectivity
- Verify SSH credentials
- Check agent logs
- Increase agent timeout

#### Out of Memory
```bash
# Edit Jenkins service file
sudo vim /etc/default/jenkins

# Increase heap size
JAVA_ARGS="-Xmx2048m -Xms512m"

# Restart Jenkins
sudo systemctl restart jenkins
```

### Debugging Pipelines

```groovy
pipeline {
    agent any
    
    stages {
        stage('Debug') {
            steps {
                // Print all environment variables
                sh 'printenv | sort'
                
                // Print workspace
                sh 'pwd'
                sh 'ls -la'
                
                // Check available commands
                sh 'which git'
                sh 'which docker'
            }
        }
    }
}
```

### Viewing Logs

```bash
# Jenkins main log
tail -f /var/log/jenkins/jenkins.log

# Specific build log
# Access via: http://localhost:8080/job/[job-name]/[build-number]/console
```

## Resources

- [Official Jenkins Documentation](https://www.jenkins.io/doc/)
- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [Jenkins Plugin Index](https://plugins.jenkins.io/)
- [Jenkins Tutorial](https://www.jenkins.io/doc/tutorials/)
- [CloudBees Jenkins Resources](https://www.cloudbees.com/jenkins/resources)
- [Awesome Jenkins](https://github.com/sahilsk/awesome-jenkins)

---

**Congratulations!** You've completed the learning repository tour. Continue practicing with these technologies to master DevOps!
