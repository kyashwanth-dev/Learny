# Terraform Complete Guide

## Table of Contents
- [Introduction](#introduction)
- [What is Terraform?](#what-is-terraform)
- [Key Concepts](#key-concepts)
- [Installing Terraform](#installing-terraform)
- [Terraform Basics](#terraform-basics)
- [Configuration Language (HCL)](#configuration-language-hcl)
- [Providers](#providers)
- [Resources](#resources)
- [Variables](#variables)
- [Outputs](#outputs)
- [State Management](#state-management)
- [Modules](#modules)
- [Data Sources](#data-sources)
- [Functions](#functions)
- [Provisioners](#provisioners)
- [Workspaces](#workspaces)
- [Backend Configuration](#backend-configuration)
- [Best Practices](#best-practices)
- [Real-World Examples](#real-world-examples)
- [Troubleshooting](#troubleshooting)

## Introduction

Terraform is an open-source Infrastructure as Code (IaC) tool created by HashiCorp that enables you to define and provision infrastructure using a declarative configuration language. It supports multiple cloud providers and services, making it a versatile tool for managing infrastructure across different platforms.

## What is Terraform?

Terraform provides:

- **Infrastructure as Code**: Define infrastructure in human-readable configuration files
- **Execution Plans**: Preview changes before applying them
- **Resource Graph**: Understand dependencies and parallelize operations
- **Change Automation**: Apply complex changesets with minimal human interaction
- **Multi-Cloud Support**: Manage resources across AWS, Azure, GCP, and more
- **Version Control**: Track infrastructure changes over time

### Benefits
- ✅ Declarative syntax - describe what you want, not how to create it
- ✅ Provider ecosystem - support for 1000+ providers
- ✅ State management - track resource state and dependencies
- ✅ Plan before apply - preview changes before execution
- ✅ Reusable modules - share and reuse infrastructure patterns
- ✅ Collaboration - teams can work together on infrastructure

### Use Cases
- **Cloud Infrastructure**: Provision VMs, networks, storage
- **Multi-Cloud Deployments**: Manage resources across providers
- **Kubernetes**: Deploy and manage clusters
- **Self-Service Clusters**: Enable developers to provision infrastructure
- **Software Defined Networking**: Configure networks programmatically
- **Resource Schedulers**: Integrate with Nomad, Kubernetes

## Key Concepts

### Infrastructure as Code (IaC)
Managing and provisioning infrastructure through code instead of manual processes.

### Provider
A plugin that enables Terraform to interact with cloud platforms and other services.

### Resource
A component of your infrastructure (e.g., VM, network, database).

### Module
A container for multiple resources that are used together.

### State
A snapshot of your infrastructure as it exists in the real world.

### Plan
A preview of the changes Terraform will make to your infrastructure.

### Apply
The action of executing the changes defined in your configuration.

### Data Source
Allows Terraform to fetch or compute data for use in configuration.

## Installing Terraform

### Linux (Ubuntu/Debian)
```bash
# Add HashiCorp GPG key
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

# Add HashiCorp repository
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

# Update and install
sudo apt update
sudo apt install terraform

# Verify installation
terraform version
```

### macOS
```bash
# Using Homebrew
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Verify installation
terraform version
```

### Windows
```powershell
# Using Chocolatey
choco install terraform

# Verify installation
terraform version
```

### Manual Installation
```bash
# Download from https://www.terraform.io/downloads
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip

# Unzip and move to PATH
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Verify
terraform version
```

### Enable Tab Completion
```bash
# Bash
terraform -install-autocomplete

# Zsh
terraform -install-autocomplete

# Reload shell
source ~/.bashrc  # or ~/.zshrc
```

## Terraform Basics

### Basic Workflow

```bash
# Initialize working directory
terraform init

# Validate configuration
terraform validate

# Format configuration files
terraform fmt

# Preview changes
terraform plan

# Apply changes
terraform apply

# Destroy infrastructure
terraform destroy
```

### Your First Terraform Configuration

Create a file named `main.tf`:
```hcl
# Configure the provider
terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

# Create a local file
resource "local_file" "example" {
  content  = "Hello, Terraform!"
  filename = "${path.module}/hello.txt"
}
```

Run the configuration:
```bash
# Initialize
terraform init

# Preview changes
terraform plan

# Apply changes
terraform apply

# Verify file was created
cat hello.txt

# Clean up
terraform destroy
```

## Configuration Language (HCL)

### HCL Syntax Basics

#### Block Structure
```hcl
# Basic block syntax
<BLOCK_TYPE> "<BLOCK_LABEL>" "<BLOCK_LABEL>" {
  # Block body
  <IDENTIFIER> = <EXPRESSION>
}

# Example
resource "aws_instance" "web" {
  ami           = "ami-abc123"
  instance_type = "t2.micro"
}
```

#### Arguments and Expressions
```hcl
# String
name = "web-server"

# Number
count = 3

# Boolean
enabled = true

# List
availability_zones = ["us-east-1a", "us-east-1b"]

# Map
tags = {
  Name        = "WebServer"
  Environment = "Production"
}
```

#### Comments
```hcl
# Single line comment

// Another single line comment

/* 
   Multi-line
   comment
*/
```

#### String Interpolation
```hcl
# Basic interpolation
name = "server-${var.environment}"

# String template
user_data = <<-EOF
  #!/bin/bash
  echo "Hello from ${var.instance_name}"
EOF
```

#### Conditional Expressions
```hcl
# Ternary operator
instance_type = var.environment == "prod" ? "t2.large" : "t2.micro"

# Count with condition
count = var.create_instance ? 1 : 0
```

#### For Expressions
```hcl
# List transformation
upper_names = [for name in var.names : upper(name)]

# Map transformation
instance_ips = {
  for instance in aws_instance.servers :
  instance.id => instance.private_ip
}

# Filtering
prod_instances = [
  for instance in var.instances :
  instance if instance.environment == "prod"
]
```

#### Dynamic Blocks
```hcl
resource "aws_security_group" "example" {
  name = "example"

  dynamic "ingress" {
    for_each = var.ingress_ports
    content {
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
}
```

## Providers

### Provider Configuration

```hcl
# AWS Provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region     = "us-east-1"
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}
```

### Multiple Provider Configurations

```hcl
# Default provider
provider "aws" {
  region = "us-east-1"
}

# Alternate provider
provider "aws" {
  alias  = "west"
  region = "us-west-2"
}

# Use alternate provider
resource "aws_instance" "west_server" {
  provider = aws.west
  ami      = "ami-xyz123"
  instance_type = "t2.micro"
}
```

### Common Providers

#### AWS
```hcl
provider "aws" {
  region  = "us-east-1"
  profile = "default"
}
```

#### Azure
```hcl
provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
}
```

#### Google Cloud
```hcl
provider "google" {
  project = "my-project-id"
  region  = "us-central1"
  zone    = "us-central1-a"
}
```

#### Kubernetes
```hcl
provider "kubernetes" {
  config_path = "~/.kube/config"
}
```

## Resources

### Resource Syntax

```hcl
resource "resource_type" "resource_name" {
  argument1 = value1
  argument2 = value2
}
```

### AWS EC2 Instance Example

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name = "WebServer"
  }

  lifecycle {
    create_before_destroy = true
  }
}
```

### Resource Dependencies

#### Implicit Dependencies
```hcl
resource "aws_eip" "ip" {
  instance = aws_instance.web.id  # Implicit dependency
}
```

#### Explicit Dependencies
```hcl
resource "aws_instance" "web" {
  ami           = "ami-abc123"
  instance_type = "t2.micro"

  depends_on = [aws_security_group.web_sg]
}
```

### Resource Meta-Arguments

#### count
```hcl
resource "aws_instance" "server" {
  count = 3

  ami           = "ami-abc123"
  instance_type = "t2.micro"

  tags = {
    Name = "Server-${count.index}"
  }
}
```

#### for_each
```hcl
resource "aws_instance" "server" {
  for_each = toset(["web", "api", "db"])

  ami           = "ami-abc123"
  instance_type = "t2.micro"

  tags = {
    Name = each.key
  }
}
```

#### lifecycle
```hcl
resource "aws_instance" "web" {
  ami           = "ami-abc123"
  instance_type = "t2.micro"

  lifecycle {
    create_before_destroy = true
    prevent_destroy       = false
    ignore_changes        = [tags]
  }
}
```

## Variables

### Variable Declaration

```hcl
# Simple variable
variable "instance_type" {
  type    = string
  default = "t2.micro"
}

# Variable with description
variable "availability_zones" {
  type        = list(string)
  description = "List of availability zones"
  default     = ["us-east-1a", "us-east-1b"]
}

# Variable with validation
variable "instance_count" {
  type    = number
  default = 1

  validation {
    condition     = var.instance_count > 0 && var.instance_count <= 10
    error_message = "Instance count must be between 1 and 10."
  }
}

# Sensitive variable
variable "db_password" {
  type      = string
  sensitive = true
}
```

### Variable Types

```hcl
# String
variable "region" {
  type    = string
  default = "us-east-1"
}

# Number
variable "instance_count" {
  type    = number
  default = 2
}

# Boolean
variable "enable_monitoring" {
  type    = bool
  default = true
}

# List
variable "availability_zones" {
  type    = list(string)
  default = ["us-east-1a", "us-east-1b"]
}

# Map
variable "instance_tags" {
  type = map(string)
  default = {
    Environment = "dev"
    Project     = "web"
  }
}

# Object
variable "instance_config" {
  type = object({
    instance_type = string
    ami           = string
    volume_size   = number
  })
}
```

### Providing Variable Values

#### Command Line
```bash
terraform apply -var="instance_type=t2.large"
terraform apply -var="tags={Name=Server,Env=Prod}"
```

#### Variable Files
```hcl
# terraform.tfvars
instance_type = "t2.large"
region        = "us-west-2"

tags = {
  Environment = "production"
  Project     = "web-app"
}
```

```bash
# Apply with specific var file
terraform apply -var-file="prod.tfvars"
```

#### Environment Variables
```bash
export TF_VAR_instance_type="t2.large"
export TF_VAR_region="us-west-2"
terraform apply
```

### Using Variables

```hcl
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = var.tags
}
```

### Local Values

```hcl
locals {
  common_tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }

  name_prefix = "${var.project}-${var.environment}"
}

resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = merge(
    local.common_tags,
    {
      Name = "${local.name_prefix}-web"
    }
  )
}
```

## Outputs

### Output Declaration

```hcl
output "instance_ip" {
  value       = aws_instance.web.public_ip
  description = "Public IP of the web server"
}

output "instance_id" {
  value = aws_instance.web.id
}

output "connection_string" {
  value     = "postgresql://${aws_db_instance.db.endpoint}"
  sensitive = true
}
```

### Output with Conditions

```hcl
output "instance_ips" {
  value = [
    for instance in aws_instance.servers :
    instance.public_ip if instance.public_ip != ""
  ]
}
```

### Viewing Outputs

```bash
# View all outputs
terraform output

# View specific output
terraform output instance_ip

# Output in JSON format
terraform output -json

# Use output in scripts
INSTANCE_IP=$(terraform output -raw instance_ip)
```

### Using Outputs from Modules

```hcl
module "network" {
  source = "./modules/network"
}

resource "aws_instance" "web" {
  subnet_id = module.network.subnet_id
}
```

## State Management

### What is Terraform State?

Terraform state is a JSON file that maps real-world resources to your configuration. It tracks metadata and improves performance for large infrastructures.

### Local State

```bash
# State is stored in terraform.tfstate file
ls -la terraform.tfstate

# View state
terraform show

# List resources in state
terraform state list

# Show specific resource
terraform state show aws_instance.web
```

### State Commands

```bash
# List resources
terraform state list

# Show resource details
terraform state show aws_instance.web

# Move resource
terraform state mv aws_instance.old aws_instance.new

# Remove resource from state
terraform state rm aws_instance.web

# Pull remote state
terraform state pull

# Push local state
terraform state push terraform.tfstate

# Replace provider
terraform state replace-provider hashicorp/aws registry.terraform.io/hashicorp/aws
```

### Remote State

#### S3 Backend
```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

#### Azure Storage Backend
```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-rg"
    storage_account_name = "terraformstate"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}
```

#### Terraform Cloud Backend
```hcl
terraform {
  cloud {
    organization = "my-org"

    workspaces {
      name = "my-workspace"
    }
  }
}
```

### State Locking

```hcl
# S3 with DynamoDB locking
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"  # Enable locking
  }
}
```

### Remote State Data Source

```hcl
# Read outputs from another state
data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "my-terraform-state"
    key    = "network/terraform.tfstate"
    region = "us-east-1"
  }
}

# Use remote state outputs
resource "aws_instance" "web" {
  subnet_id = data.terraform_remote_state.network.outputs.subnet_id
}
```

## Modules

### What are Modules?

Modules are containers for multiple resources that are used together. They enable code reuse and organization.

### Module Structure

```
module/
├── main.tf       # Main resources
├── variables.tf  # Input variables
├── outputs.tf    # Output values
└── README.md     # Documentation
```

### Creating a Module

#### modules/web-server/variables.tf
```hcl
variable "instance_type" {
  type    = string
  default = "t2.micro"
}

variable "instance_name" {
  type = string
}

variable "ami_id" {
  type = string
}
```

#### modules/web-server/main.tf
```hcl
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name = var.instance_name
  }
}
```

#### modules/web-server/outputs.tf
```hcl
output "instance_id" {
  value = aws_instance.web.id
}

output "public_ip" {
  value = aws_instance.web.public_ip
}
```

### Using a Module

```hcl
module "web_server" {
  source = "./modules/web-server"

  instance_type = "t2.medium"
  instance_name = "production-web"
  ami_id        = "ami-abc123"
}

# Access module outputs
output "web_server_ip" {
  value = module.web_server.public_ip
}
```

### Module Sources

#### Local Path
```hcl
module "web" {
  source = "./modules/web-server"
}
```

#### Terraform Registry
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "my-vpc"
  cidr = "10.0.0.0/16"
}
```

#### GitHub
```hcl
module "web" {
  source = "github.com/user/terraform-modules//web-server?ref=v1.0.0"
}
```

#### Git
```hcl
module "web" {
  source = "git::https://example.com/terraform-modules.git//modules/web?ref=v1.0"
}
```

### Module Best Practices

```hcl
# Use versioning
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"  # Allow patch updates
}

# Descriptive variable names
variable "enable_nat_gateway" {
  description = "Enable NAT Gateway for private subnets"
  type        = bool
  default     = true
}

# Document outputs
output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.main.id
}
```

## Data Sources

### What are Data Sources?

Data sources allow Terraform to fetch information from existing infrastructure or external systems.

### Common Data Sources

#### AWS AMI
```hcl
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
}
```

#### AWS VPC
```hcl
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}
```

#### Current AWS Account
```hcl
data "aws_caller_identity" "current" {}

output "account_id" {
  value = data.aws_caller_identity.current.account_id
}
```

#### Kubernetes ConfigMap
```hcl
data "kubernetes_config_map" "app_config" {
  metadata {
    name      = "app-config"
    namespace = "default"
  }
}

output "config_data" {
  value = data.kubernetes_config_map.app_config.data
}
```

## Functions

### String Functions

```hcl
# format - Format a string
format("server-%03d", 1)  # "server-001"

# join - Join list elements
join(",", ["a", "b", "c"])  # "a,b,c"

# split - Split string into list
split(",", "a,b,c")  # ["a", "b", "c"]

# lower/upper - Change case
lower("HELLO")  # "hello"
upper("hello")  # "HELLO"

# trim - Remove characters
trim("  hello  ", " ")  # "hello"

# substr - Extract substring
substr("hello world", 0, 5)  # "hello"

# replace - Replace substring
replace("hello world", "world", "terraform")  # "hello terraform"
```

### Collection Functions

```hcl
# length - Get length
length(["a", "b", "c"])  # 3

# concat - Combine lists
concat(["a", "b"], ["c", "d"])  # ["a", "b", "c", "d"]

# merge - Combine maps
merge({a = 1}, {b = 2})  # {a = 1, b = 2}

# lookup - Get map value
lookup({a = 1, b = 2}, "a", 0)  # 1

# element - Get list element
element(["a", "b", "c"], 1)  # "b"

# contains - Check if list contains value
contains(["a", "b", "c"], "b")  # true

# keys/values - Get map keys/values
keys({a = 1, b = 2})    # ["a", "b"]
values({a = 1, b = 2})  # [1, 2]

# distinct - Remove duplicates
distinct(["a", "b", "a"])  # ["a", "b"]
```

### Numeric Functions

```hcl
# max/min - Maximum/minimum value
max(1, 2, 3)  # 3
min(1, 2, 3)  # 1

# abs - Absolute value
abs(-5)  # 5

# ceil/floor - Round up/down
ceil(1.3)   # 2
floor(1.7)  # 1

# pow - Power
pow(2, 3)  # 8
```

### Encoding Functions

```hcl
# base64encode/base64decode
base64encode("hello")  # "aGVsbG8="
base64decode("aGVsbG8=")  # "hello"

# jsonencode/jsondecode
jsonencode({name = "test"})  # "{\"name\":\"test\"}"
jsondecode("{\"name\":\"test\"}")  # {name = "test"}
```

### File Functions

```hcl
# file - Read file contents
file("${path.module}/config.txt")

# templatefile - Read and render template
templatefile("${path.module}/user_data.sh", {
  name = var.instance_name
})

# fileexists - Check if file exists
fileexists("config.txt")
```

## Provisioners

### What are Provisioners?

Provisioners are used to execute scripts on local or remote machines as part of resource creation or destruction.

⚠️ **Note**: Provisioners should be used as a last resort. Consider using cloud-init or configuration management tools instead.

### Local-exec Provisioner

```hcl
resource "aws_instance" "web" {
  ami           = "ami-abc123"
  instance_type = "t2.micro"

  provisioner "local-exec" {
    command = "echo ${self.private_ip} >> private_ips.txt"
  }
}
```

### Remote-exec Provisioner

```hcl
resource "aws_instance" "web" {
  ami           = "ami-abc123"
  instance_type = "t2.micro"
  key_name      = var.key_name

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("~/.ssh/id_rsa")
    host        = self.public_ip
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y nginx",
      "sudo systemctl start nginx"
    ]
  }
}
```

### File Provisioner

```hcl
resource "aws_instance" "web" {
  ami           = "ami-abc123"
  instance_type = "t2.micro"

  connection {
    type = "ssh"
    user = "ubuntu"
    host = self.public_ip
  }

  provisioner "file" {
    source      = "app.conf"
    destination = "/etc/app.conf"
  }

  provisioner "file" {
    content     = "Server config"
    destination = "/tmp/config.txt"
  }
}
```

### Destroy-time Provisioners

```hcl
resource "aws_instance" "web" {
  ami           = "ami-abc123"
  instance_type = "t2.micro"

  provisioner "local-exec" {
    when    = destroy
    command = "echo 'Instance ${self.id} is being destroyed'"
  }
}
```

### Provisioner Failure Handling

```hcl
resource "aws_instance" "web" {
  ami           = "ami-abc123"
  instance_type = "t2.micro"

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y nginx"
    ]

    on_failure = continue  # or fail (default)
  }
}
```

## Workspaces

### What are Workspaces?

Workspaces allow you to manage multiple distinct sets of infrastructure resources using the same configuration.

### Workspace Commands

```bash
# List workspaces
terraform workspace list

# Create workspace
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod

# Switch workspace
terraform workspace select dev

# Show current workspace
terraform workspace show

# Delete workspace
terraform workspace delete dev
```

### Using Workspaces in Configuration

```hcl
# Access current workspace
locals {
  environment = terraform.workspace
}

# Different instance types per workspace
resource "aws_instance" "web" {
  ami = "ami-abc123"
  instance_type = terraform.workspace == "prod" ? "t2.large" : "t2.micro"

  tags = {
    Name        = "web-${terraform.workspace}"
    Environment = terraform.workspace
  }
}

# Workspace-specific variable files
variable "instance_count" {
  type = map(number)
  default = {
    dev     = 1
    staging = 2
    prod    = 5
  }
}

resource "aws_instance" "web" {
  count = var.instance_count[terraform.workspace]
  # ...
}
```

## Backend Configuration

### Local Backend (Default)

```hcl
terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}
```

### S3 Backend

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
    
    # Optional
    kms_key_id = "arn:aws:kms:us-east-1:123456789:key/12345"
  }
}
```

#### Create S3 Backend Resources
```bash
# Create S3 bucket
aws s3 mb s3://my-terraform-state

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket my-terraform-state \
  --versioning-configuration Status=Enabled

# Create DynamoDB table for locking
aws dynamodb create-table \
  --table-name terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

### Azure Storage Backend

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-rg"
    storage_account_name = "tfstate12345"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}
```

### GCS Backend

```hcl
terraform {
  backend "gcs" {
    bucket = "my-terraform-state"
    prefix = "prod"
  }
}
```

### Terraform Cloud Backend

```hcl
terraform {
  cloud {
    organization = "my-organization"

    workspaces {
      name = "my-workspace"
    }
  }
}
```

### Backend Configuration with Variables

```hcl
# backend.hcl
bucket = "my-terraform-state"
key    = "prod/terraform.tfstate"
region = "us-east-1"
```

```bash
# Initialize with backend config
terraform init -backend-config=backend.hcl
```

### Migrating State

```bash
# Initialize with new backend
terraform init -migrate-state

# Or reconfigure backend
terraform init -reconfigure
```

## Best Practices

### 1. Project Structure

```
terraform-project/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   │   └── ...
│   └── prod/
│       └── ...
├── modules/
│   ├── networking/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── compute/
│       └── ...
├── .gitignore
└── README.md
```

### 2. Use Remote State

```hcl
# Always use remote state for team collaboration
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "${var.project}/${var.environment}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### 3. Use Variables and Locals

```hcl
# variables.tf
variable "environment" {
  type = string
}

variable "project" {
  type = string
}

# locals.tf
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project
    ManagedBy   = "Terraform"
    Owner       = "DevOps Team"
  }

  name_prefix = "${var.project}-${var.environment}"
}

# Use in resources
resource "aws_instance" "web" {
  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-web"
  })
}
```

### 4. Use Modules for Reusability

```hcl
# Reusable module
module "web_tier" {
  source = "../../modules/web-tier"

  environment     = var.environment
  instance_count  = var.web_instance_count
  instance_type   = var.web_instance_type
  vpc_id          = module.networking.vpc_id
  subnet_ids      = module.networking.private_subnet_ids
}
```

### 5. Version Constraints

```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"  # Allow patch updates
    }
  }
}
```

### 6. Sensitive Data

```hcl
# Mark sensitive variables
variable "db_password" {
  type      = string
  sensitive = true
}

# Mark sensitive outputs
output "db_password" {
  value     = aws_db_instance.main.password
  sensitive = true
}

# Use AWS Secrets Manager
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/db/password"
}

resource "aws_db_instance" "main" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}
```

### 7. Use .gitignore

```gitignore
# .gitignore
**/.terraform/*
*.tfstate
*.tfstate.*
crash.log
crash.*.log
*.tfvars
*.tfvars.json
override.tf
override.tf.json
*_override.tf
*_override.tf.json
.terraformrc
terraform.rc
```

### 8. Documentation

```hcl
# Describe resources
variable "instance_type" {
  description = "EC2 instance type for web servers"
  type        = string
  default     = "t2.micro"
}

output "load_balancer_dns" {
  description = "DNS name of the load balancer"
  value       = aws_lb.main.dns_name
}

# Add README for modules
# modules/vpc/README.md
```

### 9. Use terraform fmt and validate

```bash
# Format code
terraform fmt -recursive

# Validate configuration
terraform validate

# Use in CI/CD
terraform fmt -check
terraform validate
```

### 10. Plan Before Apply

```bash
# Always review plan
terraform plan -out=tfplan

# Review the plan
terraform show tfplan

# Apply the plan
terraform apply tfplan
```

## Real-World Examples

### Complete AWS Infrastructure

```hcl
# main.tf
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "prod/infrastructure/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC Module
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "${var.project}-${var.environment}-vpc"
  cidr = var.vpc_cidr

  azs             = var.availability_zones
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs

  enable_nat_gateway = true
  enable_vpn_gateway = false
  enable_dns_hostnames = true

  tags = local.common_tags
}

# Security Group
resource "aws_security_group" "web" {
  name_prefix = "${var.project}-web-"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${var.project}-web-sg"
  })
}

# Launch Template
resource "aws_launch_template" "web" {
  name_prefix   = "${var.project}-web-"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = var.instance_type

  vpc_security_group_ids = [aws_security_group.web.id]

  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    environment = var.environment
  }))

  tag_specifications {
    resource_type = "instance"
    tags = merge(local.common_tags, {
      Name = "${var.project}-web-instance"
    })
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "web" {
  name                = "${var.project}-web-asg"
  vpc_zone_identifier = module.vpc.private_subnets
  target_group_arns   = [aws_lb_target_group.web.arn]

  min_size         = var.asg_min_size
  max_size         = var.asg_max_size
  desired_capacity = var.asg_desired_capacity

  launch_template {
    id      = aws_launch_template.web.id
    version = "$Latest"
  }

  health_check_type         = "ELB"
  health_check_grace_period = 300

  tag {
    key                 = "Name"
    value               = "${var.project}-web-instance"
    propagate_at_launch = true
  }

  dynamic "tag" {
    for_each = local.common_tags
    content {
      key                 = tag.key
      value               = tag.value
      propagate_at_launch = true
    }
  }
}

# Application Load Balancer
resource "aws_lb" "web" {
  name               = "${var.project}-web-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.web.id]
  subnets            = module.vpc.public_subnets

  tags = merge(local.common_tags, {
    Name = "${var.project}-web-alb"
  })
}

resource "aws_lb_target_group" "web" {
  name     = "${var.project}-web-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = module.vpc.vpc_id

  health_check {
    path                = "/"
    healthy_threshold   = 2
    unhealthy_threshold = 10
    timeout             = 5
    interval            = 30
  }

  tags = local.common_tags
}

resource "aws_lb_listener" "web" {
  load_balancer_arn = aws_lb.web.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web.arn
  }
}

# RDS Database
resource "aws_db_subnet_group" "main" {
  name       = "${var.project}-db-subnet-group"
  subnet_ids = module.vpc.private_subnets

  tags = local.common_tags
}

resource "aws_db_instance" "main" {
  identifier     = "${var.project}-db"
  engine         = "postgres"
  engine_version = "15.3"
  instance_class = var.db_instance_class

  allocated_storage     = 20
  max_allocated_storage = 100
  storage_encrypted     = true

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db.id]

  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"

  skip_final_snapshot = var.environment != "prod"

  tags = local.common_tags
}

# Data sources
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

# Locals
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project
    ManagedBy   = "Terraform"
  }
}

# Outputs
output "alb_dns_name" {
  description = "DNS name of the load balancer"
  value       = aws_lb.web.dns_name
}

output "db_endpoint" {
  description = "Database endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}
```

### Kubernetes Cluster with Terraform

```hcl
# eks-cluster.tf
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.0.0"

  cluster_name    = "${var.project}-cluster"
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    main = {
      min_size     = 2
      max_size     = 10
      desired_size = 3

      instance_types = ["t3.medium"]
      capacity_type  = "ON_DEMAND"

      labels = {
        Environment = var.environment
      }

      tags = local.common_tags
    }
  }

  tags = local.common_tags
}

# Install add-ons
resource "aws_eks_addon" "vpc_cni" {
  cluster_name = module.eks.cluster_name
  addon_name   = "vpc-cni"
}

resource "aws_eks_addon" "coredns" {
  cluster_name = module.eks.cluster_name
  addon_name   = "coredns"
}

# Kubernetes provider
provider "kubernetes" {
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
  
  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args = [
      "eks",
      "get-token",
      "--cluster-name",
      module.eks.cluster_name
    ]
  }
}

# Deploy application
resource "kubernetes_deployment" "app" {
  metadata {
    name = "myapp"
    labels = {
      app = "myapp"
    }
  }

  spec {
    replicas = 3

    selector {
      match_labels = {
        app = "myapp"
      }
    }

    template {
      metadata {
        labels = {
          app = "myapp"
        }
      }

      spec {
        container {
          image = "nginx:latest"
          name  = "nginx"

          port {
            container_port = 80
          }
        }
      }
    }
  }
}
```

## Troubleshooting

### Common Issues

#### 1. State Lock Errors

```bash
# Error: state is locked
# Force unlock (use with caution)
terraform force-unlock <lock-id>

# Prevent by ensuring only one terraform process runs at a time
```

#### 2. Resource Already Exists

```bash
# Import existing resource
terraform import aws_instance.web i-1234567890abcdef0

# Or remove from state and recreate
terraform state rm aws_instance.web
```

#### 3. Provider Authentication

```bash
# AWS
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export AWS_DEFAULT_REGION="us-east-1"

# Azure
az login

# GCP
gcloud auth application-default login
```

#### 4. Dependency Issues

```hcl
# Add explicit dependency
resource "aws_instance" "web" {
  # ...
  depends_on = [aws_security_group.web]
}
```

#### 5. Variable Not Set

```bash
# Set via environment variable
export TF_VAR_instance_type="t2.micro"

# Or pass via command line
terraform apply -var="instance_type=t2.micro"

# Or use tfvars file
terraform apply -var-file="prod.tfvars"
```

### Debugging

```bash
# Enable debug logging
export TF_LOG=DEBUG
export TF_LOG_PATH=terraform.log

# Log levels: TRACE, DEBUG, INFO, WARN, ERROR
export TF_LOG=TRACE

# Disable logging
unset TF_LOG
unset TF_LOG_PATH

# View detailed plan
terraform plan -out=tfplan
terraform show -json tfplan | jq

# Refresh state
terraform refresh
```

### Common Commands for Troubleshooting

```bash
# Check configuration syntax
terraform validate

# Show current state
terraform show

# Show specific resource
terraform state show aws_instance.web

# Get provider schema
terraform providers schema -json | jq

# Verify provider versions
terraform version
terraform providers

# Test expressions
terraform console
> var.instance_type
> length(var.availability_zones)
```

## Resources

### Official Documentation
- [Terraform Documentation](https://www.terraform.io/docs)
- [Terraform Registry](https://registry.terraform.io/)
- [HashiCorp Learn](https://learn.hashicorp.com/terraform)

### Provider Documentation
- [AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Google Cloud Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [Kubernetes Provider](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs)

### Books
- "Terraform: Up & Running" by Yevgeniy Brikman
- "HashiCorp Infrastructure Automation Certification Guide"
- "Terraform in Action" by Scott Winkler

### Tools and Extensions
- [Terraform VS Code Extension](https://marketplace.visualstudio.com/items?itemName=HashiCorp.terraform)
- [TFLint](https://github.com/terraform-linters/tflint) - Terraform linter
- [Terragrunt](https://terragrunt.gruntwork.io/) - Terraform wrapper
- [Checkov](https://www.checkov.io/) - Security scanner

### Community
- [Terraform Community Forum](https://discuss.hashicorp.com/c/terraform-core)
- [Terraform GitHub](https://github.com/hashicorp/terraform)
- [Stack Overflow - Terraform](https://stackoverflow.com/questions/tagged/terraform)

---

**Next Steps**: Apply your knowledge by provisioning cloud infrastructure and integrating with your CI/CD pipelines!
