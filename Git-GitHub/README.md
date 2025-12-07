# Git & GitHub Complete Guide

## Table of Contents
- [Introduction](#introduction)
- [What is Git?](#what-is-git)
- [What is GitHub?](#what-is-github)
- [Installing Git](#installing-git)
- [Basic Git Concepts](#basic-git-concepts)
- [Git Configuration](#git-configuration)
- [Essential Git Commands](#essential-git-commands)
- [Working with Branches](#working-with-branches)
- [GitHub Workflow](#github-workflow)
- [Collaboration on GitHub](#collaboration-on-github)
- [Advanced Git Topics](#advanced-git-topics)
- [Best Practices](#best-practices)

## Introduction

Git is a distributed version control system that helps developers track changes in their code, collaborate with others, and manage different versions of their projects. GitHub is a cloud-based hosting service that lets you manage Git repositories.

## What is Git?

Git is a **distributed version control system** created by Linus Torvalds in 2005. Key features include:

- **Distributed Architecture**: Every developer has a complete copy of the repository
- **Fast Performance**: Most operations are performed locally
- **Branching & Merging**: Easy creation and merging of branches
- **Data Integrity**: Uses SHA-1 hashing to ensure data integrity
- **Staging Area**: Allows you to format commits exactly how you want

## What is GitHub?

GitHub is a **web-based hosting service** for Git repositories. It provides:

- Remote repository hosting
- Collaboration tools (Pull Requests, Issues, Projects)
- Code review capabilities
- CI/CD integration
- Documentation hosting (GitHub Pages)
- Social coding features

## Installing Git

### Windows
```bash
# Download from https://git-scm.com/download/win
# Or use Chocolatey
choco install git
```

### macOS
```bash
# Using Homebrew
brew install git

# Or download from https://git-scm.com/download/mac
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install git
```

### Verify Installation
```bash
git --version
```

## Basic Git Concepts

### Repository (Repo)
A repository is a directory that contains your project files and the entire history of changes.

### Working Directory
The directory on your local machine where you make changes to your files.

### Staging Area (Index)
A intermediate area where you prepare changes before committing them.

### Commit
A snapshot of your repository at a specific point in time.

### Remote
A version of your repository hosted on a server (like GitHub).

## Git Configuration

### Set Your Identity
```bash
# Set your name
git config --global user.name "Your Name"

# Set your email
git config --global user.email "your.email@example.com"
```

### Set Default Editor
```bash
git config --global core.editor "code --wait"  # VS Code
git config --global core.editor "vim"          # Vim
```

### View Configuration
```bash
# View all settings
git config --list

# View specific setting
git config user.name
```

## Essential Git Commands

### Initialize a Repository
```bash
# Create a new repository
git init

# Clone an existing repository
git clone https://github.com/username/repository.git
```

### Check Status
```bash
# View the status of your working directory
git status

# Short status
git status -s
```

### Add Files to Staging
```bash
# Add specific file
git add filename.txt

# Add all files
git add .

# Add all files with specific extension
git add *.js
```

### Commit Changes
```bash
# Commit with message
git commit -m "Your commit message"

# Add and commit in one step
git commit -am "Your commit message"

# Amend last commit
git commit --amend -m "Updated message"
```

### View History
```bash
# View commit history
git log

# One-line format
git log --oneline

# Graph view
git log --graph --oneline --all

# Show last n commits
git log -n 5
```

### View Differences
```bash
# Show unstaged changes
git diff

# Show staged changes
git diff --staged

# Compare two commits
git diff commit1 commit2
```

## Working with Branches

### Understanding Branches
Branches allow you to work on different features or experiments without affecting the main codebase.

### Branch Commands
```bash
# List all branches
git branch

# Create new branch
git branch feature-name

# Switch to branch
git checkout feature-name

# Create and switch to new branch
git checkout -b feature-name

# Switch branch (Git 2.23+)
git switch feature-name

# Create and switch (Git 2.23+)
git switch -c feature-name

# Delete branch
git branch -d feature-name

# Force delete branch
git branch -D feature-name

# Rename current branch
git branch -m new-name
```

### Merging Branches
```bash
# Merge branch into current branch
git merge feature-name

# Merge with no fast-forward
git merge --no-ff feature-name

# Abort merge if there are conflicts
git merge --abort
```

### Rebasing
```bash
# Rebase current branch onto main
git rebase main

# Interactive rebase (last 3 commits)
git rebase -i HEAD~3

# Continue after resolving conflicts
git rebase --continue

# Abort rebase
git rebase --abort
```

## GitHub Workflow

### Connecting to GitHub

#### Using HTTPS
```bash
# Add remote repository
git remote add origin https://github.com/username/repository.git

# View remotes
git remote -v
```

#### Using SSH
```bash
# Generate SSH key (replace with your actual email)
ssh-keygen -t ed25519 -C "your.email@example.com" -f ~/.ssh/id_ed25519

# Add SSH key to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key to clipboard and add to GitHub settings
cat ~/.ssh/id_ed25519.pub

# Add remote using SSH
git remote add origin git@github.com:username/repository.git
```

### Push Changes
```bash
# Push to remote branch
git push origin branch-name

# Push and set upstream
git push -u origin branch-name

# Push all branches
git push --all

# Force push (use with caution!)
git push --force
```

### Pull Changes
```bash
# Fetch and merge changes
git pull origin main

# Pull with rebase
git pull --rebase origin main
```

### Fetch Changes
```bash
# Fetch changes without merging
git fetch origin

# Fetch all remotes
git fetch --all
```

## Collaboration on GitHub

### Forking a Repository
1. Click "Fork" button on GitHub
2. Clone your fork:
```bash
git clone https://github.com/your-username/repository.git
```
3. Add upstream remote:
```bash
git remote add upstream https://github.com/original-owner/repository.git
```

### Creating Pull Requests

**Step 1**: Create a new branch
```bash
git checkout -b feature-name
```

**Step 2**: Make changes and commit
```bash
git add .
git commit -m "Add new feature"
```

**Step 3**: Push to your fork
```bash
git push origin feature-name
```

**Step 4**: Create Pull Request on GitHub
- Go to your repository on GitHub
- Click "Compare & pull request"
- Fill in title and description
- Submit the pull request

### Keeping Fork Updated
```bash
# Fetch upstream changes
git fetch upstream

# Merge upstream changes into your main branch
git checkout main
git merge upstream/main

# Push updates to your fork
git push origin main
```

## Advanced Git Topics

### Stashing Changes
```bash
# Stash current changes
git stash

# Stash with message
git stash save "Work in progress on feature"

# List stashes
git stash list

# Apply most recent stash
git stash apply

# Apply specific stash
git stash apply stash@{2}

# Apply and remove stash
git stash pop

# Delete stash
git stash drop stash@{0}

# Clear all stashes
git stash clear
```

### Cherry-picking
```bash
# Apply specific commit to current branch
git cherry-pick commit-hash

# Cherry-pick multiple commits
git cherry-pick commit1 commit2

# Cherry-pick without committing
git cherry-pick -n commit-hash
```

### Resetting Changes
```bash
# Soft reset (keep changes in staging)
git reset --soft HEAD~1

# Mixed reset (keep changes in working directory)
git reset HEAD~1

# Hard reset (discard all changes)
git reset --hard HEAD~1

# Reset to specific commit
git reset --hard commit-hash
```

### Tagging
```bash
# Create lightweight tag
git tag v1.0.0

# Create annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# List tags
git tag

# Push tag to remote
git push origin v1.0.0

# Push all tags
git push --tags

# Delete tag locally
git tag -d v1.0.0

# Delete tag remotely
git push origin --delete v1.0.0
```

### Git Hooks
Git hooks are scripts that run automatically on certain Git events.

```bash
# Hooks location
cd .git/hooks/

# Common hooks:
# - pre-commit: Runs before commit
# - post-commit: Runs after commit
# - pre-push: Runs before push
```

Example pre-commit hook:
```bash
#!/bin/sh
# .git/hooks/pre-commit

# Run tests before committing
npm test
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

## Best Practices

### Commit Messages
- Use present tense ("Add feature" not "Added feature")
- First line should be 50 characters or less
- Separate subject from body with a blank line
- Explain what and why, not how

**Example:**
```
Add user authentication feature

Implement JWT-based authentication for the API.
This allows users to securely log in and access protected resources.
```

### Branching Strategy

**GitFlow:**
- `main`: Production-ready code
- `develop`: Development branch
- `feature/*`: New features
- `release/*`: Release preparation
- `hotfix/*`: Critical bug fixes

**GitHub Flow:**
- `main`: Always deployable
- `feature/*`: Feature branches created from main
- Merge via Pull Requests after review

### General Best Practices

1. **Commit Often**: Make small, logical commits
2. **Write Clear Messages**: Explain the purpose of changes
3. **Review Before Commit**: Check what you're committing with `git diff`
4. **Keep Branches Short-lived**: Merge feature branches quickly
5. **Pull Before Push**: Always pull latest changes before pushing
6. **Don't Commit Sensitive Data**: Use `.gitignore` for secrets
7. **Use `.gitignore`**: Exclude build artifacts, dependencies, etc.
8. **Test Before Commit**: Ensure code works before committing

### Common .gitignore Patterns
```gitignore
# Dependencies
node_modules/
vendor/

# Build outputs
dist/
build/
*.exe

# Environment files
.env
.env.local

# IDE files
.vscode/
.idea/
*.swp

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
logs/
```

## Troubleshooting

### Undo Last Commit
```bash
# Keep changes
git reset --soft HEAD~1

# Discard changes
git reset --hard HEAD~1
```

### Resolve Merge Conflicts
```bash
# View conflicted files
git status

# After resolving conflicts in files
git add resolved-file.txt
git commit -m "Resolve merge conflicts"
```

### Recover Deleted Files
```bash
# Restore file from last commit
git checkout HEAD -- filename.txt

# Restore all files
git checkout -- .
```

### Clean Untracked Files
```bash
# Show what would be deleted
git clean -n

# Delete untracked files
git clean -f

# Delete directories too
git clean -fd
```

## Resources

- [Official Git Documentation](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com)
- [Pro Git Book](https://git-scm.com/book/en/v2)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Learn Git Branching](https://learngitbranching.js.org/)

---

**Next Steps**: Practice these commands regularly, and explore the [GitHub Actions](../GitHubActions/README.md) guide to automate your workflows!
