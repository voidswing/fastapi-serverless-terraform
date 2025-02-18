import subprocess
import os

AWS_REGION = "ap-northeast-2"
IMAGE_NAME = "fastapi-lambda"


def change_workdir():
    """fastapi 폴더로 이동"""
    workdir = os.path.join(os.path.dirname(__file__), "../fastapi")
    return os.path.abspath(workdir)


def run_command(cmd, cwd=None):
    """CLI 명령어 실행 후 출력"""
    result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True, cwd=cwd)
    print(result.stdout.strip())
    return result.stdout.strip()


def get_ecr_uri():
    """ECR 리포지토리 URI 조회"""
    cmd = f"aws ecr describe-repositories --region {AWS_REGION} --query \"repositories[?repositoryName=='{IMAGE_NAME}'].repositoryUri\" --output text"
    return run_command(cmd)


def build_and_push_image():
    """Docker 이미지 빌드 후 ECR로 푸시"""
    workdir = change_workdir()
    ecr_uri = get_ecr_uri()

    print("🔨 Building Docker Image...")
    run_command(f"docker build -t {IMAGE_NAME} .", cwd=workdir)

    print("🔑 Logging into AWS ECR...")
    run_command(
        f"aws ecr get-login-password --region {AWS_REGION} | docker login --username AWS --password-stdin {ecr_uri}"
    )

    print("🏷️ Tagging Image...")
    run_command(f"docker tag {IMAGE_NAME}:latest {ecr_uri}:latest")

    print("📤 Pushing Image to ECR...")
    run_command(f"docker push {ecr_uri}:latest")


def main():
    try:
        build_and_push_image()
        print("🎉 ECR Deployment Complete!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")


if __name__ == "__main__":
    main()
