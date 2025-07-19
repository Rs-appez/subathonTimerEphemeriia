from uuid import uuid4


def rename_file_to_upload(instance, filename):
    """
    Rename file name with UUID
    """
    ext = filename.split(".")[-1]
    new_filename = f"{uuid4()}.{ext}"
    return new_filename
