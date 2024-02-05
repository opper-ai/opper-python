from pydantic import BaseModel


class IndexRetrieveResponse(BaseModel):
    content: str
    metadata: dict
