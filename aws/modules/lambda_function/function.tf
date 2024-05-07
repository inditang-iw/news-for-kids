resource "aws_cloudwatch_log_group" "main" {
  name              = "/aws/lambda/${local.function_name}"
  retention_in_days = var.log_retention_in_days
}

module "kms_key" {
  source = "../kms_key"
  alias  = local.resource_name
}

resource "aws_lambda_function" "main" {
  depends_on = [
    aws_cloudwatch_log_group.main,
  ]

  lifecycle {
    ignore_changes = [filename]
  }

  function_name = local.function_name
  role          = module.task_role.arn
  runtime       = var.runtime
  handler       = var.handler
  filename      = "${path.module}/empty.zip"
  memory_size   = var.memory
  timeout       = var.timeout_seconds
  kms_key_arn   = module.kms_key.arn

  tracing_config {
    #ts:skip=AC_AWS_0485 Terrascan isn't picking up that it's enabled.
    mode = "Active"
  }

  environment {
    variables = merge(
      {
        DOJO_PLATFORM = "aws"
      },
      var.environment,
    )
  }

  dynamic "vpc_config" {
    for_each = toset(local.vpc_enabled ? ["main"] : [])
    content {
      subnet_ids         = var.network_configuration.subnet_ids
      security_group_ids = [aws_security_group.main[0].id]
    }
  }
}
