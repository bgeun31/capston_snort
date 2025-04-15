# snort_log_streamer.py

import asyncio
from fastapi import WebSocket

# Snort 로그 파일 경로 (필요 시 alert.fast 또는 다른 파일명으로 수정)
SNORT_LOG_PATH = "/var/log/snort/snort.alert.fast"

async def stream_snort_log(websocket: WebSocket):
    await websocket.accept()
    process = await asyncio.create_subprocess_exec(
        "tail", "-F", SNORT_LOG_PATH,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    try:
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            await websocket.send_text(line.decode())
    except Exception as e:
        print("[Snort Log Streaming Error]", e)
    finally:
        process.kill()
        await websocket.close()

