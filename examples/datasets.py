from opperai import AsyncOpper, Opper
from opperai.types.datasets import DatasetEntry


def _sync_call():
    opper = Opper()

    name = "test_sync_call"

    def setup():
        opper.call(
            name=name,
            input="Hello, world!",
        )

        f = opper.functions.get(name=name)

        return f

    def populate():
        f = setup()
        dataset = f.dataset()

        dataset.add(
            DatasetEntry(
                input="Hello, world!",
                output="Hello, world!",
            )
        )

        for entry in dataset.get_entries():
            print(entry)

    populate()


def _sync_function():
    opper = Opper()

    def setup():
        f = opper.functions.create(
            name="test_sync",
            instructions="given an input, return the same input",
        )

        return f

    def populate():
        f = setup()
        dataset = f.dataset()
        dataset.add(
            DatasetEntry(
                input="Hello, world!",
                output="Hello, world!",
            )
        )

        for entry in dataset.get_entries():
            print(entry)

    populate()


async def _async_call():
    opper = AsyncOpper()

    name = "test_async_call"

    async def setup():
        await opper.call(name=name, input="Hello, world!")

        f = await opper.functions.get(name=name)

        return f

    async def populate():
        f = await setup()
        dataset = f.dataset()
        await dataset.add(
            DatasetEntry(
                input="Hello, world!",
                output="Hello, world!",
            )
        )

        for entry in await dataset.get_entries():
            print(entry)

    await populate()


async def _async_function():
    opper = AsyncOpper()

    async def setup():
        f = await opper.functions.create(
            name="test_async",
            instructions="given an input, return the same input",
        )

        return f

    async def populate():
        f = await setup()
        dataset = f.dataset()
        await dataset.add(
            DatasetEntry(
                input="Hello, world!",
                output="Hello, world!",
            )
        )
        for entry in await dataset.get_entries():
            print(entry)

    await populate()


def run_sync():
    _sync_call()
    _sync_function()


async def run_async():
    await _async_call()
    await _async_function()


if __name__ == "__main__":
    import asyncio
    import sys

    if len(sys.argv) == 2:
        if sys.argv[1] == "sync":
            print("Sync function")
            run_sync()
        elif sys.argv[1] == "async":
            print("Async function")
            asyncio.run(run_async())
    else:
        print("Sync call")
        run_sync()
        print("Async call")
        asyncio.run(run_async())
