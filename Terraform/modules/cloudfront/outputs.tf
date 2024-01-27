output "oai_id" {
  value = aws_cloudfront_origin_access_identity.default.id
}

output "oai_arn" {
  value = aws_cloudfront_origin_access_identity.default.iam_arn
}

output "distribution_url" {
  value = aws_cloudfront_distribution.s3_distribution.domain_name
}