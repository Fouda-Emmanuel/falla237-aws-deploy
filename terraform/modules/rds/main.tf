resource "aws_db_subnet_group" "db_subnet_grp" {
  name       = var.db_subnet_grp
  subnet_ids = var.data_subnet_ids

  tags = {
    Name = var.db_subnet_grp
  }
}

resource "aws_db_instance" "postgres_db" {
  identifier = var.db_identifier

  engine         = "postgres"
  engine_version  = "17.6"
  instance_class  = "db.t4g.micro"

  allocated_storage = 20
  storage_type      = "gp3"

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.db_subnet_grp.name
  vpc_security_group_ids = [var.data_security_group_id]

  publicly_accessible = false
  storage_encrypted = true

  skip_final_snapshot = true

  backup_retention_period = 7

  tags = {
    Name = var.db_identifier
  }
}