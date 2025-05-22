from storages.backends.s3boto3 import S3Boto3Storage


class RewardStorage(S3Boto3Storage):
    location = "rewards"
    file_overwrite = True
