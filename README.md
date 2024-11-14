# local environment run
uvicorn main:app --reload --port 6001

# 构建镜像
docker build -t kb-rag-markdown .

# 启动服务
docker run -e MINIO_ENDPOINT=xxx -e MINIO_ACCESS_KEY=xxx -e MINIO_SECRET_KEY=xxx -e MINIO_BUCKET_NAME=xxx -e MINIO_BUCKET_NAME_MARKDOWN=xxx -p 6001:6001 kb-rag-markdown