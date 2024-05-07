variable "name" {
  type = string
}

output "name" {
  value = var.name
}

variable "memory" {
  type = number
}

variable "environment" {
  type    = map(string)
  default = {}
}

variable "runtime" {
  type    = string
  default = "go1.x"
}

variable "handler" {
  type    = string
  default = "main"
}

variable "timeout_seconds" {
  type = string
}

output "timeout_seconds" {
  value = var.timeout_seconds
}

variable "log_retention_in_days" {
  type    = number
  default = 30
}

variable "inline_policy_documents" {
  type    = set(string)
  default = []
}

variable "managed_policy_arns" {
  type    = set(string)
  default = []
}

variable "network_configuration" {
  type = object({
    vpc_id     = string
    subnet_ids = set(string)
  })

  default = null
}

locals {
  function_name = var.name
  resource_name = "lambda-${local.function_name}"
  vpc_enabled   = var.network_configuration != null
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

output "resource_name" {
  value = local.resource_name
}
