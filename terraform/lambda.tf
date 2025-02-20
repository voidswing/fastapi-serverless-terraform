resource "aws_lambda_function" "fastapi_lambda" {
  function_name = "fastapi-lambda"
  role          = aws_iam_role.lambda_execution_role.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.fastapi_repo.repository_url}:latest"
  timeout       = 30
}