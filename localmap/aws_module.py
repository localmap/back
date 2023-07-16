import boto3
import mimetypes

AWS_ACCESS_KEY_ID = 'AKIATQLW6UN72MQCLJUY'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'localmap'
AWS_S3_REGION_NAME = 'ap-northeast-2'

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# S3 클라이언트 객체 생성
s3 = boto3.client(
    "s3",
    region_name="ap-northeast-2",
    aws_access_key_id="AKIATQLW6UN72MQCLJUY",
    aws_secret_access_key="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",
)


def upload_to_s3(file_obj, file_name):
    object_key = f"images/{file_name}"

    # 이미지 파일의 MIME 유형 찾기
    content_type, _ = mimetypes.guess_type(file_name)

    # S3에 이미지 업로드
    s3.upload_fileobj(
        file_obj,
        "localmap",
        object_key,
        ExtraArgs={
            "ACL": "public-read",
            "ContentDisposition": "inline",
            "ContentType": content_type,
        },
    )

    # 사진 URL 생성
    url = f"https://localmap.s3.ap-northeast-2.amazonaws.com/{object_key}"
    return url