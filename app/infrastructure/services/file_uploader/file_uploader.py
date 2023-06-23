import os
import shutil

from fastapi import UploadFile

from app.domain.services.file_uploader.file_uploader import FileUploader
from pydantic import BaseModel

class FileUploaderImpl(FileUploader, BaseModel):

    class Config:
        arbitrary_types_allowed = True

    def save_image_file(self, domain:str, image: UploadFile, uuid: str) -> str:
        save_path = os.path.join(f"images/{domain}/{uuid}", image.filename)

        os.makedirs(f"images/{domain}/{uuid}", exist_ok=True)

        with open(save_path, "wb") as f:
            shutil.copyfileobj(image.file, f)

        return save_path