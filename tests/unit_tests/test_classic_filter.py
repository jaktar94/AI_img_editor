import os
import pathlib
import unittest

from PIL import Image

from src.classic_filter import ClassicFilter
from src.filter_names_enum import FilterNamesEnum


class ClassicFilterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.image = Image.open(os.path.join(pathlib.Path().resolve(), "test", "test_images", "unnamed.jpg"))
        self.cf = ClassicFilter()

    def test_correct_filter(self):
        processed_image = self.cf.apply_filter(image=self.image, filter_name=FilterNamesEnum.GREYSCALE)
        self.assertIsNotNone(processed_image)
        processed_image = self.cf.apply_filter(image=self.image, filter_name=FilterNamesEnum.BROWN)
        self.assertIsNotNone(processed_image)
        processed_image = self.cf.apply_filter(image=self.image, filter_name=FilterNamesEnum.INVERT)
        self.assertIsNotNone(processed_image)
        processed_image = self.cf.apply_filter(image=self.image, filter_name=FilterNamesEnum.HAND_DRAWN)
        self.assertIsNotNone(processed_image)
        processed_image = self.cf.apply_filter(image=self.image, filter_name=FilterNamesEnum.EMBOSS)
        self.assertIsNotNone(processed_image)

    def test_ai_filter(self):
        processed_image = self.cf.apply_filter(image=self.image, filter_name=FilterNamesEnum.AI_CANDY)
        self.assertIsNone(processed_image)

    def test_not_filter(self):
        processed_image = self.cf.apply_filter(image=self.image, filter_name="no_filter")
        self.assertIsNone(processed_image)


if __name__ == '__main__':
    unittest.main()
