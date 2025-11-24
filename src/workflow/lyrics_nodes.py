from langchain_core.messages import AIMessage
from langgraph.prebuilt import ToolNode
from core.llm_factory import get_llm_factory
from workflow.prompts import lyrics_system_message
from workflow.state import AgentState
from workflow.tools import fetch_lyrics_async, rag_enrich_async


tools = [fetch_lyrics_async, rag_enrich_async]


llm_factory = get_llm_factory()
llm_with_tools = llm_factory.chat(temperature=0.2).bind_tools(tools)


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
