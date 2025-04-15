# app.py

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from snort_log_streamer import stream_snort_log

app = FastAPI()

# React에서 접근 가능하도록 CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 보안 강화하려면 IP/도메인 제한 가능
    allow_methods=["*"],
    allow_headers=["*"]
)

# WebSocket 엔드포인트 정의
@app.websocket("/ws/snort-log")
async def snort_log_ws(websocket: WebSocket):
    await stream_snort_log(websocket)

# 테스트용 기본 GET 엔드포인트
@app.get("/")
def root():
    return {"status": "FastAPI is running", "log": "/ws/snort-log"}
