FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制当前目录内容到容器的 /app 目录
COPY . /app

# 安装依赖项
RUN pip install -r requirements.txt

# 环境变量
ENV MINIO_ENDPOINT="None"
ENV MINIO_ACCESS_KEY="None"
ENV MINIO_SECRET_KEY="None"
ENV MINIO_BUCKET_NAME="None"
ENV MINIO_BUCKET_NAME_MARKDOWN="None"

# 暴露端口（如 Flask 默认为 5000）
EXPOSE 6000

# 运行 Python 应用
CMD ["python", "app.py"]