resource "aws_s3_bucket" "my_bucket" {
  bucket = var.bucket_name
  tags = {
    Name = "S3_bucket"
    Owner = "Gilad_Tayeb"
    Terraform = "True"
  }
}

resource "aws_s3_bucket_versioning" "my_bucket_versioning" {
  bucket = aws_s3_bucket.my_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

data "aws_iam_policy_document" "allow_oai_access" {
   statement {
     actions   = ["s3:GetObject"]
     resources = ["${aws_s3_bucket.my_bucket.arn}/*"]

     principals {
       type        = "AWS"
       identifiers = [var.cloudfront_oai_arn]
     }
   }
 }

resource "aws_s3_bucket_policy" "allow_cloudfront_oai" {
  bucket = aws_s3_bucket.my_bucket.id
  policy = data.aws_iam_policy_document.allow_oai_access.json
}