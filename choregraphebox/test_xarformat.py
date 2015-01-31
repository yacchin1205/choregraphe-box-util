import unittest
import xarformat
import os
import StringIO


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
        self.assertEquals(children1[2].get_box().tooltip, "")

        children2 = sorted(children1[0].get_children(),
                           key=lambda item: item.name)
        self.assertEquals(len(children2), 1)
        self.assertEquals(children2[0].name, "TestPython1-1A")
        self.assertIsNotNone(children2[0].get_box())
        self.assertEquals(children2[0].get_box().tooltip, "Description1-1A")

        children2 = sorted(children1[1].get_children(),
                           key=lambda item: item.name)
        self.assertEquals(len(children2), 2)
        self.assertEquals(children2[0].name, "TestPython1-2A")
        self.assertIsNotNone(children2[0].get_box())
        self.assertEquals(children2[0].get_box().tooltip, "Description1-2A\n\n"
                          "@source https://github.com/yacchin1205/"
                          "choregraphe-box-util")
        self.assertEquals(children2[1].name, "TestTimeline1-2B")
        self.assertIsNotNone(children2[1].get_box())
        self.assertEquals(children2[1].get_box().tooltip, "")

        children1 = sorted(items[1].get_children(), key=lambda item: item.name)
        self.assertEquals(len(children1), 2)
        self.assertEquals(children1[0].name, "TestDiagram2A")
        self.assertIsNotNone(children1[0].get_box())
        self.assertEquals(children1[0].get_box().tooltip, "")
        self.assertEquals(children1[1].name, "TestDialog2B")
        self.assertIsNotNone(children1[1].get_box())
        self.assertEquals(children1[1].get_box().tooltip, "")

        self.assertEquals(len(items[2].get_children()), 0)

    def test_load_box(self):
        boxlib = xarformat.load(os.path.join(self.resources, "boxlib2"))
        items = sorted(boxlib.get_children(), key=lambda item: item.name)
        self.assertEquals(len(items), 2)
        self.assertEquals(items[0].name, "Test1")
        box = items[0].get_box()
        self.assertEquals(box.name, "Test1")
        ports = box.get_inputs()
        self.assertEquals(len(ports), 5)
        self.assertEquals(ports[0].name, "onLoad")
        self.assertEquals(ports[1].name, "onStart")
        self.assertEquals(ports[2].name, "onStop")
        self.assertEquals(ports[3].name, "input1")
        self.assertEquals(ports[4].name, "input2")
        ports = box.get_outputs()
        self.assertEquals(len(ports), 3)
        self.assertEquals(ports[0].name, "onStopped")
        self.assertEquals(ports[1].name, "output1")
        self.assertEquals(ports[2].name, "output2")
        params = box.get_parameters()
        self.assertEquals(len(params), 3)
        self.assertEquals(params[0].name, "param1")
        self.assertEquals(params[1].name, "param2")
        self.assertEquals(params[2].name, "param3")

        self.assertEquals(items[1].name, "Test2")
        box = items[1].get_box()
        self.assertEquals(box.name, "Test2")
        ports = box.get_inputs()
        self.assertEquals(len(ports), 5)
        self.assertEquals(ports[0].name, "onLoad")
        self.assertEquals(ports[1].name, "onStart")
        self.assertEquals(ports[2].name, "onStop")
        self.assertEquals(ports[3].name, "input1")
        self.assertEquals(ports[4].name, "input2")
        ports = box.get_outputs()
        self.assertEquals(len(ports), 3)
        self.assertEquals(ports[0].name, "onStopped")
        self.assertEquals(ports[1].name, "output1")
        self.assertEquals(ports[2].name, "output2")
        params = box.get_parameters()
        self.assertEquals(len(params), 3)
        self.assertEquals(params[0].name, "param1")
        self.assertEquals(params[1].name, "param2")
        self.assertEquals(params[2].name, "param3")

    def test_copy_box(self):
        boxlib = xarformat.load(os.path.join(self.resources, "boxlib2"))
        items = sorted(boxlib.get_children(), key=lambda item: item.name)
        basebox = items[1].get_box()
        self.assertEquals(basebox.name, "Test2")
        behavior = xarformat.load(os.path.join(self.resources, "project1",
                                               "behavior_1", "behavior.xar"))
        target = [box for box in behavior.get_box().get_all_boxes()
                  if box.name == "Test2"][0]
        params = target.get_parameters()
        self.assertEquals(params[0].value, "1")
        self.assertEquals(params[1].value, "1")
        self.assertEquals(params[2].value, "")

        target.copy_from(basebox)
        updatexml = StringIO.StringIO()
        behavior.xarxml.write(updatexml, encoding="utf-8",
                              xml_declaration=True, method="xml")
        behavior = xarformat.load(StringIO.StringIO(updatexml.getvalue()))
        target = [box for box in behavior.get_box().get_all_boxes()
                  if box.name == "Test2"][0]
        params = target.get_parameters()
        self.assertEquals(params[0].value, "1")
        self.assertEquals(params[1].value, "1")
        self.assertEquals(params[2].value, "")


if __name__ == '__main__':
    unittest.main()
