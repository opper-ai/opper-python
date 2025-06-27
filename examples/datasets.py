import asyncio
import os
from opperai import Opper


opper = Opper(http_bearer=os.getenv("OPPER_API_KEY"))


def _sync_function():
    def setup():
        return opper.functions.create(
            name="sample_dataset_function", instructions="given an input, return the same input"
        )

    def populate():
        f = setup()
        dataset_id = f.dataset_id
        d = opper.datasets.create_entry(
            dataset_id=dataset_id,
            input="Hello, world!",
            output="Hello, world!",
            expected="Hello, world!",
            comment="Example dataset entry",
        )
        print("Dataset populated with sample:")
        print(d)

        # list entries
        entries = opper.datasets.list_entries(dataset_id=dataset_id)
        print("Entries in the dataset:")
        print(entries)

        # get entry
        entry = opper.datasets.get_entry(dataset_id=dataset_id, entry_id=d.id)
        print("Entry:")
        print(entry)

        # query entries
        query = opper.datasets.query_entries(
            dataset_id=dataset_id, query="Hello, world!"
        )
        print("Query results:")
        print(query)

        # delete entry
        opper.datasets.delete_entry(dataset_id=dataset_id, entry_id=d.id)
        print("Entry deleted")

        opper.functions.delete(function_id=f.id)

    populate()


async def _async_function():
    async def setup():
        return await opper.functions.create_async(
            name="async_dataset_function", instructions="given an input, return the same input"
        )

    async def populate():
        f = await setup()
        dataset_id = f.dataset_id
        d = await opper.datasets.create_entry_async(
            dataset_id=dataset_id,
            input="Hello, world!",
            output="Hello, world!",
            expected="Hello, world!",
            comment="Example dataset entry",
        )
        print("Dataset populated with sample:")
        print(d)

        # list entries
        entries = await opper.datasets.list_entries_async(dataset_id=dataset_id)
        print("Entries in the dataset:")
        print(entries)

        # get entry
        entry = await opper.datasets.get_entry_async(dataset_id=dataset_id, entry_id=d.id)
        print("Entry:")
        print(entry)

        # query entries
        query = await opper.datasets.query_entries_async(
            dataset_id=dataset_id, query="Hello, world!"
        )
        print("Query results:")
        print(query)

        # delete entry
        opper.datasets.delete_entry_async(dataset_id=dataset_id, entry_id=d.id)
        print("Entry deleted")

        opper.functions.delete_async(function_id=f.id)

    await populate()



def run_sync():
    print("=== Synchronous Dataset Operations ===")
    _sync_function()





if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        if sys.argv[1] == "sync":
            run_sync()
        elif sys.argv[1] == "async":
            asyncio.run(_async_function())
    else:
        run_sync()
        print("\n")
        asyncio.run(_async_function())
