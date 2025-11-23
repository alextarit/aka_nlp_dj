import asyncio
from logger.logger import init_logs
from workflow.graph import graph
from langchain_core.messages import HumanMessage


def main():
    init_logs()

    asyncio.run(
        graph.ainvoke(
            {
                "messages": [
                    HumanMessage(
                        content="Напиши песню Big Baby Tape об октяборьском вечере рифмовкой dragonborn"
                    )
                ]
            }
        )
    )


if __name__ == "__main__":
    main()
