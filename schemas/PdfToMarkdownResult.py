from pydantic import BaseModel

class PdfToMarkdownResult(BaseModel):
    md_bucket_name: str
    md_object_name: str
    md_content: str