FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制当前目录内容到容器的 /app 目录
COPY . /app

# 安装依赖项
RUN pip install -r requirements.txt

# 暴露端口（如 Flask 默认为 5000）
EXPOSE 6000

# 运行 Python 应用
CMD ["python", "app.py"]