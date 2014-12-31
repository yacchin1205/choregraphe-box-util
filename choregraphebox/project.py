# -*- coding: utf-8 -*-

import os.path
import xml.etree.ElementTree as ET
import xarformat

"""
Managing Choregraphe projects
"""

ET.register_namespace("", 'http://www.aldebaran-robotics.com/schema/choregraphe/project.xsd')

class Project:
    def __init__(self, file):
        self.file = file
        pml = ET.parse(file)
        self.boxlibs = []
        self.behaviors = []
        for desc in pml.findall(".//BehaviorDescription"):
            if desc.attrib["name"] == "behavior":
                behavior_path = os.path.join(os.path.dirname(file), desc.attrib["src"])
                self.behaviors.append(xarformat.load(os.path.join(behavior_path, desc.attrib["xar"])))
                
    def add_boxlib(self, boxlib):
        self.boxlibs.append(boxlib)
        
    def replace(self):
        for behavior in self.behaviors:
            for box in behavior.get_box().get_all_boxes():
                base = self._find_box(box.name)
                if base:
                    box.copy_from(base.get_box())
                    
    def save(self):
        for behavior in self.behaviors:
            #behavior.xarxml.write(behavior.file, encoding="utf-8", xml_declaration=True, method="xml")
            raise NotImplementedError()
        
    def _find_box(self, name):
        for boxlib in self.boxlibs:
            box = boxlib.find(name)
            if box:
                return box
        return None