#!/usr/bin/env python

from angler.plugin import Plugin

import os

class Path(Plugin):
    schemes = ['path']

    def get_parent(self):
        path = os.path.dirname(self.path)
        if path == '/':
            return None
        return Path(
            session=self.session,
            scheme=self.scheme,
            host=self.host,
            path=path,
            query='',
            fragment='',
            value='folder',
        )

    def found_node(self):
        parent = self.get_parent()
        if parent:
            self.session.add_node(parent)
            parent.found_node()
            self.session.add_edge(parent, self)