variable "scheduled_triggers" {
  type = map(object({
    name = string
    arn  = string
  }))

  default = {}
}

resource "aws_cloudwatch_event_target" "scheduled_trigger" {
  for_each  = var.scheduled_triggers
  rule      = each.value["name"]
  target_id = "lambda"
  arn       = aws_lambda_function.main.arn
}

resource "aws_lambda_permission" "scheduled_trigger" {
  for_each      = var.scheduled_triggers
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.main.function_name
  principal     = "events.amazonaws.com"
  source_arn    = each.value["arn"]
}

