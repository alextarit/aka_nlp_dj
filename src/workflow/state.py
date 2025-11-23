from langgraph.graph import MessagesState


# TODO: make it beautiful if you don't get lazy
class InputState(MessagesState):
    pass


class OverallState(MessagesState):
    song_info: dict[str, str]


class OutputState(MessagesState):
    pass
