module "s3" {
  source      = "./modules/s3_bucket"
  bucket_name = var.bucket_name
  cloudfront_oai_arn          = module.cloudfront.oai_arn
}

module "cloudfront" {
  source                      = "./modules/cloudfront"
  bucket_regional_domain_name = module.s3.s3_bucket_regional_domain_name
  origin_id                   = var.origin_id
}
