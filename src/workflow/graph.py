from langgraph.graph import START, StateGraph
from workflow.state import InputState, OverallState, OutputState
from langgraph.prebuilt import tools_condition, ToolNode
from workflow.nodes import reasoning_node
from workflow.tools import (
    get_lyrics_from_genius,
    get_artist_from_genius,
    get_album_from_genius,
)

tools = [
    get_lyrics_from_genius,
    get_artist_from_genius,
    get_album_from_genius,
]

builder = StateGraph(
    state_schema=OverallState, input_schema=InputState, output_schema=OutputState
)

builder.add_node(reasoning_node)
builder.add_node("tools", ToolNode(tools))


builder.add_edge(START, "reasoning_node")
builder.add_conditional_edges("reasoning_node", tools_condition)
builder.add_edge("tools", "reasoning_node")

graph = builder.compile()
