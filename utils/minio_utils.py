from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv
load_dotenv()
import os

# 创建 MinIO 客户端
client = Minio(
    endpoint = os.environ.get("MINIO_ENDPOINT"),
    access_key = os.environ.get("MINIO_ACCESS_KEY"),
    secret_key = os.environ.get("MINIO_SECRET_KEY"),
    secure = False  # 如果使用 HTTPS 则设为 True
)

# 加载文件为字节流
def load_file_from_minio(bucket_name: str, object_name: str) -> bytes:
    try:
        # 从指定 bucket 中获取文件
        response = client.get_object(bucket_name, object_name)
        # 读取文件内容
        file_data = response.read()
        response.close()
        response.release_conn()
        return file_data
    except S3Error as e:
        print(f"Error occurred: {e}")
        return None

# 上传文件
def upload_file_to_minio(bucket_name: str, file_path: str, object_name: str) -> bool:
    try:
        # 检查存储桶是否存在，如果不存在则创建
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
        # 上传文件
        client.fput_object(bucket_name, object_name, file_path)
        print(f"文件 {file_path} 已成功上传到 {bucket_name}/{object_name}")
        return True
    except S3Error as e:
        print(f"上传文件时出错: {e}")
        return False

if __name__ == '__main__':
    # 示例用法
    bucket_name = "rag-file-transfer"
    object_name = 'invoice.pdf'
    file_path = "C:/Users/yaohua.zhang/OneDrive - Accenture (China)/桌面/expense_0831/滴滴出行行程报销单02.pdf"

    file_data = load_file_from_minio(bucket_name, object_name)
    if file_data:
        print("文件加载成功!")
        # 对文件内容进行处理
    else:
        print("文件加载失败")

    # success = upload_file_to_minio(bucket_name, file_path, 'invoice.pdf')
    # if success:
    #     print("文件上传成功!")
    # else:
    #     print("文件上传失败")

