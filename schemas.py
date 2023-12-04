from pydantic import BaseModel


class DocumentCreate(BaseModel):
    path: str
    date: str

class DocumentText(BaseModel):
    id: int
    id_doc: int
    text: str