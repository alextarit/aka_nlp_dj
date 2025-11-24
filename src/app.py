import asyncio
import time
import gradio as gr
from langchain_core.messages import HumanMessage, AIMessage
from workflow.app_graph import app_graph
from core.utils import generate_thread_id
from core.domains import UserQuery
from core.suno_client import suno_client
from core.suno_view import DefaultSunoRecordParser
from core.suno_render import DefaultSunoRenderer


def last_song_message(messages) -> str:
    for message in reversed(messages):
        if isinstance(message, AIMessage):
            meta = getattr(message, "response_metadata", {}) or {}
            if meta.get("stage") == "prepare_suno":
                continue
            if meta.get("task") or meta.get("status"):
                continue
            return str(message.content)
    return ""


def poll_status(task_id: str, max_checks: int = 20, delay: float = 5.0) -> dict:
    last = {}
    for _ in range(max_checks):
        last = suno_client.get_details(task_id) or {}
        data = last.get("data") if isinstance(last, dict) else {}
        data = data or {}
        status = data.get("status")
        if status in {
            "SUCCESS",
            "FIRST_SUCCESS",
            "GENERATE_AUDIO_FAILED",
            "CREATE_TASK_FAILED",
        }:
            return last
        response = data.get("response") or {}
        entries = response.get("sunoData") or []
        if any(
            e.get("streamAudioUrl") or e.get("audioUrl") or e.get("downloadUrl")
            for e in entries
        ):
            return last
        if not data:
            return last
        time.sleep(delay)
    return last


def render_tracks_html(record: dict) -> str:
    parser = DefaultSunoRecordParser()
    renderer = DefaultSunoRenderer()
    status, tracks, err = parser.parse(record)
    return renderer.render(status, tracks, err)


def run_workflow(query: str, suno_options: dict, thread_id: str):
    payload = UserQuery(
        thread_id=thread_id,
        query=query,
        feedback=None,
    )
    human = HumanMessage(
        content=payload.query,
        additional_kwargs={"thread_id": payload.thread_id},
    )
    msg_list = [human]
    state = {
        "messages": msg_list,
        "query": payload.query,
        "thread_id": payload.thread_id,
        "feedback": payload.feedback or "",
        "loop_count": 0,
        "suno_options": suno_options,
        "task": {},
        "status": {},
    }
    result = asyncio.run(app_graph.ainvoke(state))
    messages_out = result["messages"]
    task = result.get("task") or {}
    status = result.get("status") or {}
    song = last_song_message(messages_out)
    return song, task, status


def handle_generate(query, instrumental, model, thread_id):
    if not query or not query.strip():
        return "Добавь запрос", gr.update(value=None), thread_id
    suno_options = {"model": model, "instrumental": instrumental, "custom_mode": True}
    try:
        song, task, status = run_workflow(query.strip(), suno_options, thread_id)
    except Exception as exc:
        return f"Ошибка: {exc}", gr.update(value=""), thread_id
    task_id = task.get("taskId") or task.get("id")
    if task_id:
        status = poll_status(task_id)
    tracks_html = render_tracks_html(status)
    return song or "Текст не получен", tracks_html, thread_id


with gr.Blocks() as demo:
    gr.Markdown("# Songwriter Agent")
    query = gr.Textbox(
        label="Запрос",
        placeholder="Напиши дуэт Big Baby Tape и Oxxxymiron на тему Горгород",
        lines=4,
    )
    instrumental = gr.Checkbox(label="Инструментал", value=False)
    model = gr.Dropdown(
        choices=["V5", "V4_5PLUS", "V4_5", "V4", "V3_5"],
        value="V5",
        label="Модель Suno",
    )
    run_btn = gr.Button("Сгенерировать", variant="primary")
    song_out = gr.Markdown(label="Текст песни")
    tracks_out = gr.HTML(label="Треки")
    thread_state = gr.State(generate_thread_id())

    run_btn.click(
        handle_generate,
        inputs=[query, instrumental, model, thread_state],
        outputs=[song_out, tracks_out, thread_state],
    )


if __name__ == "__main__":
    demo.queue().launch()
