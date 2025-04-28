import asyncio
import os

from opperai import AsyncOpper, Opper


def synchronous_embeddings():
    # Initialize the Opper client
    api_key = os.getenv("OPPER_API_KEY")
    opper = Opper(api_key=api_key)

    # Example 1: Generate embeddings for a single string
    print("Example 1: Single text input")
    response = opper.embeddings.create(
        model="openai/text-embedding-3-large", input_text="Hello, world!"
    )

    # Print the embedding vector for the input
    print(f"Model used: {response.model}")
    print(f"Embedding dimension: {len(response.data[0]['embedding'])}")
    print(f"First few values: {response.data[0]['embedding'][:5]}")
    print(f"Usage: {response.usage}")

    # Example 2: Generate embeddings for multiple strings (batch processing)
    print("\nExample 2: List of texts input")
    batch_response = opper.embeddings.create(
        model="openai/text-embedding-3-large",
        input_text=[
            "Hello, world!",
            "How are you?",
            "Machine learning is fascinating.",
        ],
    )

    # Print the embedding vectors information
    print(f"Number of embeddings: {len(batch_response.data)}")
    for i, embedding_data in enumerate(batch_response.data):
        print(f"Embedding {i + 1} dimension: {len(embedding_data['embedding'])}")

    # Print total token usage
    print(f"Total token usage: {batch_response.usage}")


async def async_embeddings():
    # Initialize the AsyncOpper client
    api_key = os.getenv("OPPER_API_KEY")
    opper = AsyncOpper(api_key=api_key)

    # Example 1: Generate embeddings for a single string
    print("\nAsync Example 1: Single text input")
    response = await opper.embeddings.create(
        model="openai/text-embedding-3-large", input_text="Hello, world!"
    )

    # Print the embedding vector for the input
    print(f"Model used: {response.model}")
    print(f"Embedding dimension: {len(response.data[0]['embedding'])}")
    print(f"First few values: {response.data[0]['embedding'][:5]}")
    print(f"Usage: {response.usage}")

    # Example 2: Generate embeddings for multiple strings (batch processing)
    print("\nAsync Example 2: List of texts input")
    batch_response = await opper.embeddings.create(
        model="openai/text-embedding-3-large",
        input_text=[
            "Hello, world!",
            "How are you?",
            "Machine learning is fascinating.",
        ],
    )

    # Print the embedding vectors information
    print(f"Number of embeddings: {len(batch_response.data)}")
    for i, embedding_data in enumerate(batch_response.data):
        print(f"Embedding {i + 1} dimension: {len(embedding_data['embedding'])}")

    # Print total token usage
    print(f"Total token usage: {batch_response.usage}")


if __name__ == "__main__":
    print("Running synchronous embeddings example")
    synchronous_embeddings()

    print("\nRunning asynchronous embeddings example")
    asyncio.run(async_embeddings())
