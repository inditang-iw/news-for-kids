locals {
  source_path = "../../../src"
  output_path = "${path.module}/.output/lambda.zip"
}

output "message" {
    value = "inside lambda-cmd.tf"
}

output "cwd" {
    value = path.cwd
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

data "archive_file" "lambda_zip" {
    type        = "zip"
    source_dir  = local.source_path
    output_path = local.output_path
}

resource "aws_lambda_function" "news_for_kids" {
    filename = local.output_path
    function_name = "news-for-kids"
    role = aws_iam_role.lambda_role.arn
    handler = "rewrite_news.lambda_handler"
    runtime = "python3.9"
    timeout = "80"
    architectures = ["x86_64"]
    layers = [aws_lambda_layer_version.lambda_layer.arn]
    source_code_hash = data.archive_file.lambda_zip.output_base64sha256
}

data "aws_iam_policy_document" "instance_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "instance_inline_policy" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]

    resources = [
      "*",
    ]
  }

  statement {
    actions = [
      "ssm:GetParameter*"
    ]

    # todo: move params to a common path e.g. news-for-kids/guardian-api-key, news-for-kids/openai-api-key to restrict access only to parameter/news-for-kids/*
    resources = [
      "arn:aws:ssm:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:parameter/*",
    ]
  }
}

resource "aws_iam_role" "lambda_role" {
  name="news-for-kids-assume-role"
  assume_role_policy=data.aws_iam_policy_document.instance_assume_role_policy.json
  inline_policy {
    name   = "news-for-kids-lambda-policy"
    policy = data.aws_iam_policy_document.instance_inline_policy.json
  }
}

resource "aws_cloudwatch_event_rule" "cron_schedule" {
    name = "cron-schedule"
    description = "Fires every 00:00, 08:00, 16:00 UTC"
    schedule_expression = "cron(0 8,16 * * ? *)"
}

resource "aws_cloudwatch_event_target" "news_for_kids_event_target" {
    rule = aws_cloudwatch_event_rule.cron_schedule.name
    target_id = "news_for_kids"
    arn = aws_lambda_function.news_for_kids.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.news_for_kids.function_name
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.cron_schedule.arn
}
