terraform {
  backend "s3" {
    bucket = "ecr-user-service"
    key    = "ecr-user-service/terraform.tfstate"
    region = "us-east-1"
  }


}

provider "aws" {
  region = var.regionDefault
}
