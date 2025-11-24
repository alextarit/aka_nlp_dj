from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from workflow.state import AgentState
from workflow.lyrics_nodes import agent, tool_node

builder = StateGraph(AgentState)

builder.add_node("agent", agent)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

lyrics_graph = builder.compile()
