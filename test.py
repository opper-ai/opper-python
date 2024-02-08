# from opperai import fn
from opperai import Client
from opperai.types import ChatPayload, Message, ContextData


# @fn()
# def translate(text: str, target_language: str) -> str:
#     """Translate text to a target language."""

# print(translate("Hello", "fr"))

client = Client(api_key="op-U009WSBBV5WXECADLHZ5")
# response = client.functions.chat(
#     "example", ChatPayload(messages=[Message(role="user", content="hello")])
# )
# context = {}
# if response.context:
#     for context_data in response.context:
#         if context_data.metadata:
#             file_name = context_data.metadata["file_name"]
#             if file_name not in context:
#                 context[file_name] = []
#             context[file_name].append(context_data.content)

# print(context)

print(client.indexes.create("test126"))
