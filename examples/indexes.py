import asyncio

from opperai import AsyncOpper, Opper
from opperai.types import Filter


async def async_crud_index():
    opper = AsyncOpper()

    index = await opper.indexes.create(
        name="async-crud-index",
    )
    print(index)

    await index.add("hello world user", metadata={"source": "user"})
    await index.add("hello world admin", metadata={"source": "admin"})

    print(await index.query("hello world"))
    print(
        await index.query(
            "hello world",
            filters=[Filter(key="source", operation="=", value="user")],
        )
    )

    print(await index.delete())


def sync_crud_index():
    opper = Opper()

    index = opper.indexes.create(
        name="sync-crud-index",
    )
    print(index)

    index.add("hello world user", metadata={"source": "user"})
    index.add("hello world admin", metadata={"source": "admin"})

    print(index.query("hello world"))
    print(
        index.query(
            "hello world", filters=[Filter(key="source", operation="=", value="user")]
        )
    )
    print(index.delete())


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "async":
            asyncio.run(async_crud_index())
        elif sys.argv[1] == "sync":
            sync_crud_index()
    else:
        asyncio.run(async_crud_index())
        sync_crud_index()
