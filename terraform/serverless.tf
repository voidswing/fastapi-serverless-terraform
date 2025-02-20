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

# ✅ ECR 리포지토리 생성
resource "aws_ecr_repository" "fastapi_repo" {
  name = "fastapi-lambda"
}

# ✅ ECR 라이프사이클 정책 (최신 5개 이미지만 유지)
resource "aws_ecr_lifecycle_policy" "fastapi_lifecycle" {
  repository = aws_ecr_repository.fastapi_repo.name
  policy     = jsonencode({
    rules = [{
      rulePriority = 1,
      description  = "Keep only the latest 5 images",
      selection    = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 5
      },
      action = {
        type = "expire"
      }
    }]
  })
}

# ✅ Lambda 실행을 위한 IAM 역할
resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# ✅ Lambda가 ECR에서 이미지 가져올 수 있도록 권한 추가
resource "aws_iam_policy" "ecr_access_policy" {
  name        = "ECRAccessPolicy"
  description = "Allows Lambda to pull images from ECR"
  policy      = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:GetAuthorizationToken"
        ],
        Resource = "*"
      }
    ]
  })
}

# IAM 역할에 정책 연결
resource "aws_iam_role_policy_attachment" "lambda_ecr_attachment" {
  policy_arn = aws_iam_policy.ecr_access_policy.arn
  role       = aws_iam_role.lambda_execution_role.name
}

# ✅ 출력 값 추가 (API Gateway & ECR URL)
output "api_gateway_endpoint" {
  value = aws_apigatewayv2_api.fastapi_gateway.api_endpoint
}

output "ecr_repository_url" {
  value = aws_ecr_repository.fastapi_repo.repository_url
}
