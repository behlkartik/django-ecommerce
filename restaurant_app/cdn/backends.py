from storages.backends.s3boto3 import S3Boto3Storage
import os

class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = 'static'
    custom_domain = os.getenv("CLOUDFRONT_DOMAIN") #cdn

class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = 'media'
    custom_domain = os.getenv("CLOUDFRONT_DOMAIN")