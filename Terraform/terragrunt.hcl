remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket = get_env("STATE_FILES_BUCKET")

    key = "${path_relative_to_include()}/terraform.tfstate"
    region         = get_env("REGION")
    encrypt        = true
    dynamodb_table = get_env("STATEFILE_LOCK_TABLE")
  }
}

terraform {
  source = "provider.tf"
  terraform_binary_constraints = ""
}