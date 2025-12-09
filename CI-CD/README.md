# CI/CD Pipelines Complete Guide

## Table of Contents
- [Introduction](#introduction)
- [What is CI/CD?](#what-is-cicd)
- [Key Concepts](#key-concepts)
- [CI/CD Pipeline Stages](#cicd-pipeline-stages)
- [CI/CD Tools Comparison](#cicd-tools-comparison)
- [Jenkins Pipelines](#jenkins-pipelines)
- [GitHub Actions Workflows](#github-actions-workflows)
- [Jenkins vs GitHub Actions](#jenkins-vs-github-actions)
- [Pipeline Design Patterns](#pipeline-design-patterns)
- [Testing Strategies](#testing-strategies)
- [Deployment Strategies](#deployment-strategies)
- [Security in CI/CD](#security-in-cicd)
- [Monitoring and Observability](#monitoring-and-observability)
- [Real-World Examples](#real-world-examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Introduction

CI/CD (Continuous Integration/Continuous Delivery) is a modern software development practice that enables teams to deliver code changes more frequently and reliably. This guide covers comprehensive CI/CD pipeline implementation using both **Jenkins** and **GitHub Actions**.

## What is CI/CD?

### Continuous Integration (CI)

Continuous Integration is the practice of automatically integrating code changes from multiple contributors into a single software project.

**Key Principles:**
- Developers commit code frequently (multiple times per day)
- Each commit triggers an automated build
- Automated tests run on every build
- Failures are detected and fixed quickly
- Main branch always remains in a deployable state

### Continuous Delivery (CD)

Continuous Delivery extends CI by automatically deploying all code changes to a testing or production environment after the build stage.

**Key Principles:**
- Automated deployment pipeline
- Code is always in a deployable state
- Releases are low-risk events
- Fast feedback loops
- Manual approval for production (optional)

### Continuous Deployment

Continuous Deployment goes one step further by automatically deploying every change that passes the pipeline to production without manual intervention.

### Benefits

- ✅ **Faster Time to Market**: Automated pipelines speed up releases
- ✅ **Improved Code Quality**: Automated testing catches bugs early
- ✅ **Reduced Risk**: Small, frequent releases are easier to debug
- ✅ **Better Collaboration**: Clear feedback on code changes
- ✅ **Increased Productivity**: Automation frees developers from manual tasks
- ✅ **Consistent Environments**: Standardized build and deployment processes

## Key Concepts

### Pipeline

A **pipeline** is an automated sequence of stages that code goes through from commit to deployment.

```
Code Commit → Build → Test → Deploy → Monitor
```

### Stage

A **stage** is a logical group of related steps in a pipeline (e.g., Build, Test, Deploy).

### Job

A **job** is a set of steps that execute on the same runner/agent.

### Step

A **step** is an individual task within a job (e.g., run a command, execute a script).

### Artifact

An **artifact** is a file or set of files produced by a build (e.g., compiled binaries, Docker images).

### Environment

An **environment** is a deployment target (e.g., development, staging, production).

### Runner/Agent

A **runner** (GitHub Actions) or **agent** (Jenkins) is a server that executes pipeline jobs.

### Trigger

A **trigger** is an event that starts a pipeline (e.g., push, pull request, schedule).

## CI/CD Pipeline Stages

### 1. Source Stage

**Purpose**: Retrieve code from version control

**Activities:**
- Clone repository
- Checkout specific branch/commit
- Fetch dependencies metadata

**Example (GitHub Actions):**
```yaml
- name: Checkout code
  uses: actions/checkout@v3
```

**Example (Jenkins):**
```groovy
stage('Checkout') {
    steps {
        checkout scm
    }
}
```

### 2. Build Stage

**Purpose**: Compile code and create deployable artifacts

**Activities:**
- Install dependencies
- Compile source code
- Create executable/package
- Generate documentation

**Example (GitHub Actions):**
```yaml
- name: Build
  run: |
    npm ci
    npm run build
```

**Example (Jenkins):**
```groovy
stage('Build') {
    steps {
        sh 'npm ci'
        sh 'npm run build'
    }
}
```

### 3. Test Stage

**Purpose**: Verify code quality and functionality

**Activities:**
- Unit tests
- Integration tests
- E2E tests
- Code coverage analysis
- Static code analysis (linting)
- Security scanning

**Example (GitHub Actions):**
```yaml
- name: Test
  run: |
    npm run lint
    npm run test:unit
    npm run test:integration
```

**Example (Jenkins):**
```groovy
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
}
```

### 4. Package Stage

**Purpose**: Create deployable artifacts

**Activities:**
- Build Docker images
- Create deployment packages
- Version artifacts
- Tag releases

**Example (GitHub Actions):**
```yaml
- name: Build Docker Image
  run: |
    docker build -t myapp:${{ github.sha }} .
    docker tag myapp:${{ github.sha }} myapp:latest
```

**Example (Jenkins):**
```groovy
stage('Package') {
    steps {
        script {
            docker.build("myapp:${env.BUILD_NUMBER}")
        }
    }
}
```

### 5. Deploy Stage

**Purpose**: Release application to target environment

**Activities:**
- Deploy to staging/production
- Run smoke tests
- Update infrastructure
- Database migrations

**Example (GitHub Actions):**
```yaml
- name: Deploy to Production
  if: github.ref == 'refs/heads/main'
  run: |
    kubectl apply -f k8s/
    kubectl set image deployment/myapp myapp=myapp:${{ github.sha }}
```

**Example (Jenkins):**
```groovy
stage('Deploy') {
    when {
        branch 'main'
    }
    steps {
        sh 'kubectl apply -f k8s/'
        sh "kubectl set image deployment/myapp myapp=myapp:${env.BUILD_NUMBER}"
    }
}
```

### 6. Monitor Stage

**Purpose**: Track application health and performance

**Activities:**
- Health checks
- Performance monitoring
- Log aggregation
- Alerting
- Rollback if needed

## CI/CD Tools Comparison

### Popular CI/CD Tools

| Tool | Type | Hosting | Best For |
|------|------|---------|----------|
| **GitHub Actions** | Cloud-native | GitHub-hosted | GitHub projects, modern workflows |
| **Jenkins** | Self-hosted | Self-hosted/Cloud | Enterprise, complex pipelines |
| **GitLab CI/CD** | Integrated | GitLab-hosted | GitLab users, all-in-one platform |
| **CircleCI** | Cloud-native | Cloud-hosted | Fast builds, Docker support |
| **Travis CI** | Cloud-native | Cloud-hosted | Open source projects |
| **Azure Pipelines** | Cloud-native | Azure-hosted | Microsoft ecosystem |
| **AWS CodePipeline** | Cloud-native | AWS-hosted | AWS infrastructure |

### Choosing the Right Tool

**Choose GitHub Actions if:**
- Your code is on GitHub
- You want tight GitHub integration
- You prefer cloud-hosted runners
- You want a modern, YAML-based syntax

**Choose Jenkins if:**
- You need complete control over infrastructure
- You have complex, customized pipelines
- You want self-hosted runners
- You have existing Jenkins infrastructure

## Jenkins Pipelines

### Jenkins Pipeline Basics

Jenkins pipelines are defined using **Declarative** or **Scripted** syntax in a `Jenkinsfile`.

### Declarative Pipeline Structure

```groovy
pipeline {
    agent any
    
    environment {
        // Environment variables
        NODE_ENV = 'production'
    }
    
    stages {
        stage('Build') {
            steps {
                // Build steps
            }
        }
        
        stage('Test') {
            steps {
                // Test steps
            }
        }
        
        stage('Deploy') {
            steps {
                // Deploy steps
            }
        }
    }
    
    post {
        always {
            // Cleanup
        }
        success {
            // On success
        }
        failure {
            // On failure
        }
    }
}
```

### Complete Jenkins Pipeline Example

```groovy
pipeline {
    agent any
    
    tools {
        nodejs 'NodeJS 18'
    }
    
    environment {
        DOCKER_REGISTRY = 'docker.io'
        IMAGE_NAME = 'mycompany/myapp'
        DEPLOY_ENV = "${env.BRANCH_NAME == 'main' ? 'production' : 'staging'}"
    }
    
    options {
        // Pipeline options
        timeout(time: 1, unit: 'HOURS')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git rev-parse --short HEAD > commit-id.txt'
                script {
                    env.COMMIT_ID = readFile('commit-id.txt').trim()
                }
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh 'npm ci'
            }
        }
        
        stage('Code Quality') {
            parallel {
                stage('Lint') {
                    steps {
                        sh 'npm run lint'
                    }
                }
                stage('Security Scan') {
                    steps {
                        sh 'npm audit --audit-level=moderate'
                    }
                }
            }
        }
        
        stage('Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh 'npm run test:unit -- --coverage'
                        junit 'reports/junit.xml'
                        publishHTML([
                            reportDir: 'coverage',
                            reportFiles: 'index.html',
                            reportName: 'Coverage Report'
                        ])
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
        
        stage('Build') {
            steps {
                sh 'npm run build'
                archiveArtifacts artifacts: 'dist/**/*', fingerprint: true
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build(
                        "${IMAGE_NAME}:${COMMIT_ID}",
                        "--build-arg BUILD_DATE=${BUILD_TIMESTAMP} ."
                    )
                    docker.build("${IMAGE_NAME}:latest")
                }
            }
        }
        
        stage('Push Docker Image') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-credentials') {
                        dockerImage.push("${COMMIT_ID}")
                        dockerImage.push('latest')
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                script {
                    sh """
                        kubectl config use-context staging
                        kubectl set image deployment/myapp \\
                            myapp=${IMAGE_NAME}:${COMMIT_ID} \\
                            -n staging
                        kubectl rollout status deployment/myapp -n staging
                    """
                }
            }
        }
        
        stage('Approval for Production') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to production?', 
                      ok: 'Deploy',
                      submitter: 'admin,devops'
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh """
                        kubectl config use-context production
                        kubectl set image deployment/myapp \\
                            myapp=${IMAGE_NAME}:${COMMIT_ID} \\
                            -n production
                        kubectl rollout status deployment/myapp -n production
                    """
                }
            }
        }
        
        stage('Smoke Tests') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                sh """
                    npm run test:smoke -- --env=${DEPLOY_ENV}
                """
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded!'
            slackSend(
                color: 'good',
                message: "Build Successful: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
        failure {
            echo 'Pipeline failed!'
            slackSend(
                color: 'danger',
                message: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
    }
}
```

### Jenkins with Docker Agent

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

### Jenkins Multi-Branch Pipeline

```groovy
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
                    } else if (env.BRANCH_NAME.startsWith('feature/')) {
                        sh './deploy-preview.sh'
                    }
                }
            }
        }
    }
}
```

## GitHub Actions Workflows

### GitHub Actions Basics

GitHub Actions workflows are defined in YAML files in the `.github/workflows` directory.

### Basic Workflow Structure

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
```

### Complete GitHub Actions Workflow Example

```yaml
name: Complete CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        type: choice
        options:
          - staging
          - production

env:
  NODE_VERSION: '18'
  DOCKER_REGISTRY: docker.io
  IMAGE_NAME: mycompany/myapp

jobs:
  # Job 1: Code Quality and Security
  quality:
    name: Code Quality & Security
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Lint code
        run: npm run lint
      
      - name: Security audit
        run: npm audit --audit-level=moderate
      
      - name: Run SonarQube scan
        uses: sonarsource/sonarqube-scan-action@master
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
  
  # Job 2: Test Suite
  test:
    name: Test Suite
    runs-on: ubuntu-latest
    needs: quality
    
    strategy:
      matrix:
        test-type: [unit, integration, e2e]
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run ${{ matrix.test-type }} tests
        run: npm run test:${{ matrix.test-type }}
      
      - name: Upload coverage
        if: matrix.test-type == 'unit'
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
          flags: unittests
  
  # Job 3: Build Application
  build:
    name: Build Application
    runs-on: ubuntu-latest
    needs: test
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build application
        run: npm run build
      
      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build-artifacts
          path: dist/
          retention-days: 7
  
  # Job 4: Build and Push Docker Image
  docker:
    name: Build & Push Docker Image
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name == 'push'
    
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=sha,prefix={{branch}}-
            type=semver,pattern={{version}}
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
  
  # Job 5: Deploy to Staging
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: docker
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.example.com
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG_STAGING }}
      
      - name: Deploy to Kubernetes
        run: |
          kubectl apply -f k8s/staging/
          kubectl set image deployment/myapp \\
            myapp=${{ needs.docker.outputs.image-tag }} \\
            -n staging
          kubectl rollout status deployment/myapp -n staging
      
      - name: Run smoke tests
        run: npm run test:smoke -- --env=staging
  
  # Job 6: Deploy to Production
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: docker
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://example.com
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG_PRODUCTION }}
      
      - name: Deploy to Kubernetes
        run: |
          kubectl apply -f k8s/production/
          kubectl set image deployment/myapp \\
            myapp=${{ needs.docker.outputs.image-tag }} \\
            -n production
          kubectl rollout status deployment/myapp -n production
      
      - name: Run smoke tests
        run: npm run test:smoke -- --env=production
      
      - name: Create GitHub Release
        if: startsWith(github.ref, 'refs/tags/')
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          draft: false
          prerelease: false
  
  # Job 7: Notification
  notify:
    name: Send Notifications
    runs-on: ubuntu-latest
    needs: [deploy-staging, deploy-production]
    if: always()
    
    steps:
      - name: Notify Slack
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Deployment completed'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### GitHub Actions with Matrix Strategy

```yaml
name: Multi-Platform Build

on: [push]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [16, 18, 20]
        exclude:
          - os: windows-latest
            node-version: 16
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
      
      - name: Install and test
        run: |
          npm ci
          npm test
```

### GitHub Actions Reusable Workflows

**`.github/workflows/reusable-build.yml`:**
```yaml
name: Reusable Build Workflow

on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string
    secrets:
      npm-token:
        required: true

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ inputs.node-version }}
      
      - name: Build
        env:
          NPM_TOKEN: ${{ secrets.npm-token }}
        run: |
          npm ci
          npm run build
```

**Using the reusable workflow:**
```yaml
name: Main Pipeline

on: [push]

jobs:
  build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      node-version: '18'
    secrets:
      npm-token: ${{ secrets.NPM_TOKEN }}
```

## Jenkins vs GitHub Actions

### Feature Comparison

| Feature | Jenkins | GitHub Actions |
|---------|---------|----------------|
| **Hosting** | Self-hosted (or cloud) | GitHub-hosted (or self-hosted) |
| **Configuration** | Jenkinsfile (Groovy) | YAML workflow files |
| **Integration** | Requires plugins | Native GitHub integration |
| **Runners** | Custom agents | GitHub runners or self-hosted |
| **Cost** | Infrastructure costs | Free for public repos, usage-based for private |
| **Learning Curve** | Steeper | Easier |
| **Flexibility** | Very high | High |
| **Plugins** | 1800+ plugins | Growing marketplace |
| **Community** | Large, established | Growing rapidly |
| **UI** | Classic/Blue Ocean | Modern GitHub UI |

### Syntax Comparison

**Jenkins (Declarative):**
```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'npm run build'
            }
        }
    }
}
```

**GitHub Actions:**
```yaml
name: Build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm run build
```

### When to Use Each

**Use Jenkins when:**
- You need complete infrastructure control
- You have complex, custom pipeline requirements
- You're already invested in Jenkins ecosystem
- You need to support legacy systems
- You require extensive plugin customization

**Use GitHub Actions when:**
- Your code is on GitHub
- You want easy setup and maintenance
- You prefer cloud-native solutions
- You want tight GitHub integration
- You're building modern applications

### Migration from Jenkins to GitHub Actions

**Jenkins Jenkinsfile:**
```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
                sh 'npm run build'
            }
        }
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
    }
}
```

**Equivalent GitHub Actions:**
```yaml
name: CI
on: [push]
jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install
      - run: npm run build
      - run: npm test
```

## Pipeline Design Patterns

### 1. Trunk-Based Development

**Strategy:** All developers work on a single branch (main/trunk) with short-lived feature branches.

```yaml
# GitHub Actions
name: Trunk-Based CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm test
      - run: npm run build
```

### 2. GitFlow

**Strategy:** Structured branching model with main, develop, feature, release, and hotfix branches.

```groovy
// Jenkins
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'npm run build'
            }
        }
        stage('Deploy to Staging') {
            when { branch 'develop' }
            steps {
                sh './deploy-staging.sh'
            }
        }
        stage('Deploy to Production') {
            when { branch 'main' }
            steps {
                input 'Deploy to production?'
                sh './deploy-production.sh'
            }
        }
    }
}
```

### 3. Feature Branch Workflow

**Strategy:** Each feature is developed in a dedicated branch and merged via pull request.

```yaml
# GitHub Actions
name: Feature Branch CI
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build
```

### 4. Monorepo Pipeline

**Strategy:** Multiple projects in a single repository with selective builds.

```yaml
# GitHub Actions
name: Monorepo CI
on:
  push:
    paths:
      - 'packages/**'

jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      packages: ${{ steps.filter.outputs.changes }}
    steps:
      - uses: actions/checkout@v3
      - uses: dorny/paths-filter@v2
        id: filter
        with:
          filters: |
            package-a:
              - 'packages/a/**'
            package-b:
              - 'packages/b/**'
  
  build:
    needs: changes
    runs-on: ubuntu-latest
    strategy:
      matrix:
        package: ${{ fromJSON(needs.changes.outputs.packages) }}
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npm run build --workspace=packages/${{ matrix.package }}
```

### 5. Blue-Green Deployment Pipeline

```yaml
# GitHub Actions
name: Blue-Green Deployment

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Green Environment
        run: |
          kubectl apply -f k8s/green/
          kubectl wait --for=condition=available deployment/myapp-green
      
      - name: Run Health Checks
        run: ./health-check.sh green
      
      - name: Switch Traffic to Green
        run: kubectl patch service myapp -p '{"spec":{"selector":{"version":"green"}}}'
      
      - name: Monitor for 5 minutes
        run: sleep 300
      
      - name: Cleanup Blue Environment
        run: kubectl delete -f k8s/blue/
```

## Testing Strategies

### Test Pyramid

```
        /\\
       /  \\
      / E2E \\
     /______\\
    /        \\
   / Integration\\
  /_____________\\
 /               \\
/   Unit Tests   \\
/__________________\\
```

### 1. Unit Tests

**Purpose:** Test individual components in isolation

```yaml
# GitHub Actions
- name: Unit Tests
  run: |
    npm run test:unit -- --coverage
    npm run test:unit -- --watch=false
```

```groovy
// Jenkins
stage('Unit Tests') {
    steps {
        sh 'npm run test:unit -- --coverage'
        junit 'reports/junit.xml'
        publishHTML([
            reportDir: 'coverage',
            reportFiles: 'index.html',
            reportName: 'Coverage Report'
        ])
    }
}
```

### 2. Integration Tests

**Purpose:** Test interaction between components

```yaml
# GitHub Actions with Docker Compose
- name: Integration Tests
  run: |
    docker-compose up -d
    npm run test:integration
    docker-compose down
```

### 3. End-to-End Tests

**Purpose:** Test complete user workflows

```yaml
# GitHub Actions with Playwright
- name: E2E Tests
  run: |
    npx playwright install
    npm run test:e2e
    
- name: Upload test results
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: playwright-report
    path: playwright-report/
```

### 4. Performance Tests

```groovy
// Jenkins with k6
stage('Performance Tests') {
    steps {
        sh 'k6 run --vus 10 --duration 30s load-test.js'
    }
}
```

### 5. Security Tests

```yaml
# GitHub Actions with Snyk
- name: Security Scan
  uses: snyk/actions/node@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
  with:
    args: --severity-threshold=high
```

## Deployment Strategies

### 1. Rolling Deployment

Gradually replace old version with new version.

```yaml
# Kubernetes Rolling Update
- name: Rolling Deployment
  run: |
    kubectl set image deployment/myapp \\
      myapp=myapp:${{ github.sha }} \\
      --record
    kubectl rollout status deployment/myapp
```

### 2. Blue-Green Deployment

Two identical environments, switch traffic between them.

```yaml
- name: Blue-Green Deploy
  run: |
    # Deploy to green
    kubectl apply -f k8s/green/
    
    # Test green
    ./test-green.sh
    
    # Switch traffic
    kubectl patch service myapp \\
      -p '{"spec":{"selector":{"version":"green"}}}'
```

### 3. Canary Deployment

Gradually roll out to a subset of users.

```yaml
- name: Canary Deployment
  run: |
    # Deploy canary with 10% traffic
    kubectl apply -f k8s/canary-10percent.yaml
    
    # Monitor metrics
    sleep 300
    
    # If metrics good, increase to 50%
    kubectl apply -f k8s/canary-50percent.yaml
    
    # Monitor again
    sleep 300
    
    # Full rollout
    kubectl apply -f k8s/production.yaml
```

### 4. Feature Flags

Deploy code but control feature availability.

```yaml
- name: Deploy with Feature Flags
  env:
    FEATURE_NEW_UI: ${{ secrets.FEATURE_NEW_UI }}
  run: |
    kubectl set env deployment/myapp \\
      FEATURE_NEW_UI=$FEATURE_NEW_UI
```

### 5. A/B Testing

Test two versions simultaneously with different user groups.

```yaml
- name: A/B Deployment
  run: |
    # Deploy version A (50% traffic)
    kubectl apply -f k8s/version-a.yaml
    
    # Deploy version B (50% traffic)
    kubectl apply -f k8s/version-b.yaml
    
    # Monitor metrics and choose winner
```

## Security in CI/CD

### 1. Secrets Management

**GitHub Actions:**
```yaml
jobs:
  deploy:
    steps:
      - name: Use secrets
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
        run: ./deploy.sh
```

**Jenkins:**
```groovy
environment {
    API_KEY = credentials('api-key-id')
    DB_PASSWORD = credentials('db-password-id')
}
```

### 2. Dependency Scanning

```yaml
# GitHub Actions with npm audit
- name: Security Audit
  run: |
    npm audit --audit-level=moderate
    npm audit fix
```

### 3. Container Scanning

```yaml
# Trivy container scanner
- name: Scan Docker Image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:${{ github.sha }}
    format: 'sarif'
    output: 'trivy-results.sarif'

- name: Upload scan results
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: 'trivy-results.sarif'
```

### 4. Code Scanning

```yaml
# CodeQL Analysis
- name: Initialize CodeQL
  uses: github/codeql-action/init@v2
  with:
    languages: javascript

- name: Perform CodeQL Analysis
  uses: github/codeql-action/analyze@v2
```

### 5. SAST (Static Application Security Testing)

```groovy
// Jenkins with SonarQube
stage('Security Scan') {
    steps {
        withSonarQubeEnv('SonarQube') {
            sh 'sonar-scanner'
        }
    }
}
```

### 6. Least Privilege Principle

```yaml
# GitHub Actions with minimal permissions
permissions:
  contents: read
  pull-requests: write
  issues: write
```

### 7. Signed Commits

```yaml
- name: Verify Signed Commits
  run: |
    git verify-commit HEAD
```

## Monitoring and Observability

### 1. Pipeline Metrics

**Key Metrics to Track:**
- Build duration
- Build success rate
- Deployment frequency
- Mean time to recovery (MTTR)
- Change failure rate
- Lead time for changes

### 2. Application Monitoring

```yaml
# Deploy with monitoring
- name: Deploy and Monitor
  run: |
    kubectl apply -f k8s/
    
    # Wait for deployment
    kubectl rollout status deployment/myapp
    
    # Check health endpoint
    curl -f https://myapp.com/health || exit 1
    
    # Check metrics
    curl -f https://myapp.com/metrics || exit 1
```

### 3. Log Aggregation

```yaml
- name: Configure Logging
  run: |
    kubectl apply -f k8s/fluentd.yaml
    kubectl apply -f k8s/elasticsearch.yaml
    kubectl apply -f k8s/kibana.yaml
```

### 4. Alerting

```groovy
// Jenkins with Slack notifications
post {
    failure {
        slackSend(
            color: 'danger',
            message: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}\\n${env.BUILD_URL}"
        )
    }
    success {
        slackSend(
            color: 'good',
            message: "Build Successful: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        )
    }
}
```

### 5. Distributed Tracing

```yaml
- name: Deploy with OpenTelemetry
  env:
    OTEL_EXPORTER_OTLP_ENDPOINT: ${{ secrets.OTEL_ENDPOINT }}
  run: |
    kubectl apply -f k8s/otel-collector.yaml
```

## Real-World Examples

### Example 1: Microservices CI/CD

```yaml
name: Microservices Pipeline

on:
  push:
    branches: [main]
    paths:
      - 'services/**'

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      services: ${{ steps.filter.outputs.changes }}
    steps:
      - uses: actions/checkout@v3
      - uses: dorny/paths-filter@v2
        id: filter
        with:
          filters: |
            auth:
              - 'services/auth/**'
            api:
              - 'services/api/**'
            frontend:
              - 'services/frontend/**'
  
  build-and-deploy:
    needs: detect-changes
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: ${{ fromJSON(needs.detect-changes.outputs.services) }}
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Build ${{ matrix.service }}
        run: |
          cd services/${{ matrix.service }}
          docker build -t ${{ matrix.service }}:${{ github.sha }} .
      
      - name: Test ${{ matrix.service }}
        run: |
          cd services/${{ matrix.service }}
          npm test
      
      - name: Deploy ${{ matrix.service }}
        run: |
          kubectl set image deployment/${{ matrix.service }} \\
            ${{ matrix.service }}=${{ matrix.service }}:${{ github.sha }}
```

### Example 2: Infrastructure as Code Pipeline

```yaml
name: Terraform CI/CD

on:
  push:
    branches: [main]
    paths:
      - 'terraform/**'
  pull_request:
    branches: [main]

jobs:
  terraform:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
      
      - name: Terraform Format Check
        run: terraform fmt -check
        working-directory: terraform
      
      - name: Terraform Init
        run: terraform init
        working-directory: terraform
      
      - name: Terraform Validate
        run: terraform validate
        working-directory: terraform
      
      - name: Terraform Plan
        run: terraform plan -out=tfplan
        working-directory: terraform
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      
      - name: Terraform Apply
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        run: terraform apply -auto-approve tfplan
        working-directory: terraform
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

### Example 3: Mobile App CI/CD

```groovy
// Jenkins Pipeline for React Native
pipeline {
    agent any
    
    environment {
        ANDROID_HOME = '/opt/android-sdk'
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
            steps {
                sh 'npm test'
            }
        }
        
        stage('Build Android') {
            steps {
                sh 'cd android && ./gradlew assembleRelease'
            }
        }
        
        stage('Build iOS') {
            steps {
                sh '''
                    cd ios
                    pod install
                    xcodebuild -workspace MyApp.xcworkspace \\
                        -scheme MyApp \\
                        -configuration Release \\
                        archive -archivePath MyApp.xcarchive
                '''
            }
        }
        
        stage('Sign and Upload') {
            parallel {
                stage('Android - Play Store') {
                    steps {
                        sh './fastlane android deploy'
                    }
                }
                stage('iOS - App Store') {
                    steps {
                        sh './fastlane ios deploy'
                    }
                }
            }
        }
    }
}
```

### Example 4: Database Migration Pipeline

```yaml
name: Database Migration

on:
  push:
    branches: [main]
    paths:
      - 'migrations/**'

jobs:
  migrate:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Backup Database
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          pg_dump $DATABASE_URL > backup-$(date +%Y%m%d-%H%M%S).sql
      
      - name: Run Migrations
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          npm run migrate:up
      
      - name: Verify Migration
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          npm run migrate:verify
      
      - name: Rollback on Failure
        if: failure()
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          npm run migrate:down
```

## Best Practices

### 1. Version Control Everything

```yaml
# Store pipeline configuration in Git
.github/workflows/
├── ci.yml
├── cd.yml
├── security.yml
└── cleanup.yml
```

### 2. Keep Pipelines Fast

**Strategies:**
- Use caching for dependencies
- Parallelize independent jobs
- Use incremental builds
- Optimize Docker layers

```yaml
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

### 3. Fail Fast

```yaml
strategy:
  fail-fast: true
  matrix:
    node-version: [16, 18, 20]
```

### 4. Make Pipelines Idempotent

Pipelines should produce same result when run multiple times.

```yaml
- name: Deploy (Idempotent)
  run: |
    kubectl apply -f k8s/  # apply is idempotent
```

### 5. Use Infrastructure as Code

```yaml
- name: Provision Infrastructure
  run: |
    terraform init
    terraform apply -auto-approve
```

### 6. Implement Proper Error Handling

```groovy
// Jenkins
try {
    sh 'npm test'
} catch (Exception e) {
    currentBuild.result = 'FAILURE'
    throw e
} finally {
    // Cleanup always runs
    cleanWs()
}
```

### 7. Tag and Version Everything

```yaml
- name: Tag Release
  run: |
    git tag v${{ github.run_number }}
    docker tag myapp:latest myapp:v${{ github.run_number }}
```

### 8. Monitor Pipeline Health

```yaml
- name: Report Metrics
  run: |
    curl -X POST https://metrics.example.com/api/builds \\
      -d '{
        "duration": "${{ job.duration }}",
        "status": "${{ job.status }}",
        "pipeline": "${{ github.workflow }}"
      }'
```

### 9. Document Your Pipelines

```yaml
name: CI Pipeline

# This pipeline runs on every push to main and:
# 1. Runs linters and security scans
# 2. Executes test suite
# 3. Builds Docker image
# 4. Deploys to staging environment

on:
  push:
    branches: [main]
```

### 10. Use Secrets Securely

**Never:**
```yaml
# DON'T DO THIS
- run: echo "API_KEY=secret123" >> .env
```

**Always:**
```yaml
# DO THIS
- name: Configure secrets
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: ./configure.sh
```

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Build Fails Intermittently

**Symptoms:** Pipeline passes sometimes, fails others

**Solutions:**
```yaml
# Add retries
- uses: nick-invision/retry@v2
  with:
    timeout_minutes: 10
    max_attempts: 3
    command: npm test

# Add better error logging
- name: Test with debug
  run: |
    set -x  # Enable debug mode
    npm test
```

#### Issue 2: Slow Pipeline

**Symptoms:** Pipeline takes too long to complete

**Solutions:**
```yaml
# Use caching
- uses: actions/cache@v3
  with:
    path: node_modules
    key: ${{ runner.os }}-deps-${{ hashFiles('package-lock.json') }}

# Parallelize jobs
jobs:
  test-unit:
    runs-on: ubuntu-latest
  test-integration:
    runs-on: ubuntu-latest
  # Run simultaneously
```

#### Issue 3: Deployment Failures

**Symptoms:** Deployment step fails

**Solutions:**
```yaml
# Add health checks
- name: Deploy and verify
  run: |
    kubectl apply -f k8s/
    kubectl rollout status deployment/myapp
    kubectl wait --for=condition=available deployment/myapp --timeout=300s

# Add automatic rollback
- name: Rollback on failure
  if: failure()
  run: |
    kubectl rollout undo deployment/myapp
```

#### Issue 4: Test Flakiness

**Symptoms:** Tests fail randomly

**Solutions:**
```yaml
# Increase timeouts
- name: Run tests with retries
  run: |
    npm test -- --testTimeout=10000 --retries=3

# Run tests in isolation
- name: Run tests serially
  run: |
    npm test -- --runInBand
```

#### Issue 5: Secret Exposure

**Symptoms:** Secrets visible in logs

**Solutions:**
```yaml
# Use secret masking
- name: Use secret safely
  env:
    SECRET_KEY: ${{ secrets.SECRET_KEY }}
  run: |
    # GitHub automatically masks secrets in logs
    echo "Secret is set"
    # NEVER echo the actual secret

# Use temporary files
- name: Configure with secret
  env:
    SECRET: ${{ secrets.SECRET }}
  run: |
    echo "$SECRET" > /tmp/secret
    chmod 600 /tmp/secret
    ./configure.sh /tmp/secret
    rm /tmp/secret
```

### Debugging Tips

#### Enable Debug Logging

**GitHub Actions:**
```yaml
# Set repository secrets:
# ACTIONS_STEP_DEBUG: true
# ACTIONS_RUNNER_DEBUG: true
```

**Jenkins:**
```groovy
pipeline {
    options {
        timestamps()
    }
    stages {
        stage('Debug') {
            steps {
                sh 'set -x'  // Enable shell debug mode
                sh 'env | sort'  // Print environment
            }
        }
    }
}
```

#### Check Pipeline Syntax

**GitHub Actions:**
```bash
# Install actionlint
brew install actionlint

# Validate workflow
actionlint .github/workflows/*.yml
```

**Jenkins:**
```bash
# Use Jenkins Pipeline validator
curl -X POST -F "jenkinsfile=<Jenkinsfile" \\
  http://jenkins-url/pipeline-model-converter/validate
```

## Resources

### Official Documentation
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [CI/CD Best Practices](https://docs.gitlab.com/ee/ci/pipelines/pipeline_efficiency.html)

### Learning Resources
- [Jenkins Pipeline Examples](https://github.com/jenkinsci/pipeline-examples)
- [GitHub Actions Starter Workflows](https://github.com/actions/starter-workflows)
- [Awesome CI/CD](https://github.com/cicdops/awesome-ciandcd)

### Tools and Utilities
- [Jenkins Pipeline Syntax Generator](https://jenkins.io/doc/book/pipeline/syntax/)
- [GitHub Actions Toolkit](https://github.com/actions/toolkit)
- [actionlint - GitHub Actions Linter](https://github.com/rhysd/actionlint)

### Community
- [Jenkins Community](https://www.jenkins.io/participate/)
- [GitHub Community Forum](https://github.community/)
- [DevOps Stack Exchange](https://devops.stackexchange.com/)

---

**Next Steps**: 
- Implement a basic pipeline for your project
- Explore [Docker](../Docker/README.md) for containerization
- Learn [Kubernetes](../Kubernetes/README.md) for orchestration
- Study [Terraform](../Terraform/README.md) for infrastructure automation

**Happy Building!** 🚀 Master CI/CD pipelines and accelerate your software delivery!
