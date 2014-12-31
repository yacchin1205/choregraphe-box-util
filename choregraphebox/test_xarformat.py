import unittest
import xarformat
import os


class TestXARformat(unittest.TestCase):
    def setUp(self):
        self.resources = os.path.join(os.path.dirname(__file__),
                                      "test-resources")

    def test_load(self):
        boxlib = xarformat.load(os.path.join(self.resources, "boxlib1"))
        items = sorted(boxlib.get_children(), key=lambda item: item.name)
        self.assertEquals(len(items), 3)
        self.assertEquals(items[0].name, "TestFolder1")
        self.assertIsNone(items[0].get_box())
        self.assertEquals(items[1].name, "TestFolder2")
        self.assertIsNone(items[1].get_box())
        self.assertEquals(items[2].name, "TestPythonA")
        self.assertIsNotNone(items[2].get_box())

        children1 = sorted(items[0].get_children(), key=lambda item: item.name)
        self.assertEquals(len(children1), 3)
        self.assertEquals(children1[0].name, "TestFolder1-1")
        self.assertIsNone(children1[0].get_box())
        self.assertEquals(children1[1].name, "TestFolder1-2")
        self.assertIsNone(children1[1].get_box())
        self.assertEquals(children1[2].name, "TestTimeline1A")
        self.assertIsNotNone(children1[2].get_box())

        children2 = sorted(children1[0].get_children(),
                           key=lambda item: item.name)
        self.assertEquals(len(children2), 1)
        self.assertEquals(children2[0].name, "TestPython1-1A")
        self.assertIsNotNone(children2[0].get_box())

        children2 = sorted(children1[1].get_children(),
                           key=lambda item: item.name)
        self.assertEquals(len(children2), 2)
        self.assertEquals(children2[0].name, "TestPython1-2A")
        self.assertIsNotNone(children2[0].get_box())
        self.assertEquals(children2[1].name, "TestTimeline1-2B")
        self.assertIsNotNone(children2[1].get_box())

        children1 = sorted(items[1].get_children(), key=lambda item: item.name)
        self.assertEquals(len(children1), 2)
        self.assertEquals(children1[0].name, "TestDiagram2A")
        self.assertIsNotNone(children1[0].get_box())
        self.assertEquals(children1[1].name, "TestDialog2B")
        self.assertIsNotNone(children1[1].get_box())

        self.assertEquals(len(items[2].get_children()), 0)


if __name__ == '__main__':
    unittest.main()
