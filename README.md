# Falla237 AWS Enterprise Deployment

## 📋 Project Overview

**Falla237 AWS Deploy** is a production-grade DevOps project that demonstrates the end-to-end deployment of a Django PWA (Progressive Web App) on AWS using industry-best practices and modern Infrastructure as Code (IaC) tools.

This project simulates how enterprises deploy and manage scalable, secure, and highly available web applications in the cloud, working within real-world constraints like **AWS account limits** (max 4 EC2 instances) and **ALB creation through ASG only**.

### 🎯 Project Goals
- Deploy a real Django application (Falla237) to AWS with **High Availability** across 3 AZs
- Implement **Immutable Infrastructure** using Golden AMIs (Packer + Ansible)
- Build a **fully automated CI/CD pipeline** with GitHub Actions
- Practice **multi-registry container management** (ECR + Docker Hub)
- Follow **security best practices** (private subnets, HTTPS, security group chaining)
- Work within **AWS account constraints** (4 EC2 limit, ALB via ASG)
- Create a **portfolio-worthy** project that demonstrates real DevOps skills

---

## 📦 COMPLETE AWS RESOURCE INVENTORY

### 🌐 NETWORK LAYER

| Resource | Quantity | Configuration | Purpose |
|----------|----------|---------------|---------|
| **VPC** | 1 | CIDR: 10.0.0.0/16 | Isolated network environment |
| **Internet Gateway** | 1 | Attached to VPC | Public internet access |
| **Subnets** | 9 | 3 public, 3 private app, 3 private data | Multi-AZ networking |
| **NAT Gateways** | 3 | 1 per AZ | Private subnet internet access |
| **Elastic IPs** | 3 | 1 per NAT Gateway | Static IPs for NAT |
| **Route Tables** | 4 | 1 public + 3 private | Traffic routing |

### 🗺️ Subnet Design (3 AZs)

| AZ | Subnet Type | CIDR | Resources |
|----|-------------|------|-----------|
| **AZ1** | Public | 10.0.1.0/24 | ALB (via ASG), NAT GW, Bastion |
| | Private App | 10.0.10.0/24 | EC2 (ASG instance 1) |
| | Private Data | 10.0.20.0/24 | RDS Primary |
| **AZ2** | Public | 10.0.2.0/24 | ALB (via ASG), NAT GW |
| | Private App | 10.0.11.0/24 | EC2 (ASG instance 2) |
| | Private Data | 10.0.21.0/24 | RDS Standby |
| **AZ3** | Public | 10.0.3.0/24 | ALB (via ASG), NAT GW |
| | Private App | 10.0.12.0/24 | EC2 (ASG instance 3) |
| | Private Data | 10.0.22.0/24 | RDS Standby |

### 🔒 SECURITY GROUPS

| Security Group | Inbound Rules | Outbound Rules | Purpose |
|----------------|---------------|----------------|---------|
| **ALB SG** | 80/443 from internet | 8000 to App SG | Load balancer firewall |
| **App SG** | 8000 from ALB, 22 from Bastion | 5432 to RDS, 443 to internet | EC2 instances firewall |
| **RDS SG** | 5432 from App + Bastion | None | Database firewall |
| **Bastion SG** | 22 from your IP | 5432 to RDS, 22 to App | Admin access |
| **NAT SG** | From private subnets | To internet | NAT translation |

### 🖥️ COMPUTE LAYER (4 EC2 Limit Applied)

| Resource | Quantity | Configuration | Purpose |
|----------|----------|---------------|---------|
| **Auto Scaling Group** | 1 | Min: 3, Max: 3, Desired: 3 | Fixed at account limit |
| **EC2 Instances (ASG)** | 3 | t2.micro, 1 per AZ | Django app servers |
| **Bastion Host** | 1 | t2.micro | Admin access to private resources |
| **Launch Template** | 1 | With Golden AMI | EC2 configuration template |
| **IAM Roles** | 2 | ECR pull, SSM access (future) | Instance permissions |

### ⚖️ LOAD BALANCING (Created via ASG)

| Resource | Quantity | Configuration | Purpose |
|----------|----------|---------------|---------|
| **Application Load Balancer** | 1 | Internet-facing | Traffic entry point |
| **HTTP Listener** | 1 | Port 80 → Redirect 443 | Force HTTPS |
| **HTTPS Listener** | 1 | Port 443 → Target group | SSL termination |
| **Target Group** | 1 | Port 8000, /health check | App instance grouping |
| **ACM Certificate** | 1 | foudadev.site, *.foudadev.site | HTTPS encryption |

### 🗄️ DATABASE LAYER

| Resource | Quantity | Configuration | Purpose |
|----------|----------|---------------|---------|
| **RDS PostgreSQL** | 1 | db.t3.micro | Application database |
| **DB Subnet Group** | 1 | 3 private data subnets | Multi-AZ placement |
| **Storage** | 20GB | GP3, encrypted | Data persistence |
| **Backups** | 7 days | Automated | Disaster recovery |

### 📦 STATE MANAGEMENT

| Resource | Quantity | Configuration | Purpose |
|----------|----------|---------------|---------|
| **S3 Bucket** | 1 | Versioned, encrypted | Terraform state storage |
| **DynamoDB Table** | 1 | Pay-per-request | State locking |

### 🐳 CONTAINER REGISTRIES

| Resource | Quantity | Purpose |
|----------|----------|---------|
| **Amazon ECR Repository** | 1 | Private image storage |
| **Docker Hub Repository** | 1 | Public image backup |

### 📊 TOTAL RESOURCES: ~45-50 AWS Resources

---

## 🏗️ Architecture Overview

### Infrastructure Layout
```
┌─────────────────────────────────────────────────────────────┐
│                         AWS Cloud                           │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  VPC (10.0.0.0/16) - 3 Availability Zones          │  │
│  │                                                     │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │  │
│  │  │   AZ1    │  │   AZ2    │  │   AZ3    │         │  │
│  │  ├──────────┤  ├──────────┤  ├──────────┤         │  │
│  │  │ Public   │  │ Public   │  │ Public   │         │  │
│  │  │ 10.0.1.0 │  │ 10.0.2.0 │  │ 10.0.3.0 │         │  │
│  │  │ - ALB    │  │ - ALB    │  │ - ALB    │         │  │
│  │  │ - NAT GW │  │ - NAT GW │  │ - NAT GW │         │  │
│  │  │ - Bastion│  │          │  │          │         │  │
│  │  ├──────────┤  ├──────────┤  ├──────────┤         │  │
│  │  │ Private  │  │ Private  │  │ Private  │         │  │
│  │  │ App      │  │ App      │  │ App      │         │  │
│  │  │ 10.0.10.0│  │ 10.0.11.0│  │ 10.0.12.0│         │  │
│  │  │ - EC2-1  │  │ - EC2-2  │  │ - EC2-3  │         │  │
│  │  ├──────────┤  ├──────────┤  ├──────────┤         │  │
│  │  │ Private  │  │ Private  │  │ Private  │         │  │
│  │  │ Data     │  │ Data     │  │ Data     │         │  │
│  │  │ 10.0.20.0│  │ 10.0.21.0│  │ 10.0.22.0│         │  │
│  │  │ - RDS    │  │ - RDS    │  │ - RDS    │         │  │
│  │  └──────────┘  └──────────┘  └──────────┘         │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │                Supporting Services                   │  │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐   │  │
│  │  │  ECR   │  │Docker  │  │   S3   │  │DynamoDB│   │  │
│  │  │        │  │  Hub   │  │(State) │  │(Lock)  │   │  │
│  │  └────────┘  └────────┘  └────────┘  └────────┘   │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow
```
User → HTTPS (443) → Route53 (foudadev.site) → ALB (SSL termination) 
      → EC2 (Auto Scaling Group - 3 instances) → Docker Container (Django App)
      → RDS PostgreSQL (Private Subnet)
```

---

## 🔄 Rolling Deployment Strategy

### Current State (Bastion Host Access)
```
[Bastion Host] → SSH access for:
                 • RDS database migrations
                 • Troubleshooting
                 • Initial setup
                 • Administrative tasks
```

### Rolling Update Policy (Instance Refresh)
When a new AMI is deployed, the ASG performs a **rolling update**:

```
Step 1: New Launch Template with updated AMI
Step 2: ASG Instance Refresh triggered
Step 3: Terminate 1 old instance → Launch 1 new instance
Step 4: Wait for health check (ALB target group)
Step 5: Repeat for remaining instances
Step 6: Deployment complete with zero downtime
```

**Benefits:**
- ✅ Zero downtime during deployments
- ✅ Automated rollback on failure
- ✅ No manual intervention needed
- ✅ Production-safe updates

---

## 🔧 Technology Stack

| Category | Tools | Purpose |
|----------|-------|---------|
| **Cloud Provider** | AWS | Infrastructure hosting |
| **Infrastructure as Code** | Terraform | Define and provision AWS resources |
| **State Management** | S3 + DynamoDB | Remote state storage + locking |
| **Containerization** | Docker | Package Django application |
| **Image Registries** | Amazon ECR, Docker Hub | Store and distribute container images |
| **Image Builder** | Packer | Create Golden AMIs |
| **Configuration Management** | Ansible | Provision AMI content |
| **CI/CD** | GitHub Actions | Automate the entire pipeline |
| **Security Scanning** | Trivy | Scan images for vulnerabilities |
| **Application** | Django + PostgreSQL | Falla237 PWA |

---

## 🔄 CI/CD Pipeline Design

### 🎯 Pipeline Design Decisions & Improvements

#### 🔹 The Problem with a Single Pipeline
In early designs, many DevOps engineers (including myself initially) make the mistake of having **one giant pipeline** that does everything on every push:

```
Push to main → Build Docker → Scan → Push → Packer → Terraform → ASG Refresh
```

**Why this is problematic:**
- ❌ **Expensive**: Every tiny code change triggers AMI baking and infrastructure updates
- ❌ **Slow**: Full pipeline can take 15-20 minutes even for a typo fix
- ❌ **Risky**: Small mistakes can accidentally trigger production infrastructure changes
- ❌ **Inflexible**: Cannot separate development iterations from production releases

**Real-world example:**
```
You fix a typo in views.py
↓
Push to main
↓
Pipeline starts
↓
• Builds Docker image (good)
• Scans with Trivy (good)
• Packs new Golden AMI (❌ unnecessary - system deps haven't changed)
• Terraform updates Launch Template (❌ unnecessary)
• ASG rolling update replaces all 3 instances (❌ overkill for a typo)
↓
15 minutes later, typo is fixed but you've wasted time and money
```

#### 🔹 The Solution: Separate CI & CD Pipelines

##### ✅ CI Pipeline (`ci.yml`) - "Fast & Frequent"
**Trigger:** Every push to `main` branch (automatic)

**What it does:**
```
Checkout code
↓
Build Docker image
↓
Run smoke tests (optional health check)
↓
Scan with Trivy (fail on HIGH/CRITICAL)
↓
Tag image with:
  • Commit SHA (falla237:git-abc1234)
  • Latest (falla237:latest)
↓
Push to both registries:
  • Amazon ECR
  • Docker Hub
↓
STOP HERE - NO INFRASTRUCTURE CHANGES
```

**Why this works:**
- ✅ Fast (~2-3 minutes)
- ✅ Every commit is tested and stored
- ✅ No risk of breaking production
- ✅ Images are ready for deployment when needed

##### ✅ CD Pipeline (`cd.yml`) - "Controlled & Production-Ready"
**Trigger:** 
- Push to Git tag (`v1.0.0`, `v1.1.0`) - automatic
- OR manual workflow dispatch

**What it does:**
```
Triggered by Git tag (e.g., v1.0.0)
↓
Pull Docker image built in CI (using commit SHA)
↓
Re-tag with semantic version (falla237:v1.0.0)
↓
Push versioned image to registries
↓
▶️ RUN DATABASE MIGRATIONS VIA BASTION HOST (ONCE) ◀️
  • GitHub Actions connects to Bastion via SSH
  • Bastion runs migration command from inside the VPC
  • This updates the database schema BEFORE new app instances start
  • Prevents version mismatch between code and database
  • RDS is in private subnet → only accessible from within VPC
↓
Packer builds Golden AMI (environment only)
  • Launches temp EC2
  • Ansible installs Docker, AWS CLI, system deps
  • Creates AMI (NO app image inside)
↓
Terraform apply:
  • Updates Launch Template with new AMI ID
  • Triggers ASG rolling update
↓
New EC2 instances boot:
  • Pull specific versioned image (falla237:v1.0.0)
  • Run container
↓
Health checks verify deployment
```

**Why this works:**
- ✅ Only runs for actual releases
- ✅ AMI baking happens only when needed
- ✅ Production changes are controlled and traceable
- ✅ Easy rollbacks: just deploy older image version
- ✅ Migrations run ONCE, preventing race conditions in scaled environments
- ✅ Bastion host provides secure access to private RDS from GitHub Actions

### 🖼️ Golden AMI Strategy Adjustment

#### ❌ Old Approach (What we avoid)
```
AMI contains:
  • Docker installed
  • App image pre-pulled
  • Container ready to run

Problem: Every app change = new AMI = expensive + slow
```

#### ✅ New Approach (What we implement)
```
AMI contains (ENVIRONMENT ONLY):
  • Ubuntu 22.04 LTS
  • Docker installed & configured
  • AWS CLI & ECR login helper
  • System dependencies
  • Security hardening

AMI does NOT contain:
  • App Docker image ❌

At boot time:
  • EC2 starts
  • Pulls specific versioned image from registry (e.g., falla237:v1.0.0)
  • Runs container
```

**Benefits of this adjustment:**
| Aspect | Old Approach | New Approach | Improvement |
|--------|--------------|--------------|-------------|
| App update | Need new AMI | Just new Docker image | Faster, cheaper |
| System update | Need new AMI | Need new AMI | Same (unavoidable) |
| Rollback | Need old AMI | Pull old image tag | Instant rollback |
| AMI bake frequency | Every commit | Only when system changes | Cost reduction |

### 🏷️ Tagging Strategy Explained

#### Two Types of Tags Working Together

**1. Git Tags (Code/Release Tags)**
```bash
# Created manually when ready to release
git tag v1.0.0
git push origin v1.0.0
```
- ✅ Triggers CD pipeline
- ✅ Marks a specific commit as a release
- ✅ Human-readable versioning

**2. Docker Image Tags (Container Tags)**

| Tag Type | Applied In | Example | Lifetime |
|----------|------------|---------|----------|
| Commit SHA | CI pipeline | `falla237:git-abc1234` | Permanent |
| Latest | CI pipeline | `falla237:latest` | Overwritten each commit |
| Semantic Version | CD pipeline | `falla237:v1.0.0` | Permanent |

**Visual Flow of Tags:**
```
Commit abc1234 pushed to main
    ↓
CI pipeline runs
    ↓
Docker tags: 
  • falla237:git-abc1234  ✓
  • falla237:latest       ✓ (overwrites previous latest)
    ↓
Push to ECR & Docker Hub

[Later] Ready for release v1.0.0
    ↓
git tag v1.0.0 && git push origin v1.0.0
    ↓
CD pipeline runs
    ↓
docker pull falla237:git-abc1234
docker tag falla237:git-abc1234 falla237:v1.0.0
docker push falla237:v1.0.0
    ↓
Now registry has:
  • falla237:git-abc1234
  • falla237:latest
  • falla237:v1.0.0   ← all point to same image!
```

### 🔹 How It All Works Together

**Scenario 1: Normal Development**
```
Developer pushes code fix
    ↓
CI runs automatically
    ↓
Image built, scanned, tagged with SHA+latest
    ↓
Pushed to registries
    ↓
Image ready for testing, but NOT deployed
    ↓
No infrastructure changes, no cost, no risk
```

**Scenario 2: Production Release**
```
Developer finishes feature, tests locally
    ↓
git tag v1.0.0
git push origin v1.0.0
    ↓
CD pipeline triggered
    ↓
Uses existing image from CI (no rebuild needed)
    ↓
Tags with semantic version v1.0.0
    ↓
▶️ SSH INTO BASTION → RUN MIGRATIONS (ONCE) ◀️
    ↓
Packer builds fresh AMI (environment only)
    ↓
Terraform updates ASG
    ↓
Rolling update deploys new version
    ↓
Zero downtime, fully automated
```

**Scenario 3: Emergency Rollback**
```
Bug discovered in v1.0.0
    ↓
Trigger CD manually with v0.9.9
    ↓
Packer uses existing AMI (no rebuild)
    ↓
Terraform updates ASG to pull v0.9.9 image
    ↓
Rolling update reverts to old version
    ↓
Downtime: zero
    ↓
Time: minutes instead of hours
```

### 🔹 Key Takeaways

| Concept | What We Learned |
|---------|-----------------|
| **CI/CD Separation** | Fast feedback for developers, controlled releases for production |
| **AMI = Environment** | Only rebuild when system changes, not for every app update |
| **App = Container** | Deploy faster by just pulling new images |
| **Tagging** | SHA for traceability, semantic versions for releases, latest for convenience |
| **Rolling Updates** | Zero-downtime deployments with ASG instance refresh |
| **Cost Optimization** | Less frequent AMI baking = lower AWS costs |
| **Bastion Host** | Secure entry point for administrative tasks in private subnets |
| **Database Migrations** | Run ONCE per deployment via Bastion host in CD pipeline, NOT in container entrypoint, to prevent race conditions in scaled environments |
| **Network Architecture** | RDS in private subnet requires migrations to be executed from within the VPC (Bastion/EC2), not directly from GitHub Actions |

---

## 🔐 Security Features

- **Defense in depth**: Multiple security layers
- **Private subnets**: RDS inaccessible from internet
- **Security group chaining**: ALB → EC2 → RDS only
- **HTTPS everywhere**: ACM certificate, HTTP → HTTPS redirect
- **Secrets management**: All credentials in GitHub Secrets
- **Image scanning**: Trivy in CI/CD pipeline
- **IAM roles**: EC2 instances have least-privilege access
- **Bastion Host**: Secure jump box for accessing private resources

---

## 📁 Repository Structure

```
falla237-aws-deploy/
│
├── .github/
│   └── workflows/
│       ├── ci.yml               # Continuous Integration pipeline (every push)
│       └── cd.yml               # Continuous Deployment pipeline (tags/manual)
│
├── terraform/
│   ├── backend-setup/          # S3 + DynamoDB (run once)
│   ├── modules/                # Reusable Terraform modules
│   │   ├── vpc/                # VPC + subnets + NAT
│   │   ├── asg/                # Auto Scaling Group + ALB
│   │   ├── bastion/            # Bastion host for admin access
│   │   └── rds/                # PostgreSQL database
│   └── environments/
│       └── prod/                # Production environment
│
├── packer/
│   └── golden-ami.pkr.hcl       # Packer template for AMI
│
├── ansible/
│   ├── playbooks/
│   │   └── provision-ami.yml    # Ansible for AMI building
│   └── roles/
│       ├── docker/               # Docker installation
│       ├── aws-cli/              # AWS CLI + ECR login
│       └── app-prep/             # App image pull & prep
│
├── app/                          # Falla237 Django source
├── Dockerfile                    # Container definition
├── .dockerignore
├── .gitignore
└── README.md                     # You are here
```

---

## 🚀 Getting Started (For Contributors)

### Prerequisites
- AWS Account with appropriate permissions
- GitHub account
- Domain name (foudadev.site) with DNS access
- Docker installed locally for testing
- SSH key pair for Bastion host access

### Initial Setup Steps
1. Clone this repository
2. Configure GitHub Secrets (AWS credentials, Docker Hub token, SSH private key, Bastion IP, DATABASE_URL, etc.)
3. Run `terraform/backend-setup/` manually to create S3 + DynamoDB
4. Test Docker build locally
5. Push to GitHub to trigger first pipeline run

---

## 📊 Key Learnings & Challenges

This project demonstrates proficiency in:

- **Infrastructure as Code**: Modular Terraform with remote state
- **Immutable Infrastructure**: Packer + Ansible for Golden AMIs
- **CI/CD Orchestration**: Multi-job GitHub Actions workflows with CI/CD separation
- **Container Management**: Multi-registry strategy with security scanning
- **AWS Networking**: VPC design with 3-AZ high availability
- **Security Best Practices**: Defense in depth, secret management, Bastion host pattern
- **Production Readiness**: Auto-scaling, health checks, rolling deployments
- **Real-World Constraints**: Working within AWS account limits
- **Tagging Strategy**: Proper image versioning with SHA, latest, and semantic tags
- **Database Migration Strategy**: Running migrations once per deployment via Bastion host in CD pipeline, preventing race conditions in auto-scaling environments
- **Network Architecture Constraints**: RDS in private subnet requires internal VPC access for migrations (Bastion/EC2)

---

## 🔮 Future Enhancements

- [ ] Replace Bastion Host with AWS Systems Manager (SSM) Session Manager for password-less access
- [ ] Add CloudWatch monitoring and alerts
- [ ] Implement blue-green deployments
- [ ] Add S3 static file hosting
- [ ] Integrate CloudFront CDN
- [ ] Add automated backup validation

---