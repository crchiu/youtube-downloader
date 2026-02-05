import uuid
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

from app.worker import (
    tasks,
    task_queue,
    worker,
    active_workers
)

app = FastAPI(title="YouTube Downloader API")


class DownloadRequest(BaseModel):
    url: HttpUrl
    format: str  # mp3 | mp4


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(worker())

@app.get("/stats")
def get_stats():
    return {
        "workers_active": active_workers,
        "queue_size": task_queue.qsize(),
        "total_tasks": len(tasks)
    }

@app.post("/download")
async def create_download(req: DownloadRequest):
    fmt = req.format.lower()
    if fmt not in ["mp3", "mp4"]:
        raise HTTPException(status_code=400, detail="format must be mp3 or mp4")

    task_id = str(uuid.uuid4())

    tasks[task_id] = {
        "status": "pending",
        "url": str(req.url),
        "format": fmt
    }

    await task_queue.put(task_id)

    return {
        "task_id": task_id,
        "status": "pending"
    }


@app.get("/download/{task_id}")
def get_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="task not found")

    return tasks[task_id]
