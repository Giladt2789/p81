output "bucket_name" {
  value = aws_s3_bucket.my_bucket.id
}

output "s3_bucket_regional_domain_name" {
  value = aws_s3_bucket.my_bucket.bucket_regional_domain_name
}