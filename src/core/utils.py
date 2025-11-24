import uuid


def generate_thread_id() -> str:
    return str(uuid.uuid4())
