import os

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = "https://s3.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_LOCATION = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

DEFAULT_FILE_STORAGE = "restaurant_app.cdn.backends.MediaRootS3Boto3Storage"
STATICFILES_STORAGE = "restaurant_app.cdn.backends.StaticRootS3Boto3Storage"
