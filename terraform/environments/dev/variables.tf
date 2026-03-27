# VPC Module
variable "region_name" {
  description = "VPC Region Name"
  type = string
  default = "us-east-1"
}

variable "vpc_name" {
  description = "VPC Name"
  type = string
  default = "falla237-vpc"
}

variable "vpc_cidr" {
  description = "VPC CIDR Block"
  type = string
  default = "10.0.0.0/16"
}

variable "public_sub_cidrs" {
  description = "Public Subnet CIDR Block with AZ"
  type = map(object({
    cidr = string
    az = string
  }))
  default = {
    "public-sub-1" = { cidr = "10.0.1.0/24", az="us-east-1a" },
    "public-sub-2" = { cidr = "10.0.2.0/24", az="us-east-1b" },
    "public-sub-3" = { cidr = "10.0.3.0/24", az="us-east-1c" }
  }
}

variable "private_app_cidrs" {
  description = "Private App Subnet CIDR Block with AZ"
  type = map(object({
    cidr = string
    az   = string
  }))
  default = {
    "private-app-sub-1" = { cidr = "10.0.11.0/24", az = "us-east-1a" },
    "private-app-sub-2" = { cidr = "10.0.12.0/24", az = "us-east-1b" },
    "private-app-sub-3" = { cidr = "10.0.13.0/24", az = "us-east-1c" }
  }
}

variable "private_data_cidrs" {
  description = "Private Data Subnet CIDR Block with AZ"
  type = map(object({
    cidr = string
    az   = string
  }))
  default = {
    "private-data-sub-1" = { cidr = "10.0.21.0/24", az = "us-east-1a" },
    "private-data-sub-2" = { cidr = "10.0.22.0/24", az = "us-east-1b" },
    "private-data-sub-3" = { cidr = "10.0.23.0/24", az = "us-east-1c" }
  }
}

variable "igw_name" {
  description = "Internet Gateway Name"
  type = string
  default = "falla237-igw"
}

# Security Group Module

variable "alb_sg" {
  description = "Application Load Balancer Security Group"
  type = string
  default = "alb-sg"
}

variable "app_sg" {
  description = "App Security Group"
  type = string
  default = "app-sg"
}

variable "data_sg" {
  description = "Data Security Group"
  type = string
  default = "data-sg"
}

variable "bastion_sg" {
  description = "Bastion Host Security Group"
  type = string
  default = "bastion-sg"
}


# RDS Module

variable "db_subnet_grp" {
  description = "RDS Subnet group"
  type = string
  default = "falla237-db-subnet-group"
}


variable "db_username" {
  description = "RDS Username"
}

variable "db_name" {
  description = "RDS Name"
}

variable "db_password" {
  description = "RDS Password"
}

variable "db_identifier" {
  description = "RDS Identifier"
  type = string
  default = "falla237-db"
}


# IAM-Role Module

variable "role_name" {
  description = "Name of the IAM role"
  type        = string
  default = "falla237-role"
}


# Bastion Module

variable "ami_id" {
  description = "Ubuntu AMI ID"
  type = string
  default = "ami-0ec10929233384c7f"
}

variable "instance_type" {
  description = "Instance Type"
  type = string
  default = "t3.micro"
}

variable "keypair_name" {
  description = "Key Pair Name"
  type = string
  default = "falla237-keypair"
}

variable "instance_name" {
  description = "Instance Name"
  type = string
  default = "bastion"
}
