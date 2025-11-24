import asyncio
from langchain_core.messages import AIMessage
from workflow.state import MusicState
from core.suno_client import suno_client


async def generate_track(state: MusicState) -> MusicState:
    request = state["request"]
    result = await asyncio.to_thread(suno_client.generate, request)
    message = AIMessage(
        content=f"Suno task: {result.get('taskId') or result}",
        response_metadata={"task": result},
    )
    return {"task": result, "messages": [message]}


async def fetch_status(state: MusicState) -> MusicState:
    task = state.get("task") or {}
    task_id = task.get("taskId") or task.get("id")
    if not task_id:
        return {"status": {}, "messages": []}
    status = await asyncio.to_thread(suno_client.get_details, task_id)
    message = AIMessage(
        content=f"Suno status: {status.get('data', status) if status else 'нет данных'}",
        response_metadata={"status": status},
    )
    return {"status": status, "messages": [message]}
