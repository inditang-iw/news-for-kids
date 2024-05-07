output "message" {
    value = "inside lambda-cmd.tf"
}

output "cwd" {
    value = path.cwd
}

data "archive_file" "lambda_zip" {
    type        = "zip"
    source_dir  = "../../../src"
    output_path = "../../../.output/check_foo.zip"
}

# resource "aws_lambda_function" "check_foo" {
#     filename = "check_foo.zip"
#     function_name = "checkFoo"
#     role = "${aws_iam_role.check_foo_role.id}"
#     handler = "rewrite_news.lambda_handler"
# }
# 
# resource "aws_iam_role" "check_foo_role" {
#   name="check-foo-assume-role"
#   # assume_role_policy="assume_role_policy.json"
#   assume_role_policy = <<EOF
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Action": "sts:AssumeRole",
#       "Principal": {
#         "Service": "lambda.amazonaws.com"
#       },
#       "Effect": "Allow",
#       "Sid": ""
#     },
#     {
#       "Effect": "Allow",
#       "Action": [
#         "logs:CreateLogGroup",
#         "logs:CreateLogStream",
#         "logs:PutLogEvents"
#       ],
#       "Resource": ["*"]
#     }
#     # todo: add one more statement for ssm:GetParameter
#     # todo: move params to a common path e.g. news-for-kids/guardian-api-key, news-for-kids/openai-api-key to restrict access only to parameter/news-for-kids/*
#     {
#       "Effect": "Allow",
#       "Action": ["ssm:GetParameter*"],
#       "Resource": ["arn:aws:ssm:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:parameter/*"]
#     }
#   ]
# }
# EOF
# }
# 
# resource "aws_cloudwatch_event_rule" "cron_schedule" {
#     name = "cron-schedule"
#     description = "Fires every 00:00, 08:00, 16:00"
#     schedule_expression = "cron(0 0,8,16 * * *)"
# }
# 
# resource "aws_cloudwatch_event_target" "check_foo_every_five_minutes" {
#     rule = aws_cloudwatch_event_rule.cron_schedule.name
#     target_id = "check_foo"
#     arn = aws_lambda_function.check_foo.arn
# }
# 
# resource "aws_lambda_permission" "allow_cloudwatch_to_call_check_foo" {
#     statement_id = "AllowExecutionFromCloudWatch"
#     action = "lambda:InvokeFunction"
#     function_name = aws_lambda_function.check_foo.function_name
#     principal = "events.amazonaws.com"
#     source_arn = aws_cloudwatch_event_rule.every_five_minutes.arn
# }
