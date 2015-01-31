# -*- coding: utf-8 -*-

import os.path
import lxml.etree as ET
import urllib
import copy
import re

"""
Loading Choregraphe behavior/box archive files
"""

NS_PROJECT = 'http://www.aldebaran-robotics.com/schema/choregraphe/project.xsd'


class BasePort:
    def __init__(self, node):
        self.id = node.attrib["id"]
        self.name = node.attrib["name"]


class Port(BasePort):
    def __init__(self, node):
        BasePort.__init__(self, node)
        assert int(node.attrib["type_size"]) == 1
        self.type = int(node.attrib["type"])


class Parameter(BasePort):
    def __init__(self, node):
        BasePort.__init__(self, node)
        self.content_type = node.attrib["content_type"]
        self.value = node.attrib["value"]


class Box:
    def __init__(self, node, name=None, prefix=""):
        self.name = name if name else node.attrib["name"]
        self.node = node
        self.prefix = prefix
        self.tooltip = node.attrib["tooltip"]

    def get_inputs(self):
        return [Port(node)
                for node in self.node.findall(self.prefix + "Input")]

    def get_outputs(self):
        return [Port(node)
                for node in self.node.findall(self.prefix + "Output")]

    def get_parameters(self):
        return [Parameter(node)
                for node in self.node.findall(self.prefix + "Parameter")]

    def get_all_boxes(self):
        return [Box(node, prefix=self.prefix)
                for node in self.node.findall(".//%sBox" % self.prefix)]

    def copy_from(self, source):
        preserved_keys = set(["name", "id", "x", "y"])
        for attrname in set(source.node.keys()) - preserved_keys:
            self.node.set(attrname, source.node.attrib[attrname])
        parampat = re.compile(r'(\{.+\})?Parameter')
        old_params = {}
        for child in list(self.node.getchildren()):
            self.node.remove(child)
            if parampat.match(child.tag) and "id" in child.attrib:
                old_params[child.attrib["id"]] = child
        for source_child in source.node.getchildren():
            child = copy.deepcopy(source_child)
            if parampat.match(child.tag) and "id" in child.attrib:
                new_id = child.attrib["id"]
                if new_id in old_params:
                    child.attrib["value"] = old_params[new_id].attrib["value"]
            self.node.append(child)


class XARArchive:
    def __init__(self, file, name=None, prefix=""):
        self.file = file
        self.name = name if name else os.path.basename(os.path.dirname(file))
        self.prefix = prefix
        self.xarxml = None
        self.box = None

    def get_children(self):
        return []

    def get_box(self):
        if self.box:
            return self.box
        xarxml = ET.parse(self.file, parser=ET.XMLParser(strip_cdata=False))
        verify_xar_version(xarxml.getroot())
        boxes = xarxml.findall(self.prefix + "Box")
        if len(boxes) != 1:
            raise IOError("Only one Box element is allowed"
                          " (%d Box elements found)" % len(boxes))
        self.box = Box(boxes[0], self.name, self.prefix)
        self.xarxml = xarxml
        return self.box

    def findall(self, name):
        return []

    def find(self, name):
        return None


class XARFolder:
    def __init__(self, dir, name=None):
        self.dir = dir
        self.name = name if name else os.path.basename(dir)
        xalinfo = ET.parse(os.path.join(self.dir, "xalinfo"))
        self.box = None
        self.children = []
        names = [node.attrib['name'] for node in xalinfo.findall("Node")]
        for dirname in os.listdir(self.dir):
            if dirname in names:
                name = dirname
            elif urllib.unquote(dirname) in names:
                name = urllib.unquote(dirname)
            else:
                continue
            dir = os.path.join(self.dir, dirname)
            behavior_xar = os.path.join(dir, "behavior.xar")
            box_xar = os.path.join(dir, "box.xar")
            if os.path.exists(os.path.join(dir, "xalinfo")):
                self.children.append(XARFolder(dir, name))
            elif os.path.exists(behavior_xar):
                self.children.append(XARArchive(behavior_xar, name,
                                     "{%s}" % NS_PROJECT))
            elif os.path.exists(box_xar):
                self.children.append(XARArchive(box_xar, name))
            else:
                raise IOError("An archive type for '%s' is not known" % dir)

    def get_children(self):
        return self.children

    def get_box(self):
        return None

    def find(self, name):
        for child in self.children:
            if child.name == name:
                return child
        for child in self.children:
            box = child.find(name)
            if box:
                return box
        return None

    def findall(self, name):
        found = []
        for child in self.children:
            if child.name == name:
                found.append(child)
        for child in self.children:
            found.extend(child.findall(name))
        return found


def load(f):
    """
    Loading archive from file or directory
    """
    if isinstance(f, basestring):
        if os.path.isdir(f):
            return XARFolder(f)
        elif os.path.isfile(f):
            return XARArchive(f, prefix="{%s}" % NS_PROJECT)
        else:
            raise IOError("Unknown file path '%s'" % f)
    else:
        return XARArchive(f, name="behavior.xar", prefix="{%s}" % NS_PROJECT)


def verify_xar_version(elem):
    if elem.attrib["xar_version"] != "3":
        raise IOError("Unknown xar version '%s' is detected"
                      % elem.attrib["xar_version"])
