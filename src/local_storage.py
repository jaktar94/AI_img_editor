import os
from PIL import Image

from src.filter_names_enum import FilterNamesEnum


class LocalStorage:
    def __init__(self, tmp_folder_path: str, filters_folder_path: str):
        self.__tmp_folder_path = tmp_folder_path
        self.__filters_folder_path = filters_folder_path
        self.__last_image_id = 0

    def save_image(self, image: Image) -> int:
        self.__last_image_id += 1
        image.save(os.path.join(self.__tmp_folder_path, str(self.__last_image_id) + ".jpg"))
        return self.__last_image_id

    def get_image(self, image_id: int) -> Image:
        return Image.open(os.path.join(self.__tmp_folder_path, str(image_id) + ".jpg")).convert('RGB')

    def get_image_path(self, image_id: int) -> str:
        return os.path.join(self.__tmp_folder_path, str(image_id) + ".jpg")

    def delete_image(self, image_id: int):
        os.remove(os.path.join(self.__tmp_folder_path, str(image_id) + ".jpg"))

    def delete_images(self):
        for root, dirs, files in os.walk(self.__tmp_folder_path):
            for f in files:
                os.remove(os.path.join(root, f))
        self.__last_image_id = 0

    def get_filter_image(self, filter_name: FilterNamesEnum):
        return Image.open(os.path.join(self.__filters_folder_path, filter_name.value.lower() + ".jpg"))