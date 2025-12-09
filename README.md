# Learny - Complete DevOps Learning Repository

Welcome to **Learny** - a comprehensive learning repository designed to help you master essential DevOps tools and technologies. Each folder contains detailed, step-by-step guides with practical examples, best practices, and real-world use cases.

## 📚 Table of Contents

This repository covers the following topics:

1. [Git & GitHub](#git--github) - Version control and collaboration
2. [CI/CD Pipelines](#cicd-pipelines) - Complete CI/CD guide with Jenkins and GitHub Actions
3. [GitHub Actions](#github-actions) - CI/CD automation with GitHub
4. [Jenkins](#jenkins) - CI/CD automation server
5. [Docker](#docker) - Containerization platform
6. [Kubernetes](#kubernetes) - Container orchestration
7. [Kafka](#kafka) - Distributed event streaming platform
8. [Terraform](#terraform) - Infrastructure as Code tool

## 🎯 What You'll Learn

### Git & GitHub
Learn version control fundamentals, Git commands, branching strategies, and GitHub collaboration workflows.

**Topics Covered:**
- Git installation and configuration
- Essential Git commands (commit, push, pull, merge)
- Branching and merging strategies
- GitHub workflow (forking, pull requests, code reviews)
- Advanced topics (rebase, cherry-pick, stash, hooks)
- Best practices and troubleshooting

📖 **[Start Learning Git & GitHub →](./Git-GitHub/README.md)**

### CI/CD Pipelines
Master continuous integration and continuous delivery with comprehensive coverage of Jenkins and GitHub Actions.

**Topics Covered:**
- CI/CD fundamentals and concepts
- Complete pipeline stages (source, build, test, package, deploy)
- Jenkins pipelines (Declarative and Scripted)
- GitHub Actions workflows
- Jenkins vs GitHub Actions comparison
- Pipeline design patterns (trunk-based, GitFlow, feature branch)
- Testing strategies (unit, integration, E2E)
- Deployment strategies (rolling, blue-green, canary)
- Security in CI/CD
- Monitoring and observability
- Real-world examples
- Best practices and troubleshooting

📖 **[Start Learning CI/CD Pipelines →](./CI-CD/README.md)**

### GitHub Actions
Master CI/CD automation with GitHub's built-in workflow system.

**Topics Covered:**
- Workflow syntax and structure
- Events and triggers
- Jobs, steps, and actions
- Matrix builds and caching
- Secrets and environment variables
- Real-world pipeline examples
- Best practices and troubleshooting

📖 **[Start Learning GitHub Actions →](./GitHubActions/README.md)**

### Docker
Understand containerization and learn to build, ship, and run applications in containers.

**Topics Covered:**
- Docker fundamentals and architecture
- Working with images and containers
- Dockerfile best practices
- Docker Compose for multi-container applications
- Networking and volumes
- Multi-stage builds
- Security and optimization
- Real-world examples

📖 **[Start Learning Docker →](./Docker/README.md)**

### Kubernetes
Learn container orchestration at scale with Kubernetes.

**Topics Covered:**
- Kubernetes architecture and components
- Pods, Deployments, and Services
- ConfigMaps, Secrets, and Volumes
- Scaling and load balancing
- Ingress and networking
- StatefulSets and DaemonSets
- Best practices for production
- Troubleshooting guides

📖 **[Start Learning Kubernetes →](./Kubernetes/README.md)**

### Jenkins
Master continuous integration and continuous delivery with Jenkins.

**Topics Covered:**
- Jenkins installation and setup
- Creating and managing jobs
- Pipeline as Code (Jenkinsfile)
- Plugin ecosystem
- Distributed builds
- Integration with Docker and Kubernetes
- Security and credentials management
- Real-world CI/CD pipelines

📖 **[Start Learning Jenkins →](./Jenkins/README.md)**

### Kafka
Master distributed event streaming and real-time data pipelines with Apache Kafka.

**Topics Covered:**
- Kafka architecture and core concepts
- Producers and Consumers
- Topics, Partitions, and Consumer Groups
- Kafka Connect and Kafka Streams
- Schema Registry and Avro
- Security and authentication
- Performance tuning and monitoring
- Real-world streaming applications

📖 **[Start Learning Kafka →](./Kafka/README.md)**

### Terraform
Learn Infrastructure as Code and automate cloud resource provisioning with Terraform.

**Topics Covered:**
- Terraform fundamentals and HCL syntax
- Providers and Resources
- Variables, Outputs, and Modules
- State management and backends
- Workspaces and environments
- Best practices for production
- Multi-cloud deployments
- Real-world infrastructure examples

📖 **[Start Learning Terraform →](./Terraform/README.md)**

## 🚀 Getting Started

### Prerequisites
- Basic command-line knowledge
- Understanding of software development concepts
- Willingness to learn and practice

### How to Use This Repository

1. **Start with the Basics**: Begin with Git & GitHub if you're new to version control
2. **Progress Sequentially**: The topics build on each other:
   - Git/GitHub → CI/CD Pipelines → Docker → Kubernetes → Kafka → Terraform
3. **Practice Regularly**: Follow the examples and try them on your own
4. **Experiment**: Modify examples and create your own projects
5. **Build Projects**: Apply what you learn to real-world scenarios

### Recommended Learning Path

```
┌─────────────┐
│ Git & GitHub│
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  CI/CD Pipelines│
│ (Jenkins + GHA) │
└──────┬──────────┘
       │
       ▼
┌─────────────┐
│   Docker    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Kubernetes  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Kafka    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Terraform  │
└─────────────┘
```

## 💡 Tips for Success

1. **Hands-On Practice**: Don't just read - try every command and example
2. **Build Projects**: Apply concepts to real projects
3. **Join Communities**: Engage with DevOps communities online
4. **Stay Updated**: Technologies evolve; keep learning
5. **Document Your Journey**: Keep notes and build a personal knowledge base
6. **Collaborate**: Work on open-source projects to gain experience

## 🛠️ Quick Setup Guides

### Setting Up Your Environment

**Install Git:**
```bash
# macOS
brew install git

# Ubuntu/Debian
sudo apt install git

# Windows
choco install git
```

**Install Docker:**
```bash
# macOS
brew install --cask docker

# Ubuntu
sudo apt install docker.io

# Windows
choco install docker-desktop
```

**Install kubectl (Kubernetes CLI):**
```bash
# macOS
brew install kubectl

# Linux (verify checksum after download)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
# Verify the binary (optional but recommended)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check

# Windows
choco install kubernetes-cli
```

## 📖 Additional Resources

### Official Documentation
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com)
- [Docker Documentation](https://docs.docker.com)
- [Kubernetes Documentation](https://kubernetes.io/docs)
- [Jenkins Documentation](https://www.jenkins.io/doc)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Terraform Documentation](https://www.terraform.io/docs)

### Learning Platforms
- [GitHub Learning Lab](https://lab.github.com)
- [Docker Playground](https://labs.play-with-docker.com)
- [Kubernetes Playground](https://labs.play-with-k8s.com)

### Community
- [DevOps Subreddit](https://reddit.com/r/devops)
- [Stack Overflow](https://stackoverflow.com)
- [DevOps Chat Communities](https://devops.com/community)

## 🤝 Contributing

This is a learning repository, and contributions are welcome! If you find errors, want to add more examples, or improve explanations:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This repository is created for educational purposes. Feel free to use, share, and modify the content for learning.

## ⭐ Support

If you find this repository helpful:
- ⭐ Star this repository
- 🍴 Fork it to customize for your needs
- 📢 Share it with others learning DevOps
- 💬 Provide feedback or suggestions

## 📞 Contact

Have questions or suggestions? Feel free to:
- Open an issue
- Start a discussion
- Contribute improvements

---

**Happy Learning!** 🚀 Start your DevOps journey today!

## 🗺️ Repository Structure

```
Learny/
├── Git-GitHub/
│   └── README.md          # Complete Git & GitHub guide
├── CI-CD/
│   └── README.md          # Complete CI/CD Pipelines guide (Jenkins + GitHub Actions)
├── GitHubActions/
│   └── README.md          # Complete GitHub Actions guide
├── Jenkins/
│   └── README.md          # Complete Jenkins guide
├── Docker/
│   └── README.md          # Complete Docker guide
├── Kubernetes/
│   └── README.md          # Complete Kubernetes guide
├── Kafka/
│   └── README.md          # Complete Apache Kafka guide
├── Terraform/
│   └── README.md          # Complete Terraform guide
└── README.md              # This file
```

---

**Version:** 1.0.0  
**Last Updated:** December 2024  
**Maintained by:** kyashwanth-dev