resource "aws_security_group" "bastion_sg" {
  name        = var.bastion_sg
  description = "Bastion Host Security Group"
  vpc_id      = var.vpc_id

  tags = {
    Name = var.bastion_sg
  }
}

resource "aws_vpc_security_group_ingress_rule" "ssh_from_my_ip" {
  security_group_id = aws_security_group.bastion_sg.id
  from_port         = 22
  ip_protocol       = "tcp"
  to_port           = 22
  cidr_ipv4         = "${var.my_ip}/32"
}

resource "aws_vpc_security_group_egress_rule" "bastion_outbound" {
  security_group_id = aws_security_group.bastion_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1" 
}

resource "aws_security_group" "alb_sg" {
  name        = var.alb_sg
  description = "Application Load Balancer Security Group"
  vpc_id      = var.vpc_id

  tags = {
    Name = var.alb_sg
  }
}

resource "aws_vpc_security_group_ingress_rule" "alb_http" {
  security_group_id = aws_security_group.alb_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 80
  ip_protocol       = "tcp"
  to_port           = 80
}

resource "aws_vpc_security_group_ingress_rule" "alb_https" {
  security_group_id = aws_security_group.alb_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 443
  ip_protocol       = "tcp"
  to_port           = 443
}

resource "aws_vpc_security_group_egress_rule" "alb_outbound_ipv4" {
  security_group_id = aws_security_group.alb_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1" 
}


resource "aws_security_group" "app_sg" {
  name        = var.app_sg
  description = "App Security Group"
  vpc_id      = var.vpc_id

  tags = {
    Name = var.app_sg
  }
}

resource "aws_vpc_security_group_ingress_rule" "app_from_alb" {
  security_group_id = aws_security_group.app_sg.id
  from_port         = 8000
  ip_protocol       = "tcp"
  to_port           = 8000
  referenced_security_group_id = aws_security_group.alb_sg.id
}

resource "aws_vpc_security_group_ingress_rule" "app_ssh_from_bastion" {
  security_group_id = aws_security_group.app_sg.id
  from_port         = 22
  ip_protocol       = "tcp"
  to_port           = 22
  referenced_security_group_id = aws_security_group.bastion_sg.id
}


resource "aws_vpc_security_group_egress_rule" "app_outbound" {
  security_group_id = aws_security_group.app_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1" 
}


resource "aws_security_group" "data_sg" {
  name        = var.data_sg
  description = "Data Security Group (For Database)"
  vpc_id      = var.vpc_id

  tags = {
    Name = var.data_sg
  }
}

resource "aws_vpc_security_group_ingress_rule" "data_from_app" {
  security_group_id = aws_security_group.data_sg.id
  from_port         = 5432
  ip_protocol       = "tcp"
  to_port           = 5432
  referenced_security_group_id = aws_security_group.app_sg.id
}

resource "aws_vpc_security_group_ingress_rule" "data_from_bastion" {
  security_group_id = aws_security_group.data_sg.id
  from_port         = 5432
  ip_protocol       = "tcp"
  to_port           = 5432
  referenced_security_group_id = aws_security_group.bastion_sg.id
}
