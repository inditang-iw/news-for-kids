variable "source_kinesis_streams" {
  type = map(object({
    arn        = string
    batch_size = number
    filter     = string
  }))
  default = {}
}

locals {
  source_kinesis_streams = merge(
    {
      for k, v in var.source_kinesis_streams :
      k => v
      if !can(regex("\\/consumer\\/", v.arn))
    },
    {
      for k, v in var.source_kinesis_streams :
      k => merge(
        v,
        {
          arn = join("/", slice(split("/", v["arn"]), 0, 2))
        }
      )
      if can(regex("\\/consumer\\/", v.arn))
    }
  )

  source_kinesis_consumers = {
    for k, v in var.source_kinesis_streams :
    k => v
    if can(regex("/consumer/", v.arn))
  }
}

resource "aws_lambda_event_source_mapping" "source_kinesis_stream" {
  for_each   = var.source_kinesis_streams
  depends_on = [aws_iam_role_policy.source_kinesis_stream]

  function_name     = aws_lambda_function.main.function_name
  batch_size        = each.value.batch_size
  enabled           = true
  event_source_arn  = each.value.arn
  starting_position = "TRIM_HORIZON"

  function_response_types = ["ReportBatchItemFailures"]

  dynamic "filter_criteria" {
    for_each = each.value.filter != "" && each.value.filter != null ? ["main"] : []

    content {
      filter {
        pattern = each.value.filter
      }
    }
  }
}

resource "aws_iam_role_policy" "source_kinesis_stream" {
  count = length(var.source_kinesis_streams) > 0 ? 1 : 0

  role   = module.task_role.name
  policy = data.aws_iam_policy_document.source_kinesis_stream[0].json
}

data "aws_iam_policy_document" "source_kinesis_stream" {
  count = length(var.source_kinesis_streams) > 0 ? 1 : 0

  statement {
    effect = "Allow"
    actions = [
      "kinesis:DescribeStream",
      "kinesis:DescribeStreamSummary",
      "kinesis:GetRecords",
      "kinesis:GetShardIterator",
      "kinesis:ListShards",
    ]
    resources = [for k, v in local.source_kinesis_streams : v["arn"]]
  }

  dynamic "statement" {
    for_each = length(local.source_kinesis_consumers) > 0 ? ["main"] : []
    content {
      effect    = "Allow"
      actions   = ["kinesis:SubscribeToShard"]
      resources = [for k, v in local.source_kinesis_consumers : v["arn"]]
    }
  }
}
