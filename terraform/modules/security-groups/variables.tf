variable "vpc_id" {
  description = "VPC ID"
}


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

variable "my_ip" {
  description = "My IP Address"
  type = string
  default = "129.0.189.191"
}