from pydantic import BaseModel
from typing import Optional


class Query(BaseModel):
    query: str
    thread_id : Optional[str]=None