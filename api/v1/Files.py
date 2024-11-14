from fastapi import APIRouter

import os
from loguru import logger
from magic_pdf.pipe.UNIPipe import UNIPipe
from magic_pdf.rw.DiskReaderWriter import DiskReaderWriter
from utils.minio_utils import load_file_from_minio, upload_file_to_minio
from dotenv import load_dotenv
from schemas.PdfToMarkdownResult import PdfToMarkdownResult
from schemas.PdfToMarkdownRequest import PdfToMarkdownRequest
from datetime import datetime
import fnmatch


load_dotenv()
fileRouter = APIRouter(
    prefix="/files",
    tags=["文件处理"],
)

@fileRouter.post("/pdf_to_markdown", response_model = PdfToMarkdownResult)
async def pdf_to_markdown(request : PdfToMarkdownRequest) -> PdfToMarkdownResult:
    try:
        # 获取当前脚本相对路径
        current_script_dir = os.path.dirname(os.path.abspath(__file__))

        md_name = int(datetime.now().timestamp() * 1000)
        md_object_name = f'{md_name}.md'

        # 从MinIO下载加载原文件
        pdf_bytes = load_file_from_minio(
            bucket_name = request.bucket_name,
            object_name = request.object_name
        )

        # PDF -> Markdown
        jso_useful_key = {"_pdf_type": "", "model_list": []}
        local_image_dir = os.path.join(current_script_dir, 'images')
        image_dir = str(os.path.basename(local_image_dir))
        image_writer = DiskReaderWriter(local_image_dir)
        pipe = UNIPipe(pdf_bytes, jso_useful_key, image_writer)
        pipe.pipe_classify()
        pipe.pipe_analyze()
        pipe.pipe_parse()
        md_content = pipe.pipe_mk_markdown(image_dir, drop_mode="none")
        with open(md_object_name, "w", encoding="utf-8") as f:
            f.write(md_content)

        # 上传Markdown文件至MinIO
        upload_result = upload_file_to_minio(
            # 本地文件路径
            file_path = md_object_name,
            bucket_name = os.environ.get("MINIO_BUCKET_NAME_MARKDOWN"),
            object_name = md_object_name
        )
        if upload_result:
            # 删除本地文件
            if os.path.exists(md_object_name):
                # 删除文件
                os.remove(md_object_name)

        # 遍历上传图片至MinIO
        traverse_upload_images_in_directory(local_image_dir)

        return PdfToMarkdownResult(
            md_bucket_name = os.environ.get("MINIO_BUCKET_NAME_MARKDOWN"),
            md_object_name = md_object_name,
            md_content = md_content
        )
    except Exception as e:
        logger.exception(e)

def traverse_upload_images_in_directory(directory):
    print(directory)
    # 定义常见图片格式的扩展名
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.tiff']
    # 遍历目录及其子目录
    for root, dirs, files in os.walk(directory):
        for extension in image_extensions:
            for filename in fnmatch.filter(files, extension):
                # 获取图片文件的完整路径
                file_path = os.path.join(root, filename)
                print(file_path)
                suffix = os.path.splitext(file_path)[1]
                timestamp_milliseconds = int(datetime.now().timestamp() * 1000)
                object_name = f'{timestamp_milliseconds}.{suffix}'
                upload_result = upload_file_to_minio(
                    # 本地文件路径
                    file_path = file_path,
                    bucket_name = os.environ.get("MINIO_BUCKET_NAME_MARKDOWN"),
                    object_name = object_name
                )
                if upload_result:
                    # 删除本地文件
                    if os.path.exists(file_path):
                        # 删除文件
                        os.remove(file_path)

if __name__ == '__main__':
    # pdf_to_markdown(bucket_name='rag-file-transfer', object_name='invoice.pdf')
    traverse_upload_images_in_directory('images')
