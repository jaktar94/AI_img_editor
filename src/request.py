from logging import error

from src.filter_names_enum import FilterNamesEnum


class Request:
    def __init__(self, input_image_id: int, filter_name: str):
        self.__input_image_id: int = input_image_id
        self.__output_image_id: int = None
        self.__filter_name: FilterNamesEnum = None
        for filter_name_enum in FilterNamesEnum:
            if filter_name_enum.value == filter_name:
                self.__filter_name = filter_name_enum
        if self.__filter_name is None:
            error(msg=f"Filter {filter_name} not found !")
        self.__is_ai_filter: bool = self.__filter_name.name.lower().startswith("ai_")

    @property
    def input_image_id(self):
        return self.__input_image_id

    @property
    def output_image_id(self):
        return self.__output_image_id

    @output_image_id.setter
    def output_image_id(self, image_id: int):
        self.__output_image_id = image_id

    @property
    def filter_name(self):
        return self.__filter_name

    @property
    def is_ai_filter(self):
        return self.__is_ai_filter
