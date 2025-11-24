from langgraph.graph import START, END, StateGraph
from workflow.state import AppState
from workflow.lyrics_graph import lyrics_graph
from workflow.music_graph import music_graph
from workflow.prepare_suno import prepare_suno_request
from langgraph.types import RetryPolicy


builder = StateGraph(AppState)

builder.add_node(
    "lyrics",
    lyrics_graph,
    retry_policy=RetryPolicy(max_attempts=3, initial_interval=1.0),
)
builder.add_node(
    "prepare_suno",
    prepare_suno_request,
    retry_policy=RetryPolicy(max_attempts=3, initial_interval=1.0),
)
builder.add_node(
    "music", music_graph, retry_policy=RetryPolicy(max_attempts=3, initial_interval=1.0)
)

builder.add_edge(START, "lyrics")
builder.add_edge("lyrics", "prepare_suno")
builder.add_edge("prepare_suno", "music")
builder.add_edge("music", END)

app_graph = builder.compile()
