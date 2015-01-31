# -*- coding: utf-8 -*-

import os.path
import logging
import re
import sys
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

    def find_by_box(self, query, strict=True):
        for boxes in self._index.values():
            for (p, box) in boxes:
                if self._match_box(query, box):
                    if not strict or self._match_box_strict(query, box):
                        return box
        raise NotFoundError(query.name)

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

    def _match_box(self, query, box):
        logger.debug("_match_box: query.name=%s, box.name=%s"
                     % (query.name, box.name))
        if query.name != box.name:
            return False
        if not self._match_ports(query.get_inputs(), box.get_inputs()):
            return False
        if not self._match_ports(query.get_outputs(), box.get_outputs()):
            return False
        if not self._match_params(query.get_parameters(),
                                  box.get_parameters()):
            return False
        return True

    def _match_ports(self, queryports, boxports):
        if len(queryports) != len(boxports):
            return False
        for (queryp, boxp) in zip(queryports, boxports):
            logger.debug("_match_port: queryp.name=%s, boxp.name=%s"
                         % (queryp.name, boxp.name))
            if queryp.name != boxp.name:
                return False
            if queryp.id != boxp.id:
                return False
            if queryp.type != boxp.type:
                return False
        return True

    def _match_params(self, queryparams, boxparams):
        if len(queryparams) != len(boxparams):
            return False
        for (queryp, boxp) in zip(queryparams, boxparams):
            logger.debug("_match_param: queryp.name=%s, boxp.name=%s"
                         % (queryp.name, boxp.name))
            if queryp.name != boxp.name:
                return False
            if queryp.id != boxp.id:
                return False
            if queryp.content_type != boxp.content_type:
                return False
        return True

    def _match_box_strict(self, query, box):
        logger.debug("_match_box: query.name=%s, box.name=%s"
                     % (query.name, box.name))
        querytags = self._get_tags(query.tooltip)
        boxtags = self._get_tags(box.tooltip)
        if not ("source" in querytags and "source" in boxtags):
            return False
        return querytags["source"] == boxtags["source"]


class Warning:
    def __init__(self, path, message):
        self.path = path
        self.message = message


def load(path):
    if os.path.isdir(path):
        return BoxLib(xarformat.load(path))
    else:
        raise IOError("Not a directory '%s'" % path)


def verify():
    logging.basicConfig(level=logging.ERROR)
    warns = 0
    for path in sys.argv[1:]:
        for warn in load(path).verify_tags():
            print("%s: %s" % (warn.path, warn.message))
            warns += 1
    print("%d warnings" % warns)
    sys.exit(0 if warns == 0 else 1)

if __name__ == '__main__':
    verify()
