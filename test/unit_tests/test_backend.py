import os
import pathlib
import unittest

from src.backend import Backend
from src.local_storage import LocalStorage


class FakeFlaskRequest():
    def __init__(self, img, val):
        self.files = {'image': img}
        self.values = {'saved_image_id': val}


class FakeStorage(LocalStorage):
    def __init__(self):
        pass

    def get_image(self, img_id):
        return True

    def delete_images(self):
        return True

    def delete_image(self, image_id):
        pass


class TestBackend(unittest.TestCase):
    def test_image_size(self):
        backend = Backend(queue=None, storage=None)

        x, y = backend.get_image_size(flask_request_local=FakeFlaskRequest(
            os.path.join(pathlib.Path().resolve(), "test", "test_images", "skull_100_100.jpg"), val=None))

        self.assertEqual(x, 100)
        self.assertEqual(y, 100)

    def test_not_image_size(self):
        backend = Backend(queue=None, storage=None)
        is_failed = False
        try:
            fr = FakeFlaskRequest(os.path.join(pathlib.Path().resolve(), "main.py"), val=None)
            x, y = backend.get_image_size(flask_request_local=fr)
        except:
            is_failed = True
        self.assertTrue(is_failed)

    def test_save_image(self):
        backend = Backend(queue=None, storage=FakeStorage())
        fr = FakeFlaskRequest(img=None, val=1)
        res = backend.save_image(flask_request_local=fr)
        self.assertTrue(res)

    def test_get_last_saved_image(self):
        backend = Backend(queue=None, storage=FakeStorage())
        fr = FakeFlaskRequest(img=None, val=1)
        res = backend.save_image(flask_request_local=fr)
        self.assertTrue(res)

        self.assertEqual(backend.get_last_saved_image(), 1)

    def test_reset(self):
        backend = Backend(queue=None, storage=FakeStorage())
        self.assertTrue(backend.reset())

    def test_delete_image(self):
        backend = Backend(queue=None, storage=FakeStorage())

        is_failed = False
        try:
            backend.delete_image(image_id=1)
        except:
            is_failed = True
        self.assertFalse(is_failed)


if __name__ == '__main__':
    unittest.main()
