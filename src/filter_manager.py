import threading
from logging import error, info
from time import sleep

from src.ai_filter import AIFilter
from src.classic_filter import ClassicFilter
from src.filter_names_enum import FilterNamesEnum
from src.local_storage import LocalStorage
from src.queue import Queue


class FilterManager:
    def __init__(self, storage: LocalStorage, queue: Queue):
        self.__ai_filter = AIFilter()
        self.__classic_filter = ClassicFilter()
        self.__storage: LocalStorage = storage
        self.__queue: Queue = queue

    def import_filters(self):
        info(msg="Checking images with styles")
        for filter_image in FilterNamesEnum:
            if filter_image.name.lower().startswith("ai_"):
                if self.__storage.get_filter_image(filter_name=filter_image) is None:
                    error(f"Filter {filter_image.value} not found !")
                    raise
                else:
                    info(msg=f"Filter {filter_image.value} found")
        info(msg="Checking images with styles completed")

    def run(self):
        def run():
            while True:
                request = self.__queue.get_open_request()
                if request is None:
                    sleep(2)
                    continue
                info(msg=f"Processing a request {request.input_image_id}")
                image = self.__storage.get_image(image_id=request.input_image_id)
                if request.is_ai_filter:
                    info(msg=f"Applying AI Filter {request.filter_name} to request {request.input_image_id}")
                    result = self.__ai_filter.apply_filter(image=image, filter_name=request.filter_name)
                else:
                    info(msg=f"Applying Classic Filter {request.filter_name} to request {request.input_image_id}")
                    result = self.__classic_filter.apply_filter(image=image, filter_name=request.filter_name)
                result_id = self.__storage.save_image(result)

                request.output_image_id = result_id

                info(msg=f"Output image for request {request.input_image_id} has id {request.output_image_id}")
                info(msg=f"Deleting image with id {request.input_image_id}")
                self.__storage.delete_image(image_id=request.input_image_id)
                info(msg=f"Moving request {request.input_image_id} to closed")
                self.__queue.move_open_to_closed(request=request)

        info(msg="Starting FilterManager thread")
        threading.Thread(target=run).start()
