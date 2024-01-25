output "oai_id" {
  value = aws_cloudfront_origin_access_identity.default.id
}

output "oai_arn" {
  value = aws_cloudfront_origin_access_identity.default.iam_arn
}