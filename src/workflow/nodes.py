import logging
from langchain_openai import ChatOpenAI
from workflow.tools import (
    get_lyrics_from_genius,
    get_artist_from_genius,
    get_album_from_genius,
)
from conf.settings import settings
from workflow.state import OverallState

client_llm = ChatOpenAI(
    model="gpt-4o-mini", temperature=0.0, api_key=settings.DEEPSEEK_API_KEY
)

tools = [
    get_lyrics_from_genius,
    get_artist_from_genius,
    get_album_from_genius,
]
client_llm_with_tools = ChatOpenAI(
    model="gpt-4o-mini", temperature=0.0, api_key=settings.DEEPSEEK_API_KEY
).bind_tools(tools)

logger = logging.getLogger(__name__)


async def reasoning_node(state: OverallState) -> OverallState:
    """
    Node for reasoning about the question user
    """
    response = await client_llm_with_tools.ainvoke(state["messages"])
    print(response)
    return {"messages": [response]}
