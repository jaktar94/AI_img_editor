import unittest
import cv2
from PIL import Image
from src.ai_filter import AIFilter
from src.filter_names_enum import FilterNamesEnum


class AIFilterTestCase(unittest.TestCase):
    def setUp(self):
        self.aiFilter = AIFilter()

    def testCommonOutput(self):
        image = Image.open('test/test_images/fox_320_480.jpg').convert('RGB')
        filter_name = FilterNamesEnum.AI_FEATHERS
        output = self.aiFilter.apply_filter(image, filter_name)
        self.assertEqual(output.__class__, image.__class__)
        self.assertEqual(output.size, image.size)

    def testSingleChannelImage(self):
        image = Image.open('test/test_images/fox_320_480.jpg').convert('L')
        filter_name = FilterNamesEnum.AI_FEATHERS
        with self.assertRaises(ValueError):
            _ = self.aiFilter.apply_filter(image, filter_name)

    def testInvalidFilterName(self):
        image = Image.open('test/test_images/fox_320_480.jpg').convert('RGB')
        filter_name = FilterNamesEnum.BROWN
        with self.assertRaises(cv2.error):
            _ = self.aiFilter.apply_filter(image, filter_name)
