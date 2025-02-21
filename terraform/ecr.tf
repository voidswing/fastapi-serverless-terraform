
resource "aws_ecr_repository" "fastapi_repo" {
  name = "fastapi-lambda"
}


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


output "ecr_repository_url" {
  value = aws_ecr_repository.fastapi_repo.repository_url
}
