from pydantic import BaseModel

class PdfToMarkdownRequest(BaseModel):
    bucket_name: str
    object_name: str