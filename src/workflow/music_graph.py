from langgraph.graph import START, END, StateGraph
from workflow.state import MusicState
from workflow.music_nodes import generate_track, fetch_status

builder = StateGraph(MusicState)

builder.add_node("generate", generate_track)
builder.add_node("status", fetch_status)

builder.add_edge(START, "generate")
builder.add_edge("generate", "status")
builder.add_edge("status", END)

music_graph = builder.compile()
