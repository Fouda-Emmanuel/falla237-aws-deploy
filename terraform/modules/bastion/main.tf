resource "aws_key_pair" "my_keypair" {
  key_name   = var.keypair_name
  public_key = file("~/.ssh/id_ed25519.pub")
}

resource "aws_instance" "bastion" {
  ami = var.ami_id
  instance_type = var.instance_type
  key_name = aws_key_pair.my_keypair.key_name
  subnet_id = var.public_subnet_id
  vpc_security_group_ids = [var.bastion_security_grp_id]

  tags = {
    Name = var.instance_name
  }
}