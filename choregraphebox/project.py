# -*- coding: utf-8 -*-

import os.path
import lxml.etree as ET
import xarformat
import boxlib
import argparse
import logging

"""
Managing Choregraphe projects
"""

logger = logging.getLogger("choregraphebox")


class Project:
    def __init__(self, file):
        self.file = file
        pml = ET.parse(file)
        self.boxlibs = []
        self.behaviors = []
        for desc in pml.findall(".//BehaviorDescription"):
            if desc.attrib["name"] == "behavior":
                behavior_path = os.path.join(os.path.dirname(file),
                                             desc.attrib["src"])
                self.behaviors.append(
                    xarformat.load(os.path.join(behavior_path,
                                   desc.attrib["xar"])))

    def add_boxlib(self, boxlib):
        self.boxlibs.append(boxlib)

    def replace(self, strict=True):
        for behavior in self.behaviors:
            for box in behavior.get_box().get_all_boxes():
                if not box.has_plugin:
                    try:
                        updated = self._find_by_box(box, strict)
                        logger.info("Found in box library: %s->%s"
                                    % (box.name, updated.name))
                        box.copy_from(updated)
                    except boxlib.NotFoundError:
                        logger.info("Not found in box library: %s" % box.name)

    def save(self):
        for behavior in self.behaviors:
            behavior.xarxml.write(behavior.file, encoding="utf-8",
                                  xml_declaration=True, method="xml")

    def _find_by_box(self, box, strict):
        for lib in self.boxlibs:
            try:
                return lib.find_by_box(box, strict)
            except boxlib.NotFoundError:
                pass
        raise boxlib.NotFoundError(box.name)


def main():
    parser = argparse.ArgumentParser(description="Replace boxes "
                                     "in Choregraphe project")
    parser.add_argument('projects', metavar='PML_PATH', type=str, nargs='+',
                        help='target projects')
    parser.add_argument('--lib', '-l', dest='lib', metavar='BOXLIB_PATHS',
                        type=str, required=True, help="box libraries"
                        "(comma separated)")
    parser.add_argument('--verbose', '-v', dest='verbose', action='store_true',
                        help='verbose output')
    parser.add_argument('--dry-run', dest='dryrun', action='store_true',
                        help='without save')
    parser.add_argument('--ignore-tags', dest='ignoretags',
                        action='store_true', help='disable strict search')

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO if args.verbose else logging.ERROR)

    for project in args.projects:
        logger.info("Target: %s" % project)
        proj = Project(project)
        for lib in args.lib.split(":"):
            logger.info("Load box library: %s" % lib)
            proj.add_boxlib(boxlib.load(lib))
        logger.info("Replacing...")
        proj.replace(strict=not args.ignoretags)
        if not args.dryrun:
            logger.info("Saving...")
            proj.save()

if __name__ == "__main__":
    main()
