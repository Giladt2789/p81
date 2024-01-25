variable "region" {
  description = "The region where the resources will be deployed"
  type        = string
}

variable "aws_profile" {
  description = "AWS profile to use"
  type        = string
}

variable "bucket_name" {
  type        = string
  description = "The buckets name"
}

variable "origin_id" {
  type = string
}