import uvicorn
from fastapi import FastAPI
from api.v1 import Files
app = FastAPI()

@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to RAG Markdown API"}

# 添加路由
app.include_router(Files.fileRouter)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=6001)