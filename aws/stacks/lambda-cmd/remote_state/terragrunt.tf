# Generated by Terragrunt. Sig: nIlQXj57tbuaRZEa
data "terraform_remote_state" "main" {
  backend = "s3"
  config = {
    bucket         = "news-for-kids-baseline-terraform-state-058264124525-eu-north-1"
    region         = "eu-north-1"
    key            = "lambda-cmd.tfstate"
  }
}