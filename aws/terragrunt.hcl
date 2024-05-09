terraform_version_constraint = ">= 1.1"

terragrunt_version_constraint = ">= 0.35"

retryable_errors = [
  "(?s).*Error installing provider.*tcp.*connection reset by peer.*",
  "(?s).*timeout while waiting for plugin to start.*",
  "(?s).*Provider produced inconsistent final plan.*tags_all: new element \"Name\" has appeared.*This is a bug in the provider.*",
]

locals {
  account_id     = get_aws_account_id()
  primary_region = "eu-north-1"
}

generate "backend" {
  path      = "terragrunt.tf"

  if_exists = "overwrite_terragrunt"

  contents = <<EOF
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.48"
    }
  }

  required_version = ">= 1.1.0"

  backend "s3" {
    bucket         = "news-for-kids-baseline-terraform-state-${local.account_id}-${local.primary_region}"
    key            = "${trimprefix(path_relative_to_include(), "stacks/")}.tfstate"
    region         = "${local.primary_region}"
  }
}

provider "aws" {
  region              = "${local.primary_region}"
  allowed_account_ids = ["${local.account_id}"]
  default_tags {
    tags = {
      Stack = "${trimprefix(path_relative_to_include(), "stacks/")}"
    }
  }
}
EOF
}

generate "remote_state" {
  path      = "remote_state/terragrunt.tf"
  if_exists = "overwrite_terragrunt"

  contents = <<EOF
data "terraform_remote_state" "main" {
  backend = "s3"
  config = {
    bucket         = "news-for-kids-baseline-terraform-state-${local.account_id}-${local.primary_region}"
    region         = "${local.primary_region}"
    key            = "${trimprefix(path_relative_to_include(), "stacks/")}.tfstate"
  }
}
EOF
}

generate "remote_state_main_tf" {
  path              = "remote_state/main.tf"
  if_exists         = "skip"
  disable_signature = true
  contents          = ""
}
