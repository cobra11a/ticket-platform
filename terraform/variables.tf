variable "aws_region" {
  default     = "ap-south-1"
  description = "AWS region for all resources"
  type        = string

}

variable "table_name" {
  default     = "tickets"
  description = "DynamoDB table name"
  type        = string

}

variable "lambda_zip_path" {
  default     = "..//build/lambda.zip"
  description = "Path to the packaged Lambda zip"
  type        = string

}
