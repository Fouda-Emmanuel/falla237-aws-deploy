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

variable "public_subnet_id" {
  description = "Public Subnet ID"
  type = string
}

variable "bastion_security_grp_id" {
  description = "Bastion Security Group ID (from SG Module)"
  type = string
}