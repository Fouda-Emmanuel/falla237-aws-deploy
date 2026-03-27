packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.8"
      source  = "github.com/hashicorp/amazon"
    }
    ansible = {
      version = ">= 1.1.0"
      source  = "github.com/hashicorp/ansible"
    }
  }
}


# SOURCE (BUILDER)
source "amazon-ebs" "golden_ami" {
  region        = var.aws_region
  instance_type = var.instance_type

  source_ami   = var.source_ami_id
  ssh_username = var.ssh_username

  ami_name = "${var.ami_name}-{{timestamp}}"

  tags = {
    Name        = "falla237-golden-ami"
    Environment = "dev"
    Project     = "falla237"
  }
}


# BUILD

build {
  name    = "falla237-golden-ami-build"
  sources = ["source.amazon-ebs.golden_ami"]

  provisioner "ansible" {
    playbook_file = "../ansible/playbooks/provision.yml"

    extra_arguments = [
      "--extra-vars",
      "ansible_python_interpreter=/usr/bin/python3"
    ]

    ansible_env_vars = [
      "ANSIBLE_ROLES_PATH=../ansible/roles"
    ]
  }

  post-processor "manifest" {
    output = "manifest.json"
  }
}