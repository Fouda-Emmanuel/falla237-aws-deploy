variable "db_subnet_grp" {
  description = "RDS Subnet group"
  type = string
  default = "falla237-db-subnet-group"
}

variable "data_subnet_ids" {
  description = "Private Data Subnet IDs"
  type = list(string)
}

variable "data_security_group_id" {
  description = "RDS Security Group ID"
  type = string
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