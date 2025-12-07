# GitHub Actions Complete Guide

## Table of Contents
- [Introduction](#introduction)
- [What are GitHub Actions?](#what-are-github-actions)
- [Key Concepts](#key-concepts)
- [Getting Started](#getting-started)
- [Workflow Syntax](#workflow-syntax)
- [Events and Triggers](#events-and-triggers)
- [Jobs and Steps](#jobs-and-steps)
- [Actions Marketplace](#actions-marketplace)
- [Environment Variables and Secrets](#environment-variables-and-secrets)
- [Matrix Builds](#matrix-builds)
- [Caching Dependencies](#caching-dependencies)
- [Artifacts](#artifacts)
- [Real-World Examples](#real-world-examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Introduction

GitHub Actions is a powerful CI/CD platform that allows you to automate your software development workflows directly in your GitHub repository. You can build, test, and deploy your code right from GitHub.

## What are GitHub Actions?

GitHub Actions enables you to:
- **Automate workflows**: Build, test, and deploy code automatically
- **Run on events**: Trigger workflows on push, pull requests, issues, etc.
- **Use community actions**: Leverage thousands of pre-built actions
- **Custom runners**: Run on GitHub-hosted or self-hosted runners
- **Multi-platform**: Support for Linux, Windows, and macOS

### Benefits
- ✅ Integrated with GitHub
- ✅ Free for public repositories
- ✅ Matrix builds for testing across multiple environments
- ✅ Rich marketplace of reusable actions
- ✅ Flexible event-driven architecture

## Key Concepts

### Workflow
A configurable automated process defined in a YAML file that runs one or more jobs.

### Event
A specific activity that triggers a workflow (e.g., push, pull_request, schedule).

### Job
A set of steps that execute on the same runner. Jobs run in parallel by default.

### Step
An individual task that can run commands or actions within a job.

### Action
A reusable unit of code that can be shared and used in workflows.

### Runner
A server that runs your workflows when triggered. Can be GitHub-hosted or self-hosted.

## Getting Started

### Step 1: Create Workflow Directory
```bash
mkdir -p .github/workflows
```

### Step 2: Create Your First Workflow

Create `.github/workflows/hello-world.yml`:

```yaml
name: Hello World

on: [push]

jobs:
  greet:
    runs-on: ubuntu-latest
    
    steps:
      - name: Say hello
        run: echo "Hello, World!"
```

### Step 3: Commit and Push
```bash
git add .github/workflows/hello-world.yml
git commit -m "Add hello world workflow"
git push
```

### Step 4: View Results
Go to your repository on GitHub → Actions tab to see the workflow run.

## Workflow Syntax

### Basic Structure
```yaml
name: Workflow Name              # Name displayed in Actions tab
on: [push, pull_request]         # Events that trigger workflow
jobs:                            # Jobs to run
  job-name:                      # Unique job identifier
    runs-on: ubuntu-latest       # Runner environment
    steps:                       # Steps to execute
      - name: Step name          # Step name
        run: echo "Hello"        # Command to run
```

### Complete Example
```yaml
name: CI Pipeline

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
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm test
      
      - name: Build project
        run: npm run build
```

## Events and Triggers

### Common Events

#### Push Event
```yaml
on:
  push:
    branches:
      - main
      - 'releases/**'
    paths:
      - '**.js'
      - '!docs/**'
```

#### Pull Request Event
```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches:
      - main
```

#### Schedule Event (Cron)
```yaml
on:
  schedule:
    # Runs at 00:00 UTC every day
    - cron: '0 0 * * *'
```

#### Manual Trigger (workflow_dispatch)
```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        default: 'staging'
```

#### Issue Events
```yaml
on:
  issues:
    types: [opened, edited, closed]
```

#### Release Events
```yaml
on:
  release:
    types: [published, created]
```

### Multiple Events
```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
  workflow_dispatch:
```

## Jobs and Steps

### Defining Jobs
```yaml
jobs:
  job1:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Job 1"
  
  job2:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Job 2"
```

### Job Dependencies
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npm run build
  
  test:
    needs: build  # Runs after build completes
    runs-on: ubuntu-latest
    steps:
      - run: npm test
  
  deploy:
    needs: [build, test]  # Runs after both complete
    runs-on: ubuntu-latest
    steps:
      - run: npm run deploy
```

### Conditional Jobs
```yaml
jobs:
  deploy:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying to production"
```

### Step Types

#### Run Commands
```yaml
steps:
  - name: Run multiple commands
    run: |
      echo "Line 1"
      echo "Line 2"
      npm install
      npm test
```

#### Use Actions
```yaml
steps:
  - name: Checkout repository
    uses: actions/checkout@v3
  
  - name: Setup Node.js
    uses: actions/setup-node@v3
    with:
      node-version: '18'
```

#### Conditional Steps
```yaml
steps:
  - name: Only on main branch
    if: github.ref == 'refs/heads/main'
    run: echo "This is the main branch"
  
  - name: Only on success
    if: success()
    run: echo "Previous steps succeeded"
  
  - name: Only on failure
    if: failure()
    run: echo "A step failed"
  
  - name: Always run
    if: always()
    run: echo "This always runs"
```

## Actions Marketplace

### Popular Actions

#### Checkout Code
```yaml
- uses: actions/checkout@v3
  with:
    fetch-depth: 0  # Fetch all history
```

#### Setup Languages
```yaml
# Node.js
- uses: actions/setup-node@v3
  with:
    node-version: '18'

# Python
- uses: actions/setup-python@v4
  with:
    python-version: '3.11'

# Java
- uses: actions/setup-java@v3
  with:
    distribution: 'temurin'
    java-version: '17'

# Go
- uses: actions/setup-go@v4
  with:
    go-version: '1.21'
```

#### Cache Dependencies
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

#### Upload/Download Artifacts
```yaml
# Upload
- uses: actions/upload-artifact@v3
  with:
    name: build-output
    path: dist/

# Download
- uses: actions/download-artifact@v3
  with:
    name: build-output
    path: dist/
```

## Environment Variables and Secrets

### Environment Variables

#### Default Variables
```yaml
steps:
  - name: Use default environment variables
    run: |
      echo "Repository: ${{ github.repository }}"
      echo "Branch: ${{ github.ref }}"
      echo "SHA: ${{ github.sha }}"
      echo "Actor: ${{ github.actor }}"
```

#### Custom Variables
```yaml
env:
  GLOBAL_VAR: "global value"

jobs:
  example:
    runs-on: ubuntu-latest
    env:
      JOB_VAR: "job value"
    steps:
      - name: Use variables
        env:
          STEP_VAR: "step value"
        run: |
          echo "Global: $GLOBAL_VAR"
          echo "Job: $JOB_VAR"
          echo "Step: $STEP_VAR"
```

### Secrets

#### Setting Secrets
1. Go to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add name and value

#### Using Secrets
```yaml
steps:
  - name: Use secret
    env:
      API_KEY: ${{ secrets.API_KEY }}
    run: |
      echo "API Key is set"
      # Don't echo the actual secret!
```

#### Example: Deploy with Secrets
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to server
        env:
          SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
          SERVER_HOST: ${{ secrets.SERVER_HOST }}
        run: |
          echo "$SSH_PRIVATE_KEY" > key.pem
          chmod 600 key.pem
          scp -i key.pem -r dist/* user@$SERVER_HOST:/var/www/
```

## Matrix Builds

### Basic Matrix
```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: [16, 18, 20]
    
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm test
```

### Matrix with Include/Exclude
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node-version: [16, 18, 20]
    include:
      # Add specific combination
      - os: macos-latest
        node-version: 18
    exclude:
      # Exclude specific combination
      - os: windows-latest
        node-version: 16
```

### Fail Fast
```yaml
strategy:
  fail-fast: false  # Continue other jobs if one fails
  matrix:
    node-version: [16, 18, 20]
```

## Caching Dependencies

### Node.js Cache
```yaml
steps:
  - uses: actions/checkout@v3
  
  - uses: actions/setup-node@v3
    with:
      node-version: '18'
      cache: 'npm'
  
  - run: npm ci
  - run: npm test
```

### Custom Cache
```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: |
      ~/.npm
      ~/.cache
    key: ${{ runner.os }}-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-
```

### Python Cache
```yaml
- uses: actions/setup-python@v4
  with:
    python-version: '3.11'
    cache: 'pip'

- run: pip install -r requirements.txt
```

## Artifacts

### Upload Artifacts
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm run build
      
      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: production-files
          path: dist/
          retention-days: 7
```

### Download Artifacts
```yaml
jobs:
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v3
        with:
          name: production-files
          path: dist/
      
      - name: Deploy
        run: ./deploy.sh
```

## Real-World Examples

### Node.js CI/CD Pipeline
```yaml
name: Node.js CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [16, 18, 20]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linter
        run: npm run lint
      
      - name: Run tests
        run: npm test
      
      - name: Build
        run: npm run build
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
  
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to production
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
        run: |
          echo "Deploying to production..."
          npm run deploy
```

### Python CI Pipeline
```yaml
name: Python CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov flake8
      
      - name: Lint with flake8
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
      
      - name: Test with pytest
        run: |
          pytest --cov=./ --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Docker Build and Push
```yaml
name: Docker Build

on:
  push:
    branches: [main]
    tags:
      - 'v*'

jobs:
  docker:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
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
          images: username/app-name
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Multi-Environment Deployment
```yaml
name: Deploy

on:
  push:
    branches:
      - main
      - develop

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Determine environment
        id: env
        run: |
          if [[ "${{ github.ref }}" == "refs/heads/main" ]]; then
            echo "environment=production" >> $GITHUB_OUTPUT
            echo "url=https://prod.example.com" >> $GITHUB_OUTPUT
          else
            echo "environment=staging" >> $GITHUB_OUTPUT
            echo "url=https://staging.example.com" >> $GITHUB_OUTPUT
          fi
      
      - name: Deploy to ${{ steps.env.outputs.environment }}
        uses: actions/deploy-pages@v2
        with:
          environment: ${{ steps.env.outputs.environment }}
          url: ${{ steps.env.outputs.url }}
```

## Best Practices

### 1. Use Specific Action Versions
```yaml
# Good: Pin to specific version
- uses: actions/checkout@v3

# Better: Pin to SHA for security
- uses: actions/checkout@8e5e7e5ab8b370d6c329ec480221332ada57f0ab
```

### 2. Minimize Workflow Runs
```yaml
on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'tests/**'
    paths-ignore:
      - '**.md'
      - 'docs/**'
```

### 3. Use Concurrency Control
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### 4. Secure Secrets Usage
```yaml
# Never expose secrets in logs
- name: Use secret safely
  env:
    TOKEN: ${{ secrets.TOKEN }}
  run: |
    # Use the secret but don't echo it
    curl -H "Authorization: Bearer $TOKEN" https://api.example.com
```

### 5. Set Timeouts
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 30  # Prevent stuck jobs
```

### 6. Use Job Outputs
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
    steps:
      - id: version
        run: echo "version=1.0.0" >> $GITHUB_OUTPUT
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying version ${{ needs.build.outputs.version }}"
```

### 7. Organize Complex Workflows
```yaml
# Split into reusable workflows
name: Main Workflow

on: [push]

jobs:
  test:
    uses: ./.github/workflows/test.yml
  
  build:
    uses: ./.github/workflows/build.yml
    needs: test
```

## Troubleshooting

### Debug Logging
Enable debug logging by setting repository secrets:
- `ACTIONS_STEP_DEBUG`: `true`
- `ACTIONS_RUNNER_DEBUG`: `true`

### Common Issues

#### Issue: Workflow not triggering
**Solution**: Check event filters, branch names, and paths

#### Issue: Permission denied
**Solution**: Update workflow permissions
```yaml
permissions:
  contents: read
  pull-requests: write
```

#### Issue: Secrets not available
**Solution**: Verify secret names and ensure they're set in the correct scope

#### Issue: Cache not working
**Solution**: Verify cache key and paths are correct
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

### Viewing Logs
- Go to Actions tab
- Click on workflow run
- Click on job
- Expand steps to see detailed logs

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Actions Marketplace](https://github.com/marketplace?type=actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [GitHub Actions Examples](https://github.com/actions/starter-workflows)
- [Awesome GitHub Actions](https://github.com/sdras/awesome-actions)

---

**Next Steps**: Explore [Docker](../Docker/README.md) to learn how to containerize your applications!
