import os
import pathlib
import unittest
import multiprocessing
from time import sleep

import requests
from PIL import Image


def backend_process():
    import main


class IntegrationTests(unittest.TestCase):

    @staticmethod
    def _run_backend():
        thread = multiprocessing.Process(target=backend_process)
        thread.start()
        sleep(5)
        return thread

    def test_ping(self):
        th = self._run_backend()

        r = requests.get(url="http://localhost:5000/ping")
        self.assertTrue(r.json()['success'])

        th.terminate()

    def test_file_server(self):
        th = self._run_backend()

        r = requests.get(url="http://localhost:8000/")
        self.assertIsNotNone(r.text)

        th.terminate()

    def test_get_image_size(self):
        th = self._run_backend()
        path = os.path.join(pathlib.Path().resolve(), "test", "test_images", "fox_320_480.jpg")

        payload = {'image': open(path, 'rb')}
        response = requests.post(url="http://localhost:5000/get_size", files=payload)
        r = response.json()
        self.assertEqual(r['w'], 320)
        self.assertEqual(r['h'], 480)
        th.terminate()

    def test_get_not_image_size(self):
        th = self._run_backend()
        path = os.path.join(pathlib.Path().resolve(), "test", "unit_tests", "test_ai_filter.py")

        payload = {'image': open(path, 'rb')}
        response = requests.post(url="http://localhost:5000/get_size", files=payload)
        self.assertEqual(response.status_code, 500)
        th.terminate()

    def test_apply_filter(self):
        th = self._run_backend()

        path = os.path.join(pathlib.Path().resolve(), "test", "test_images", "fox_320_480.jpg")

        payload = {'image': open(path, 'rb')}
        data = {'filter_name': "Candy"}
        response = requests.post(url="http://localhost:5000/", data=data, files=payload)

        self.assertEqual(response.json()['id'], 2)

        th.terminate()

    def test_apply_filter_on_incorrect_file(self):
        th = self._run_backend()

        path = os.path.join(pathlib.Path().resolve(), "test", "unit_tests", "test_ai_filter.py")

        payload = {'image': open(path, 'rb')}
        data = {'filter_name': "Candy"}
        response = requests.post(url="http://localhost:5000/", data=data, files=payload)

        self.assertEqual(response.status_code, 500)

        th.terminate()

    def test_save_unreal_image(self):
        th = self._run_backend()
        data = {'saved_image_id': "2000"}
        response = requests.post(url="http://localhost:5000/save_image", data=data)
        r = response.json()
        self.assertFalse(r['success'])
        th.terminate()

    def test_save_image(self):
        th = self._run_backend()

        path = os.path.join(pathlib.Path().resolve(), "test", "test_images", "fox_320_480.jpg")

        payload = {'image': open(path, 'rb')}
        data = {'filter_name': "Candy"}
        response = requests.post(url="http://localhost:5000/", data=data, files=payload)

        self.assertEqual(response.json()['id'], 2)

        data = {'saved_image_id': "2"}
        response = requests.post(url="http://localhost:5000/save_image", data=data)
        r = response.json()
        self.assertTrue(r['success'])

        th.terminate()

    def test_reset(self):
        th = self._run_backend()

        r = requests.get(url="http://localhost:5000/reset")
        self.assertEqual(r.json()['error'], "NO")

        th.terminate()

    def test_get_last_saved(self):
        th = self._run_backend()

        path = os.path.join(pathlib.Path().resolve(), "test", "test_images", "fox_320_480.jpg")
        payload = {'image': open(path, 'rb')}
        data = {'filter_name': "Candy"}
        requests.post(url="http://localhost:5000/", data=data, files=payload)

        data = {'saved_image_id': "2"}
        requests.post(url="http://localhost:5000/save_image", data=data)

        response = requests.get(url="http://localhost:5000/get_last_saved")

        r = response.json()

        self.assertEqual(r['error'], "NO")
        self.assertEqual(r['id'], "2")

        data = {'filter_name': "Candy"}
        path = os.path.join(pathlib.Path().resolve(), "test", "test_images", "cat_300_100.jpg")
        payload = {'image': open(path, 'rb')}
        requests.post(url="http://localhost:5000/", data=data, files=payload)
        data = {'saved_image_id': "4"}
        requests.post(url="http://localhost:5000/save_image", data=data)

        response = requests.get(url="http://localhost:5000/get_last_saved")

        r = response.json()

        self.assertEqual(r['error'], "NO")
        self.assertEqual(r['id'], "4")

        th.terminate()

    def test_bad_get_last_saved(self):
        th = self._run_backend()

        response = requests.get(url="http://localhost:5000/get_last_saved")
        r = response.json()

        self.assertEqual(r['error'], "YES")

        th.terminate()

    def test_find_file_in_http_server(self):
        th = self._run_backend()

        path = os.path.join(pathlib.Path().resolve(), "test", "test_images", "fox_320_480.jpg")

        payload = {'image': open(path, 'rb')}
        data = {'filter_name': "Candy"}
        response = requests.post(url="http://localhost:5000/", data=data, files=payload)

        self.assertEqual(response.json()['id'], 2)

        r = requests.get(url="http://localhost:8000/")
        self.assertIn("2.jpg", r.text)

        th.terminate()

    def test_reset_applied_filters(self):
        th = self._run_backend()
        path = os.path.join(pathlib.Path().resolve(), "test", "test_images", "fox_320_480.jpg")

        payload = {'image': open(path, 'rb')}
        data = {'filter_name': "Candy"}
        requests.post(url="http://localhost:5000/", data=data, files=payload)

        data = {'saved_image_id': "2"}
        requests.post(url="http://localhost:5000/save_image", data=data)

        response = requests.get(url="http://localhost:5000/get_last_saved")
        r = response.json()
        self.assertEqual(r['error'], "NO")
        self.assertEqual(r['id'], "2")

        payload = {'image': open(path, 'rb')}
        data = {'filter_name': "Candy"}
        requests.post(url="http://localhost:5000/", data=data, files=payload)

        response = requests.get(url="http://localhost:5000/get_last_saved")
        r = response.json()
        self.assertEqual(r['error'], "NO")
        self.assertEqual(r['id'], "2")

        th.terminate()

    def test_images_on_file_server(self):
        th = self._run_backend()

        requests.get(url="http://localhost:5000/reset")

        r = requests.get(url="http://localhost:8000/")
        self.assertNotIn("2.jpg", r.text)

        path = os.path.join(pathlib.Path().resolve(), "test", "test_images", "fox_320_480.jpg")

        payload = {'image': open(path, 'rb')}
        data = {'filter_name': "Candy"}
        requests.post(url="http://localhost:5000/", data=data, files=payload)

        r = requests.get(url="http://localhost:8000/")
        self.assertIn("2.jpg", r.text)

        r = requests.get(url="http://localhost:8000/2.jpg")
        from io import BytesIO

        img = Image.open(BytesIO(r.content))
        self.assertEqual(img.size[0], 320)
        self.assertEqual(img.size[1], 480)

        th.terminate()

    def test_incorrect_requests(self):
        th = self._run_backend()

        path = os.path.join(pathlib.Path().resolve(), "test", "unit_tests", "test_ai_filter.py")
        payload = {'image': open(path, 'rb')}
        requests.post(url="http://localhost:5000/get_size", files=payload)

        path = os.path.join(pathlib.Path().resolve(), "test", "unit_tests", "test_ai_filter.py")
        payload = {'image': open(path, 'rb')}
        data = {'filter_name': "Candy"}
        requests.post(url="http://localhost:5000/", data=data, files=payload)

        path = os.path.join(pathlib.Path().resolve(), "test", "test_images", "fox_320_480.jpg")
        payload = {'image': open(path, 'rb')}
        data = {'filter_name': "NOTAFILTER"}
        requests.post(url="http://localhost:5000/", data=data, files=payload)

        requests.get(url="http://localhost:8000/200000.jpg")

        data = {'saved_image_id': "2000"}
        requests.post(url="http://localhost:5000/save_image", data=data)

        r = requests.get(url="http://localhost:5000/ping")
        self.assertTrue(r.json()['success'])

        th.terminate()

    def test_apply_filter_with_incorrect_name(self):
        th = self._run_backend()

        path = os.path.join(pathlib.Path().resolve(), "test", "test_images", "fox_320_480.jpg")

        payload = {'image': open(path, 'rb')}
        data = {'filter_name': "NOTAFILTER"}
        response = requests.post(url="http://localhost:5000/", data=data, files=payload)

        print(response.status_code)
        self.assertEqual(response.status_code, 500)

        th.terminate()


if __name__ == '__main__':
    unittest.main()
