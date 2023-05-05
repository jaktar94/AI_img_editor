import unittest
import cv2
import numpy as np
from ai_filters.Style_GAN.inference_stylegan import run
from src.filter_names_enum import FilterNamesEnum


class InferenceStyleganTestCase(unittest.TestCase):
    def setUp(self):
        self.image = cv2.imread('tests/test_images/fox_320_480.jpg', cv2.IMREAD_UNCHANGED)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    def testCommonOutput(self):
        filter_name = FilterNamesEnum.AI_FEATHERS.value.lower()
        result_image = run(self.image, style=filter_name)
        self.assertEqual(result_image.shape, self.image.shape)
        self.assertEqual(True, (result_image != np.nan).all() & (result_image != None).all())

    def testInvalidFilterName(self):
        filter_name = FilterNamesEnum.BROWN
        with self.assertRaises(cv2.error):
            output = run(self.image, style=filter_name)
