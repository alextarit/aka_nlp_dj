from langgraph.graph import MessagesState
from core.domains import SunoRequest, SunoOptions


class AgentState(MessagesState):
    query: str
    thread_id: str
    feedback: str | None
    loop_count: int


class MusicState(MessagesState):
    query: str
    thread_id: str
    feedback: str | None
    suno_options: dict | SunoOptions
    request: SunoRequest | None
    task: dict
    status: dict


class AppState(MessagesState):
    query: str
    thread_id: str
    feedback: str | None
    loop_count: int
    suno_options: dict | SunoOptions
    request: SunoRequest | None
    task: dict
    status: dict
