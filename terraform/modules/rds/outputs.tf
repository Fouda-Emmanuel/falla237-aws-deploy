output "rds_subnet_group_name" {
  description = "RDS Subnet Group"
  value = aws_db_subnet_group.db_subnet_grp.name
}

output "rds_endpoint" {
  description = "RDS Endpoint"
  value = aws_db_instance.postgres_db.address
}

output "rds_port" {
  description = "RDS Port"
  value = aws_db_instance.postgres_db.port
}