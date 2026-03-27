variable "aws_region" {
  type        = string
  description = "AWS region where the AMI will be built"
  default     = "us-east-1"
}

variable "source_ami_id" {
  type        = string
  description = "Base Ubuntu AMI ID used to create the Golden AMI"
  default     = "ami-0ec10929233384c7f"
}

variable "ami_name" {
  type        = string
  description = "Name prefix for the generated Golden AMI"
  default     = "falla237-golden-ami"
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type used temporarily by Packer to build the AMI"
  default     = "t3.micro"
}

variable "ssh_username" {
  type        = string
  description = "SSH username for the base Ubuntu AMI"
  default     = "ubuntu"
}