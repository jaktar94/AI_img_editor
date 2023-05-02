import unittest

from src.filter_names_enum import FilterNamesEnum
from src.request import Request


class RequestTest(unittest.TestCase):
    def setUp(self) -> None:
        self.id1 = 1
        self.id2 = 2

    def testRequestParams(self):
        r = Request(input_image_id=self.id1, filter_name=FilterNamesEnum.GREYSCALE.value)

        self.assertEqual(first=self.id1, second=r.input_image_id, msg="Expected equal IDs")

        self.assertIsNone(obj=r.output_image_id, msg="Expected None output id")

        self.assertEqual(first=r.filter_name, second=FilterNamesEnum.GREYSCALE, msg="Expected GREYSCALE filter")

        r.output_image_id = self.id2
        self.assertEqual(first=r.output_image_id, second=self.id2, msg="Expected equal IDs")

    def testRequestAIChecker(self):
        r = Request(input_image_id=self.id1, filter_name=FilterNamesEnum.GREYSCALE.value)

        self.assertFalse(expr=r.is_ai_filter)

        r2 = Request(input_image_id=self.id1, filter_name=FilterNamesEnum.AI_CANDY.value)

        self.assertTrue(expr=r2.is_ai_filter)

    def testRequestFilterNames(self):
        r = Request(input_image_id=self.id1, filter_name=FilterNamesEnum.GREYSCALE.value)
        self.assertEqual(first=r.filter_name, second=FilterNamesEnum.GREYSCALE, msg="Expected GREYSCALE filter")

        self.assertFalse(expr=r.is_ai_filter)

        is_failed = False
        try:
            Request(input_image_id=self.id1, filter_name="NOTAFILTER")
        except:
            is_failed = True

        self.assertTrue(expr=is_failed)


if __name__ == '__main__':
    unittest.main()
