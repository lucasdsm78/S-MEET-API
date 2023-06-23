from abc import ABC, abstractmethod

from fastapi import UploadFile
from fastapi.responses import FileResponse


class FileUploader(ABC):

    @abstractmethod
    def save_image_file(self, domain: str, image: UploadFile, uuid: str) -> str:
        raise NotImplementedError