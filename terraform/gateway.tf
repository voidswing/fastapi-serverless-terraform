provider "aws" {
  region = "ap-northeast-2"
}

# API Gateway 설정
resource "aws_apigatewayv2_api" "fastapi_gateway" {
  name          = "fastapi-gateway"
  protocol_type = "HTTP"
  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "OPTIONS"]
    allow_headers = ["content-type"]
  }
}

resource "aws_apigatewayv2_stage" "dev_stage" {
  api_id      = aws_apigatewayv2_api.fastapi_gateway.id
  name        = "dev"
  auto_deploy = true
}

output "api_gateway_endpoint" {
  value = aws_apigatewayv2_api.fastapi_gateway.api_endpoint
}
