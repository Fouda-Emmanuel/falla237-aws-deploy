output "role_name" {
  description = "Role Name"
  value = aws_iam_role.my_role.name
}

output "instance_profile_name" {
  description = "Instance Profile Name"
  value = aws_iam_instance_profile.my_role_profile.name
}