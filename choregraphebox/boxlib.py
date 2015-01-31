# -*- coding: utf-8 -*-

import os.path
import logging
import re
import xarformat

logger = logging.getLogger('choregraphebox')


class NotFoundError(Exception):
    pass


class BoxLib:
    def __init__(self, xarnode):
        self.xarnode = xarnode
        self._index = {}
        self._make_index("", xarnode)

    def find_by_path(self, path):
        for boxes in self._index.values():
            for (p, box) in boxes:
                if p == path:
                    return box
        raise NotFoundError(path)

    def verify_tags(self):
        warnings = []
        for boxes in self._index.values():
            for (path, box) in boxes:
                logger.info("Name: %s" % path)
                tags = self._get_tags(box.tooltip)
                for (key, value) in tags.items():
                    logger.info("Tag: %s=%s" % (key, value))
                if "source" not in tags:
                    logger.warn("%s: Tag '@source' is not defined in tooltip"
                                % path)
                    warnings.append(Warning(path,
                                    "Tag '@source' is not defined in tooltip"))
        return warnings

    def _get_tags(self, tooltip):
        tags = {}
        tagp = re.compile(r'\s*@([a-zA-Z][a-zA-Z0-9_]*)\s+(.*)\s*')
        for line in tooltip.splitlines():
            tagm = tagp.match(line)
            if tagm:
                tags[tagm.group(1)] = tagm.group(2)
        return tags

    def _make_index(self, path, xarnode):
        if xarnode.get_box():
            box = xarnode.get_box()
            boxinfo = (path, box)
            if box.name in self._index:
                self._index[box.name].append(boxinfo)
            else:
                self._index[box.name] = [boxinfo]
        for child in xarnode.get_children():
            self._make_index(path + "/" + child.name, child)


class Warning:
    def __init__(self, path, message):
        self.path = path
        self.message = message


def load(path):
    if os.path.isdir(path):
        return BoxLib(xarformat.load(path))
    else:
        raise IOError("Not a directory '%s'" % f)
