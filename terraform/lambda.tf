resource "aws_lambda_function" "api"{
function_name = "tickets-api"
role = aws_iam_role.lambda.arn
 runtime = "python3.12"
 handler ="main.handler"
 filename = var.lambda_zip_path
 source_code_hash = filebase64sha256(var.lambda_zip_path)
 timeout = 10
 memory_size = 256

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.tickets.name
    }
  }

  depends_on = [aws_iam_role_policy_attachment.logs]
}
