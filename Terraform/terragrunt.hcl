# Terragrunt configuration

terraform {
  # Configure Terraform version
  source = "tf"
  version = "~> 1.5.7"

  # Configure temporary backend for init
  extra_arguments "temporary_backend" {
    commands = ["init"]

    arguments = [
      "-backend-config=bucket=my-temp-bucket"
    ]
  }
}

# Remote state dependency
dependency "s3_bucket" {
  config_path = "./modules/s3_bucket"

  mock_outputs = {
    bucket_id = "temp-bucket"
  }

  mock_outputs_allowed_terraform_commands = ["init"]
}

# Configure live backend
terraform {
  backend "s3" {
    bucket         = dependency.s3_bucket.outputs.bucket_id
    key            = "terraform.tfstate"
    region         = "eu-central-1"
  }
}

# Include all config in modules
terragrunt_include {
  path = "${find_in_parent_folders()}"
}