import os
import pathlib
import unittest

from PIL import Image

from src.filter_names_enum import FilterNamesEnum
from src.local_storage import LocalStorage


class LocalStorageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp_folder_path = os.path.normpath(os.path.join(pathlib.Path().resolve(), "tmp"))
        self.filters_folder_path = os.path.normpath(
            os.path.join(pathlib.Path().resolve(), "ai_filters", "Style_GAN", "images"))

        self.image1 = Image.open(
            os.path.join(pathlib.Path().resolve(), "test", "test_images", "skull_100_100.jpg"))
        self.image2 = Image.open(
            os.path.join(pathlib.Path().resolve(), "test", "test_images", "lake_800_450.jpg"))
        self.notimage = open(file=os.path.join(pathlib.Path().resolve(), "main.py"), mode="rb")

    def test_save_image(self):
        ls = LocalStorage(tmp_folder_path=self.tmp_folder_path, filters_folder_path=self.filters_folder_path)
        ls.delete_images()
        before = 0
        for _ in os.listdir(path=self.tmp_folder_path):
            before += 1

        ls.save_image(image=self.image1)

        after = 0

        for _ in os.listdir(path=self.tmp_folder_path):
            after += 1

        self.assertEqual(first=before + 1, second=after)

    def test_correct_id_name(self):

        ls = LocalStorage(tmp_folder_path=self.tmp_folder_path, filters_folder_path=self.filters_folder_path)

        id1 = ls.save_image(self.image1)
        id2 = ls.save_image(self.image2)
        self.assertEqual(first=id2, second=id1 + 1)

    def test_get_image(self):

        ls = LocalStorage(tmp_folder_path=self.tmp_folder_path, filters_folder_path=self.filters_folder_path)

        id = ls.save_image(self.image1)
        img = ls.get_image(image_id=id)

        self.assertEqual(first=img.size, second=self.image1.size)

    def test_save_not_image(self):
        ls = LocalStorage(tmp_folder_path=self.tmp_folder_path, filters_folder_path=self.filters_folder_path)

        is_failed = False
        try:
            ls.save_image(image=self.notimage)
        except:
            is_failed = True
        self.assertTrue(is_failed)

    def test_get_image_path(self):
        ls = LocalStorage(tmp_folder_path=self.tmp_folder_path, filters_folder_path=self.filters_folder_path)
        img_id = ls.save_image(image=self.image1)

        img_path = ls.get_image_path(image_id=img_id)

        self.assertEqual(img_path,
                         os.path.normpath(os.path.join(pathlib.Path().resolve(), "tmp", str(img_id) + ".jpg")))

        img = Image.open(img_path)

        self.assertEqual(img.size, self.image1.size)

    def test_delete_real_image(self):
        ls = LocalStorage(tmp_folder_path=self.tmp_folder_path, filters_folder_path=self.filters_folder_path)

        for root, dirs, files in os.walk(self.tmp_folder_path):
            for f in files:
                os.remove(os.path.join(root, f))

        is_failed = False
        try:
            ls.get_image(image_id=1)
        except:
            is_failed = True

        self.assertTrue(is_failed)

        img_id = ls.save_image(image=self.image1)

        ls.get_image(image_id=img_id)

        ls.delete_image(image_id=img_id)

        is_failed = False
        try:
            ls.get_image(image_id=img_id)
        except:
            is_failed = True
        self.assertTrue(is_failed)

    def test_delete_not_real_image(self):
        ls = LocalStorage(tmp_folder_path=self.tmp_folder_path, filters_folder_path=self.filters_folder_path)

        for root, dirs, files in os.walk(self.tmp_folder_path):
            for f in files:
                os.remove(os.path.join(root, f))

        is_failed = False
        try:
            ls.delete_image(image_id=1)
        except:
            is_failed = True
        self.assertTrue(is_failed)

    def test_delete_image_twice(self):
        ls = LocalStorage(tmp_folder_path=self.tmp_folder_path, filters_folder_path=self.filters_folder_path)

        for root, dirs, files in os.walk(self.tmp_folder_path):
            for f in files:
                os.remove(os.path.join(root, f))

        id = ls.save_image(self.image1)

        ls.delete_image(image_id=id)
        is_failed = False
        try:
            ls.delete_image(image_id=id)
        except:
            is_failed = True
        self.assertTrue(is_failed)

    def test_get_not_image(self):
        with open(os.path.normpath(os.path.join(self.tmp_folder_path, "file.jpg")), "w") as f:
            f.write("1111111111111111")
        is_failed = False
        try:
            ls = LocalStorage(tmp_folder_path=self.tmp_folder_path, filters_folder_path=self.filters_folder_path)
            ls.get_image(image_id="file")
        except:
            is_failed = True

        self.assertTrue(is_failed)

    def test_many_images(self):
        import threading
        ls = LocalStorage(tmp_folder_path=self.tmp_folder_path, filters_folder_path=self.filters_folder_path)

        def save_image():
            id = ls.save_image(image=self.image1)
            ls.get_image(image_id=id)

        lst = []
        for i in range(100):
            my_thread = threading.Thread(target=save_image())
            my_thread.start()
            lst.append(my_thread)
        for i in lst:
            i.join()

        ls.delete_images()

    def test_delete_images(self):
        ls = LocalStorage(tmp_folder_path=self.tmp_folder_path, filters_folder_path=self.filters_folder_path)
        ls.save_image(image=self.image1)
        import pathlib
        initial_count = 0
        for path in pathlib.Path(self.tmp_folder_path).iterdir():
            if path.is_file():
                initial_count += 1
        self.assertEqual(1, initial_count)

        ls.delete_images()
        initial_count = 0
        for path in pathlib.Path(self.tmp_folder_path).iterdir():
            if path.is_file():
                initial_count += 1
        self.assertEqual(0, initial_count)

    def test_filter_image(self):
        ls = LocalStorage(tmp_folder_path=self.tmp_folder_path, filters_folder_path=self.filters_folder_path)
        img = ls.get_filter_image(filter_name=FilterNamesEnum.AI_STARRY_NIGHT)
        self.assertEqual(type(img), type(self.image1))

    def test_classic_filter_image(self):
        ls = LocalStorage(tmp_folder_path=self.tmp_folder_path, filters_folder_path=self.filters_folder_path)
        is_failed = False
        try:
            ls.get_filter_image(filter_name=FilterNamesEnum.GREYSCALE)
        except:
            is_failed = True
        self.assertTrue(is_failed)

    def tearDown(self) -> None:
        ls = LocalStorage(tmp_folder_path=self.tmp_folder_path, filters_folder_path=self.filters_folder_path)
        ls.delete_images()
        self.notimage.close()


if __name__ == '__main__':
    unittest.main()
