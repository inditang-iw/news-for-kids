#define variables
locals {
  environment       = "dev"
  layer_path        = ".output"
  layer_zip_name    = "layer.zip"
  layer_name        = "lambda_layer_${local.environment}"
  requirements_name = "requirements.txt"
  requirements_path = "${path.cwd}/${local.requirements_name}"
}

# create zip file from requirements.txt. Triggers only when the file is updated
# you don't need the requirements.txt from the project as many of the packages 
# are present in lambda runtime, so only put those packages not in lambda runtime
# (e.g. openai) in this requirements.txt
resource "null_resource" "lambda_layer" {
  triggers = {
    requirements = filesha1(local.requirements_path)
  }
  # the command to install python and dependencies to the machine and zips
  provisioner "local-exec" {
    command = <<EOT
      cd ${local.layer_path}
      rm -rf python
      mkdir python
      pip3 install -r ${local.requirements_path} --platform manylinux2014_x86_64 -t python/ --implementation cp --python-version 3.9 --only-binary=:all:
      rm ${local.layer_zip_name}
      zip -r ${local.layer_zip_name} python/
    EOT
  }
}

# create lambda layer from s3 object
resource "aws_lambda_layer_version" "lambda_layer" {
  filename            = "${local.layer_path}/${local.layer_zip_name}"
  layer_name          = local.layer_name
  compatible_runtimes = ["python3.9"]
  compatible_architectures = ["x86_64"]
  source_code_hash    = filebase64sha256("${local.layer_path}/${local.layer_zip_name}")
}
