import subprocess
import os
import argparse

IMAGE_NAME = "fastapi"
CONTAINER_NAME = "fastapi_container"


def change_workdir():
    """fastapi 폴더로 이동"""
    workdir = os.path.join(os.path.dirname(__file__), "../fastapi")
    return os.path.abspath(workdir)


def run_command(cmd):
    """CLI 명령어 실행 후 결과 반환"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.returncode


def remove_existing_container():
    """기존 실행 중인 컨테이너가 있으면 중지 후 삭제"""
    print(f"🔍 Checking for existing container: {CONTAINER_NAME}")

    output, _ = run_command(f"docker ps -a --filter 'name={CONTAINER_NAME}' --format '{{{{.ID}}}}'")
    if output:
        print(f"🛑 Stopping and removing existing container: {CONTAINER_NAME}")
        run_command(f"docker rm -f {CONTAINER_NAME}")


def build_image(workdir):
    """Docker 이미지 빌드"""
    print(f"🔨 Building Docker image: {IMAGE_NAME}")
    subprocess.run(["docker", "build", "-t", IMAGE_NAME, ".", "-f", "Dockerfile.local"], cwd=workdir, check=True)


def run_container(port):
    """새로운 컨테이너 실행"""
    print(f"🚀 Running container: {CONTAINER_NAME} on port {port}")
    subprocess.run(["docker", "run", "-d", "-p", f"{port}:{8000}", "--name", CONTAINER_NAME, IMAGE_NAME], check=True)


def main():
    parser = argparse.ArgumentParser(description="Build and run FastAPI Docker container locally.")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the container on (default: 8000)")
    args = parser.parse_args()

    workdir = change_workdir()

    try:
        remove_existing_container()  # 기존 컨테이너 제거
        build_image(workdir)  # Docker 이미지 빌드
        run_container(args.port)  # 새로운 컨테이너 실행
        print(f"🎉 Docker container is running on port {args.port}!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
