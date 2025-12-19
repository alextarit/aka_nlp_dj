from langchain_core.messages import AIMessage
from langgraph.prebuilt import ToolNode
from utils.llm_retry import create_llm
from workflow.prompts import lyrics_system_message
from workflow.state import AgentState
from workflow.tools import fetch_lyrics_async, rag_enrich_async


tools = [fetch_lyrics_async, rag_enrich_async]


llm_with_tools = create_llm(temperature=0.2).bind_tools(tools)


async def agent(state: AgentState) -> AgentState:
    history = [lyrics_system_message, *state["messages"]]
    response = await llm_with_tools.ainvoke(history)
    return {
        "messages": [
            AIMessage(
                content=response.content,
                tool_calls=response.tool_calls,
                response_metadata=response.response_metadata,
            )
        ],
        "loop_count": state.get("loop_count", 0) + 1,
    }


tool_node = ToolNode(tools)
