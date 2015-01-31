import unittest
import boxlib
import os


class TestBoxLib(unittest.TestCase):
    def setUp(self):
        self.resources = os.path.join(os.path.dirname(__file__),
                                      "test-resources")

    def test_load(self):
        lib = boxlib.load(os.path.join(self.resources, "boxlib1"))
        self.assertEquals(lib.find_by_path("/TestFolder1/TestFolder1-1/"
                          "TestPython1-1A").name, "TestPython1-1A")
        self.assertEquals(lib.find_by_path("/TestFolder1/TestFolder1-2/"
                          "TestPython1-2A").name, "TestPython1-2A")
        self.assertEquals(lib.find_by_path("/TestFolder1/TestFolder1-2/"
                          "TestTimeline1-2B").name, "TestTimeline1-2B")
        self.assertEquals(lib.find_by_path("/TestFolder1/TestTimeline1A")
                          .name, "TestTimeline1A")
        self.assertEquals(lib.find_by_path("/TestFolder2/TestDiagram2A")
                          .name, "TestDiagram2A")
        self.assertEquals(lib.find_by_path("/TestFolder2/TestDialog2B")
                          .name, "TestDialog2B")
        self.assertEquals(lib.find_by_path("/TestPythonA").name,
                          "TestPythonA")
        self.assertRaises(boxlib.NotFoundError, lambda:
                          lib.find_by_path("/TestFolder1/TestFolder1-1"))
        self.assertRaises(boxlib.NotFoundError, lambda:
                          lib.find_by_path("/TestFolder1/TestFolder1-2"))
        self.assertRaises(boxlib.NotFoundError, lambda:
                          lib.find_by_path("/TestFolder2"))
        self.assertRaises(boxlib.NotFoundError, lambda:
                          lib.find_by_path("/TestPythonB"))
        self.assertRaises(boxlib.NotFoundError, lambda:
                          lib.find_by_path("/TestFolder1/TestFolder1-1/"
                                           "TestPython1-1B"))

    def test_verify(self):
        lib = boxlib.load(os.path.join(self.resources, "boxlib1"))
        warn_paths = []
        for warn in lib.verify_tags():
            self.assertTrue('@source' in warn.message)
            warn_paths.append(warn.path)
        self.assertTrue("/TestFolder1/TestFolder1-1/"
                        "TestPython1-1A" in warn_paths)
        self.assertFalse("/TestFolder1/TestFolder1-1/"
                         "TestPython1-2A" in warn_paths)
        self.assertTrue("/TestFolder1/TestFolder1-2/"
                        "TestTimeline1-2B" in warn_paths)
        self.assertTrue("/TestFolder1/TestTimeline1A" in warn_paths)
        self.assertTrue("/TestFolder2/TestDiagram2A" in warn_paths)
        self.assertTrue("/TestFolder2/TestDialog2B" in warn_paths)
        self.assertTrue("/TestPythonA" in warn_paths)


if __name__ == '__main__':
    unittest.main()
