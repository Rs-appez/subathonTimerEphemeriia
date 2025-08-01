from storages.backends.s3boto3 import S3Boto3Storage


class RewardStorage(S3Boto3Storage):
    location = "rewards"
    file_overwrite = False


class BackgroundStorage(S3Boto3Storage):
    location = "backgrounds"
    file_overwrite = False


class GoalStorage(S3Boto3Storage):
    location = "goals"
    file_overwrite = False
