import unittest
from ai_filters.Style_GAN.utils import *


class AIUtilsTestCase(unittest.TestCase):
    def setUp(self):
        image = Image.open('test/test_images/fox_320_480.jpg').convert("RGB")
        self.image = np.asarray(image)

    def testCommonImageProcessing(self):
        processed_image = tensor_process_rgbimage(self.image)
        self.assertEqual(processed_image.__class__, torch.Tensor)
        self.assertEqual(processed_image.dtype, torch.float)
        self.assertEqual((self.image.shape[2], self.image.shape[0], self.image.shape[1]), processed_image.shape)

    def testCommonBatchProcessing(self):
        image = tensor_process_rgbimage(self.image).unsqueeze(0)
        processed_image = preprocess_batch(image)
        torch.testing.assert_close(image[:, [2, 1, 0]], processed_image)

    def testCommonPostprocessing(self):
        image = tensor_process_rgbimage(self.image)
        devices = ["cpu", "cuda"] if torch.cuda.is_available() else ["cpu"]
        for i, device in enumerate(devices):
            with self.subTest(i=i):
                image = image.to(device)
                processed_image = tensor_postprocess_rgbimage(image, cuda=device == "cuda")
                self.assertEqual(processed_image.__class__, np.ndarray)
                self.assertEqual(processed_image.dtype, np.uint8)
                self.assertEqual((image.shape[1], image.shape[2], image.shape[0]), processed_image.shape)
                self.assertEqual(True, ((processed_image >= 0) & (processed_image <= 255)).all())

    def testPostprocessingWithInvalidDevice(self):
        image = tensor_process_rgbimage(self.image)
        with self.subTest(i=1):
            image = image.to("cpu")
            try:
                tensor_postprocess_rgbimage(image, cuda=True)
                result = True
            except Exception:
                result = False
            self.assertEqual(True, result)

        with self.subTest(i=2):
            if not torch.cuda.is_available():
                self.skipTest("Cuda is not available")
            image = image.to("cuda")
            with self.assertRaises(TypeError):
                tensor_postprocess_rgbimage(image, cuda=False)


if __name__ == '__main__':
    unittest.main()
