import asyncio
import os
from opperai import Opper

opper = Opper(
    http_bearer=os.getenv("OPPER_API_KEY"),
)


async def async_crud_kb():
    kb = await opper.knowledge.create_async(
        name="async-crud-kb",
    )
    print(kb)

    await opper.knowledge.add_async(
        knowledge_base_id=kb.id,
        content="hello world user",
        metadata={"source": "user"},
    )
    await opper.knowledge.add_async(
        knowledge_base_id=kb.id, content="hello world admin", metadata={"source": "admin"}
    )

    print(
        await opper.knowledge.query_async(
            knowledge_base_id=kb.id,
            query="hello world",
        )
    )
    print(
        await opper.knowledge.query_async(
            knowledge_base_id=kb.id,
            query="hello world",
            filters=[{"field": "source", "operation": "=", "value": "user"}],
        )
    )

    print(await opper.knowledge.delete_async(knowledge_base_id=kb.id))


def sync_crud_kb():
    kb = opper.knowledge.create(
        name="sync-crud-kb",
    )
    print(kb)

    opper.knowledge.add(
        knowledge_base_id=kb.id,
        content="hello world user",
        metadata={"source": "user"},
    )
    opper.knowledge.add(
        knowledge_base_id=kb.id, content="hello world admin", metadata={"source": "admin"}
    )

    print(opper.knowledge.query(knowledge_base_id=kb.id, query="hello world"))
    print(
        opper.knowledge.query(
            knowledge_base_id=kb.id,
            query="hello world",
            filters=[{"field": "source", "operation": "=", "value": "user"}],
        )
    )
    print(opper.knowledge.delete(knowledge_base_id=kb.id))


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "async":
            asyncio.run(async_crud_kb())
        elif sys.argv[1] == "sync":
            sync_crud_kb()
    else:
        asyncio.run(async_crud_kb())
        sync_crud_kb()
