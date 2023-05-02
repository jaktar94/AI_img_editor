import unittest

from src.filter_manager import FilterManager


class FakeStorageGood:
    def get_filter_image(self, filter_name):
        return True


class FakeStorageBad:
    def get_filter_image(self, filter_name):
        return None


class FilterManagerTest(unittest.TestCase):
    def test_import_filters_good(self):
        is_failed = False
        try:
            fm = FilterManager(queue=None, storage=FakeStorageGood())
            fm.import_filters()
        except:
            is_failed = True
        self.assertFalse(is_failed)

    def test_import_filters_bad(self):
        is_failed = False
        try:
            fm = FilterManager(queue=None, storage=FakeStorageBad())
            fm.import_filters()
        except:
            is_failed = True
        self.assertTrue(is_failed)


if __name__ == '__main__':
    unittest.main()
