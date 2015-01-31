import unittest
import boxlib
import xarformat
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

        lib = boxlib.load(os.path.join(self.resources, "boxlib2"))
        warn_paths = []
        for warn in lib.verify_tags():
            self.assertTrue('@source' in warn.message)
            warn_paths.append(warn.path)
        self.assertTrue("/Test1" in warn_paths)
        self.assertFalse("/Test2" in warn_paths)

    def test_find_by_box(self):
        lib = boxlib.load(os.path.join(self.resources, "boxlib2"))
        behavior = xarformat.load(os.path.join(self.resources, "project1",
                                               "behavior_1", "behavior.xar"))
        targets = [box for box in behavior.get_box().get_all_boxes()
                   if box.name == "Test1"]
        self.assertEquals(len(targets), 1)
        basebox = lib.find_by_box(targets[0], strict=False)
        self.assertEquals(basebox.name, "Test1")
        # "Strict" search must be failure
        # because Test1 box has no "@source" tags in the tooltip
        self.assertRaises(boxlib.NotFoundError, lambda:
                          lib.find_by_box(targets[0]))

        targets = [box for box in behavior.get_box().get_all_boxes()
                   if box.name == "Test2"]
        self.assertEquals(len(targets), 1)
        basebox = lib.find_by_box(targets[0], strict=False)
        self.assertEquals(basebox.name, "Test2")
        basebox = lib.find_by_box(targets[0])
        self.assertEquals(basebox.name, "Test2")


if __name__ == '__main__':
    unittest.main()
