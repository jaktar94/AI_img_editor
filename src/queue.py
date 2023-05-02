from src.request import Request


class Queue:
    def __init__(self):
        self.__list_open_requests: list[Request] = []
        self.__list_closed_requests: list[Request] = []

    def add_open_request(self, request: Request):
        self.__list_open_requests.append(request)

    def get_open_request(self) -> Request:
        return self.__list_open_requests.pop() if len(self.__list_open_requests) > 0 else None

    def move_open_to_closed(self, request: Request):
        self.__list_closed_requests.append(request)

    def get_closed_requests(self) -> list[Request]:
        return self.__list_closed_requests

    def delete_closed_request(self, request: Request):
        self.__list_closed_requests.remove(request)
