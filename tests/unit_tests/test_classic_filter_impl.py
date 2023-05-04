import os
import pathlib
import unittest

from PIL import Image
import numpy as np

import classic_filters.classic_filter_impl


class ClassicFilterImplementationTest(unittest.TestCase):
    def getSize(self, image: Image) -> float:
        image_height, image_width = image.size
        return image_height * image_width * len(image.getbands())

    def setUp(self) -> None:
        self.image = Image.open(os.path.join(pathlib.Path().resolve(), "test", "test_images", "photo3.jpg"))
        self.verticalImage = Image.open(
            os.path.join(pathlib.Path().resolve(), "test", "test_images", "firefox-ailurus-fulgens-malaya.jpg"))
        self.squareImage = Image.open(
            os.path.join(pathlib.Path().resolve(), "test", "test_images", "unnamed.jpg"))
        self.badImage = Image.open(
            os.path.join(pathlib.Path().resolve(), "test", "test_images", "unnamed_2.jpg"))

    def test_image_size(self):
        image_size = self.getSize(image=self.image)

        new_image = classic_filters.classic_filter_impl.greyscale_filter(self.image)
        new_size = self.getSize(new_image)
        self.assertEqual(first=image_size, second=new_size)

        new_image = classic_filters.classic_filter_impl.brown_filter(self.image)
        new_size = self.getSize(new_image)
        self.assertEqual(first=image_size, second=new_size)

        new_image = classic_filters.classic_filter_impl.invert_filter(self.image)
        new_size = self.getSize(new_image)
        self.assertEqual(first=image_size, second=new_size)

        new_image = classic_filters.classic_filter_impl.hand_drawn_filter(self.image)
        new_size = self.getSize(new_image)
        self.assertEqual(first=image_size, second=new_size)

        new_image = classic_filters.classic_filter_impl.emboss_filter(self.image)
        new_size = self.getSize(new_image)
        self.assertEqual(first=image_size, second=new_size)

    def test_greyscale_channels(self):
        new_image = classic_filters.classic_filter_impl.greyscale_filter(self.image)
        self.assertEqual(first=len(self.image.getbands()), second=len(new_image.getbands()))

    def test_greyscale_results(self):
        channel_count = len(self.image.getbands())
        image_height, image_width = self.image.size

        new_image = classic_filters.classic_filter_impl.greyscale_filter(self.image)
        new_img_array = np.array(new_image.getdata()).reshape(image_width, image_height, channel_count)
        for y in range(image_height):
            for x in range(image_width):
                self.assertEqual(first=new_img_array[x, y, 1], second=new_img_array[x, y, 2])
                self.assertEqual(first=new_img_array[x, y, 0], second=new_img_array[x, y, 1])

    def test_brown_color_consistency(self):
        test_pixel = np.array([[[0, 0, 0]]])
        test_image = Image.fromarray(test_pixel.astype(np.uint8))
        new_image = classic_filters.classic_filter_impl.brown_filter(test_image)
        self.assertEqual(first=list(new_image.getdata()), second=[(52, 27, 16)])

    def test_invert_results(self):
        test_pixel = np.array([[[0, 0, 0]]])
        test_image = Image.fromarray(test_pixel.astype(np.uint8))
        new_image = classic_filters.classic_filter_impl.invert_filter(test_image)
        self.assertEqual(first=list(new_image.getdata()), second=[(255, 255, 255)])

    def test_double_invert_results(self):
        new_image = classic_filters.classic_filter_impl.invert_filter(self.image)
        new_image = classic_filters.classic_filter_impl.invert_filter(new_image)
        self.assertEqual(first=list(new_image.getdata()), second=list(self.image.getdata()))

    def test_convolution_dimensions(self):
        new_image_horizontal = classic_filters.classic_filter_impl.hand_drawn_filter(self.image)
        self.assertIsNotNone(new_image_horizontal)
        new_image_horizontal = classic_filters.classic_filter_impl.emboss_filter(self.image)
        self.assertIsNotNone(new_image_horizontal)

        new_image_vertical = classic_filters.classic_filter_impl.hand_drawn_filter(self.verticalImage)
        self.assertIsNotNone(new_image_vertical)
        new_image_vertical = classic_filters.classic_filter_impl.emboss_filter(self.verticalImage)
        self.assertIsNotNone(new_image_vertical)

        new_image_square = classic_filters.classic_filter_impl.hand_drawn_filter(self.squareImage)
        self.assertIsNotNone(new_image_square)
        new_image_square = classic_filters.classic_filter_impl.emboss_filter(self.squareImage)
        self.assertIsNotNone(new_image_square)

    def test_convolution_error(self):
        self.assertRaises(TypeError, classic_filters.classic_filter_impl.emboss_filter, self.badImage)


if __name__ == '__main__':
    unittest.main()
