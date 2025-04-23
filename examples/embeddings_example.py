import os

from opperai import Opper

# Initialize the Opper client
api_key = os.getenv("OPPER_API_KEY")
opper = Opper(api_key=api_key)

# Example 1: Generate embeddings for a single string
print("Example 1: Single text input")
response = opper.embeddings.create(
    model="text-embedding-ada-002", input_text="Hello, world!"
)

# Print the embedding vector for the input
print(f"Model used: {response.model}")
print(f"Embedding dimension: {len(response.data[0]['embedding'])}")
print(f"First few values: {response.data[0]['embedding'][:5]}")
print(f"Usage: {response.usage}")

# Example 2: Generate embeddings for multiple strings (batch processing)
print("\nExample 2: List of texts input")
batch_response = opper.embeddings.create(
    model="text-embedding-ada-002",
    input_text=["Hello, world!", "How are you?", "Machine learning is fascinating."],
)

# Print the embedding vectors information
print(f"Number of embeddings: {len(batch_response.data)}")
for i, embedding_data in enumerate(batch_response.data):
    print(f"Embedding {i+1} dimension: {len(embedding_data['embedding'])}")

# Print total token usage
print(f"Total token usage: {batch_response.usage}")
