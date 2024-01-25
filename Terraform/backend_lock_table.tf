resource "aws_dynamodb_table" "terraform_locks" {
  name         = "assignment-statefile-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
  tags = {
    Name = "DynamoDB_Table"
    Owner = "Gilad_Tayeb"
    Terraform = "True"
  }
}
