module "vpc" {
  source = "../../modules/vpc"

  vpc_name = var.vpc_name
  region_name = var.region_name
  vpc_cidr = var.vpc_cidr
  public_sub_cidrs = var.public_sub_cidrs
  private_app_cidrs = var.private_app_cidrs
  private_data_cidrs = var.private_data_cidrs
  igw_name = var.igw_name

  local_tags = local.common_tags

}

module "security-group" {
  source = "../../modules/security-groups"

  vpc_id = module.vpc.vpc_id
  bastion_sg = var.bastion_sg
  alb_sg = var.alb_sg
  app_sg = var.app_sg
  data_sg = var.data_sg

}

module "rds" {
  source = "../../modules/rds"
  

  data_subnet_ids = module.vpc.private_data_subnet_ids
  data_security_group_id = module.security-group.data_sg_id
  db_name = var.db_name
  db_password = var.db_password
  db_username = var.db_username
  db_identifier = var.db_identifier
  db_subnet_grp = var.db_subnet_grp
}

module "iam-role" {
  source = "../../modules/iam-role"

  role_name = var.role_name
}

module "bastion" {
  source = "../../modules/bastion"

  ami_id = var.ami_id
  instance_name = var.instance_name
  instance_type = var.instance_type
  keypair_name = var.keypair_name
  public_subnet_id = module.vpc.public_subnet_ids["public-sub-1"]
  bastion_security_grp_id = module.security-group.bastion_sg_id
}