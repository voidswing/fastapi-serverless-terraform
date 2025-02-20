from fastapi import FastAPI
from mangum import Mangum  # Lambda용 어댑터

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Lambda!"}


# ✅ Lambda 실행을 위한 핸들러 설정
handler = Mangum(app)
