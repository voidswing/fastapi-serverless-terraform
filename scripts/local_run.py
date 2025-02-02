import subprocess
import os
import argparse

IMAGE_NAME = "fastapi"
CONTAINER_NAME = "fastapi_container"


def change_workdir():
    workdir = os.path.join(os.path.dirname(__file__), "../fastapi")
    return os.path.abspath(workdir)


def build_image(workdir):
    print(f"Building Docker image: {IMAGE_NAME}")
    subprocess.run(["docker", "build", "-t", IMAGE_NAME, "."], cwd=workdir, check=True)


def run_container(port):
    print(f"Running container: {CONTAINER_NAME} on port {port}")
    subprocess.run(["docker", "run", "-d", "-p", f"{port}:{8000}", "--name", CONTAINER_NAME, IMAGE_NAME], check=True)


def main():
    parser = argparse.ArgumentParser(description="Build and run FastAPI Docker container locally.")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the container on (default: 8000)")
    args = parser.parse_args()

    workdir = change_workdir()

    try:
        build_image(workdir)
        run_container(args.port)
        print(f"Docker container is running on port {args.port}!")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
