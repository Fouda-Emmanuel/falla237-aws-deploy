terraform {
  backend "s3" {
    bucket = "emson-iam-s3-bucket"
    key = "dev/terraform.tfstate"
    region = "us-east-1"
    dynamodb_table = "my-state-lock-record"
    encrypt = true
  }
}