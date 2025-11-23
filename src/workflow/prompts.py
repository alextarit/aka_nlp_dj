from langchain_core.messages import SystemMessage

reasoning_prompt = SystemMessage(
    content="""
You are a helpful assistant that can answer questions about the song.
As well as fulfill any user request aimed at creative activity in the field of music.
"""
)
