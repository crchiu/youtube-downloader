import asyncio
from typing import Dict
from app.downloader import download_youtube

tasks: Dict[str, dict] = {}
task_queue: asyncio.Queue = asyncio.Queue()

# 🔹 新增：目前有多少 worker 正在跑任務
active_workers = 0


async def worker():
    global active_workers

    while True:
        task_id = await task_queue.get()
        active_workers += 1

        task = tasks[task_id]
        try:
            tasks[task_id]["status"] = "downloading"

            filename = await asyncio.to_thread(
                download_youtube,
                task["url"],
                task["format"],
                task_id
            )

            tasks[task_id]["status"] = "completed"
            tasks[task_id]["file"] = filename

        except Exception as e:
            tasks[task_id]["status"] = "failed"
            tasks[task_id]["error"] = str(e)

        finally:
            active_workers -= 1
            task_queue.task_done()
