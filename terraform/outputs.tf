output "table_name" {
  value = aws_dynamodb_table.tickets.name
}
output "table_arn" {
  value = aws_dynamodb_table.tickets.arn
}