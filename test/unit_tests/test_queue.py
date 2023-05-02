import unittest
from src.queue import Queue


class Request:
    def __init__(self, input_image_id=0):
        self.input_image_id = input_image_id


class MyTestCase(unittest.TestCase):

    def test_add_open_request(self):
        q = Queue()
        r = Request()
        is_failed = False
        try:
            q.add_open_request(request=r)
        except:
            is_failed = True
        self.assertFalse(is_failed)

    def test_get_open_request(self):
        q = Queue()
        r = Request()
        q.add_open_request(request=r)
        self.assertEqual(r, q.get_open_request())

    def test_get_none_request(self):
        q = Queue()
        self.assertIsNone(q.get_open_request())

    def test_get_many_requests(self):
        q = Queue()
        r = Request()
        import threading

        def save_request():
            q.add_open_request(request=r)
            r2 = q.get_open_request()
            self.assertEqual(r, r2)

        lst = []
        for i in range(100):
            my_thread = threading.Thread(target=save_request())
            my_thread.start()
            lst.append(my_thread)
        for i in lst:
            i.join()

    def test_get_many_requests_and_none(self):
        q = Queue()
        r = Request()
        import threading

        def save_request():
            q.add_open_request(request=r)

        lst = []
        for i in range(100):
            my_thread = threading.Thread(target=save_request())
            my_thread.start()
            lst.append(my_thread)
        for i in lst:
            i.join()

        lst_request = []

        def get_request():
            lst_request.append(q.get_open_request())

        lst = []
        for i in range(500):
            my_thread = threading.Thread(target=get_request())
            my_thread.start()
            lst.append(my_thread)
        for i in lst:
            i.join()

        self.assertEqual(len(list(filter(lambda x: not x is None, lst_request))), 100)

    def test_move_to_closed(self):
        r = Request()
        q = Queue()
        self.assertEqual(0, len(q.get_closed_requests()))
        q.add_open_request(r)
        q.get_open_request()
        q.move_open_to_closed(r)
        self.assertEqual(1, len(q.get_closed_requests()))

    def test_get_closed_request(self):
        r = Request()
        q = Queue()
        q.add_open_request(r)
        q.move_open_to_closed(r)
        self.assertEqual(1, len(q.get_closed_requests()))
        q.move_open_to_closed(r)
        self.assertEqual(2, len(q.get_closed_requests()))
        self.assertEqual(q.get_closed_requests(), q.get_closed_requests())

    def test_delete_real_request(self):
        r = Request()
        q = Queue()
        q.add_open_request(r)
        q.move_open_to_closed(r)
        self.assertEqual(1, len(q.get_closed_requests()))
        q.delete_closed_request(r)
        self.assertEqual(0, len(q.get_closed_requests()))

    def test_delete_not_real_request(self):
        r1 = Request(1)
        r2 = Request(2)

        q = Queue()
        q.add_open_request(r1)
        q.move_open_to_closed(r1)
        self.assertEqual(1, len(q.get_closed_requests()))
        is_failed = False
        try:
            q.delete_closed_request(r2)
        except:
            is_failed = True
        self.assertEqual(1, len(q.get_closed_requests()))
        self.assertTrue(is_failed)

    def test_delete_request_twice(self):
        r = Request()
        q = Queue()
        q.add_open_request(r)
        q.move_open_to_closed(r)
        self.assertEqual(1, len(q.get_closed_requests()))
        q.delete_closed_request(r)
        self.assertEqual(0, len(q.get_closed_requests()))
        is_failed = False
        try:
            q.delete_closed_request(r)
        except:
            is_failed = True
        self.assertEqual(0, len(q.get_closed_requests()))
        self.assertTrue(is_failed)


if __name__ == '__main__':
    unittest.main()
