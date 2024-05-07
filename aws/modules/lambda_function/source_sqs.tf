variable "source_sqs_queues" {
  type = map(object({
    arn        = string
    batch_size = number
    key_arn    = string
  }))

  default = {}
}

resource "aws_lambda_permission" "source_sqs_queue" {
  for_each      = var.source_sqs_queues
  depends_on    = [aws_iam_role_policy.source_sqs_queue]
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.main.function_name
  principal     = "sqs.amazonaws.com"
}

resource "aws_lambda_event_source_mapping" "input_queues" {
  for_each         = var.source_sqs_queues
  depends_on       = [aws_lambda_permission.source_sqs_queue]
  event_source_arn = each.value["arn"]
  function_name    = aws_lambda_function.main.function_name
  batch_size       = each.value["batch_size"]
}

resource "aws_iam_role_policy" "source_sqs_queue" {
  count = length(var.source_sqs_queues) > 0 ? 1 : 0

  role   = module.task_role.name
  policy = data.aws_iam_policy_document.source_sqs_queue[0].json
}

data "aws_iam_policy_document" "source_sqs_queue" {
  count = length(var.source_sqs_queues) > 0 ? 1 : 0

  statement {
    effect = "Allow"
    actions = [
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
    ]
    resources = [
      for k, v in var.source_sqs_queues : v["arn"]
    ]
  }

  statement {
    effect  = "Allow"
    actions = ["kms:Decrypt"]
    resources = [
      for k, v in var.source_sqs_queues : v["key_arn"]
    ]
  }
}
