import os
import uuid


def save_file(file, folder):

    upload_dir = f"uploads/{folder}"

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    extension = file.filename.split(".")[-1]

    filename = f"{uuid.uuid4()}.{extension}"

    filepath = os.path.join(
        upload_dir,
        filename
    )

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return filepath