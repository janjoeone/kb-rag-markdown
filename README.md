# run
uvicorn main:app --reload --port 6170

# 构建镜像
docker build -t kb-rag-markdown .

# 启动服务
docker run --env-file .env.development -p 6000:6000 kb-rag-markdown