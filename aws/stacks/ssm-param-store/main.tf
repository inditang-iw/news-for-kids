output "message" {
    value = "inside ssm-param-store.tf"
}

variable "parameter_names" {
    type    = list(string)
    default = []
}

resource "aws_ssm_parameter" "param" {
    lifecycle {
        ignore_changes = [
            # Ignore changes to value as it should be managed directly through aws console/api to avoid exposing secrets in git repo
            value,
        ]
    }
    count = length(var.parameter_names)
    name  = var.parameter_names[count.index]
    type  = "SecureString"
    value = "dummy"
}
