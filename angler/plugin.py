
import logging
import re

def urisplit(uri):
    pattern = "^([a-zA-Z+_-]+)://([^/]*)(/[^?#]*)(?:\?([^#]*))?(?:#(.*))?$"
    match = re.match(pattern, uri)
    if match is None:
        raise ValueError("Unable to parse uri {!r}".format(uri))
    return match.groups()


def urijoin(scheme, host, path, query, fragment):
    if not path.startswith('/'):
        raise ValueError("Invalid 'path': {!r}".format(path))
    return '{scheme}://{host}{path}{query}{fragment}'.format(
        scheme=scheme,
        host=host,
        path=path,
        query=(query or '') and '?' + query,
        fragment=(fragment or '') and '?' + fragment
    )


class Plugin(object):
    def __init__(self, session, scheme, host, path, query, fragment, value):
        self.session = session
        self.scheme = scheme
        self.host = host
        self.path = path
        self.query = query
        self.fragment = fragment
        self.value = value
        self.logger = logging.getLogger(scheme)

    def __hash__(self):
        return hash((self.scheme, self.host, self.path, self.query,
                     self.fragment))

    @classmethod
    def from_node(cls, session, node):
        return cls(session, value=node.value, *urisplit(node.uri))

    def get_uri(self):
        return urijoin(self.scheme, self.host, self.path, self.query,
                       self.fragment)

    def found_node(self):
        pass

    def found_incoming_edge(self, source):
        pass

    def found_outgoing_edge(self, sink):
        pass