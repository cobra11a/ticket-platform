output "table_name" {
  value = aws_dynamodb_table.tickets.name
}
output "table_arn" {
  value = aws_dynamodb_table.tickets.arn
}
output "lambda_function_name" {
  value = aws_lambda_function.api.function_name
}
output "api_url" {
  description = "Base URL of the deployed API"
  value       = aws_apigatewayv2_api.http.api_endpoint
}