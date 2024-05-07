locals {
  security_group_name = "lambda-${local.function_name}"
}

resource "aws_security_group" "main" {
  count = local.vpc_enabled ? 1 : 0

  name        = local.security_group_name
  description = local.security_group_name
  vpc_id      = var.network_configuration.vpc_id

  tags = {
    Name = local.security_group_name
  }
}

output "security_group_id" {
  value      = local.vpc_enabled ? aws_security_group.main[0].id : null
  depends_on = [aws_security_group_rule.egress]
}

resource "aws_security_group_rule" "egress" {
  count = local.vpc_enabled ? 1 : 0

  security_group_id = aws_security_group.main[0].id
  type              = "egress"
  cidr_blocks       = ["0.0.0.0/0"]
  from_port         = 0
  to_port           = 65535
  protocol          = "tcp"
}
