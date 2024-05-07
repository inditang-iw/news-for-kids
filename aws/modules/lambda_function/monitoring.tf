module "metrics" {
  source = "../lambda_metrics"

  function_name  = aws_lambda_function.main.function_name
  log_group_name = aws_cloudwatch_log_group.main.name
}
