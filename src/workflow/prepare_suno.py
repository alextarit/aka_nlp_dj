from pydantic import BaseModel
from langchain_core.messages import AIMessage
from core.llm_factory import get_llm_factory
from workflow.prompts import build_suno_prepare_messages
from workflow.state import MusicState
from core.suno_prepare import SunoPayload, DefaultSunoPreparer


class SunoExtract(BaseModel):
    title: str
    style: str
    prompt: str


preparer = DefaultSunoPreparer()
llm_factory = get_llm_factory()


async def prepare_suno_request(state: MusicState) -> MusicState:
    options = state.get("suno_options")
    song_text = ""
    for message in reversed(state.get("messages", [])):
        if isinstance(message, AIMessage):
            song_text = str(message.content)
            break
    if not song_text and state.get("messages"):
        song_text = str(state["messages"][-1].content)
    extractor = llm_factory.chat(temperature=0.2).with_structured_output(SunoExtract)
    prompt_messages = build_suno_prepare_messages(state.get("query", ""), song_text)
    parsed = await extractor.ainvoke(prompt_messages)
    prompt_text = options.get("prompt") or parsed.prompt
    payload = SunoPayload(
        prompt=prompt_text,
        style=options.get("style") or parsed.style,
        title=options.get("title") or parsed.title,
    )
    request = preparer.build(payload, options)
    message = AIMessage(
        content=f"Готовим трек: {request.title} / {request.style}",
        response_metadata={"stage": "prepare_suno"},
    )
    return {"request": request, "messages": [message]}
