output "bastion_sg_id" {
  description = "Bastion Host Security Group ID"
  value = aws_security_group.bastion_sg.id
}

output "alb_sg_id" {
  description = "Application Load Balancer Security Group ID"
  value = aws_security_group.alb_sg.id
}

output "app_sg_id" {
  description = "APP Security Group ID"
  value = aws_security_group.app_sg.id
}

output "data_sg_id" {
  description = "Data Security Group ID"
  value = aws_security_group.data_sg.id
}