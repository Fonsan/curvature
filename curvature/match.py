
class And(object):
    def __init__(self, *terms):
        try:
            for term in terms:
                if not callable(term.match):
                    raise ValueError('Terms must support a "match" method.')
            self.terms = terms
        except AttributeError:
            raise ValueError('Terms must support a "match" method.')

    def match(self, way_or_collection):
        for term in self.terms:
            if not term.match(way_or_collection):
                return False
        return True

    def match_collection(self, collection):
        for term in self.terms:
            if not term.match(collection):
                return False
        return True

    def match_way(self, way):
        for term in self.terms:
            if not term.match_way(way):
                return False
        return True

class Or(And):
    def match(self, way_or_collection):
        for term in self.terms:
            if term.match(way_or_collection):
                return True
        return False

    def match_collection(self, collection):
        for term in self.terms:
            if term.match(collection):
                return True
        return False

    def match_way(self, way):
        for term in self.terms:
            if term.match_way(way):
                return True
        return False

class Not(object):
    def __init__(self, term):
        try:
            if not callable(term.match):
                raise ValueError('Terms must support a "match" method.')
            self.term = term
        except AttributeError:
            raise ValueError('Terms must support a "match" method.')

    def match(self, way_or_collection):
        return not self.term.match(way_or_collection)

    def match_collection(self, collection):
        return not self.term.match_collection(collection)

    def match_way(self, way):
        return not self.term.match_way(way)

class WayMatcher(object):

    def match(self, way_or_collection):
        if 'ways' in way_or_collection:
            return self.match_collection(way_or_collection)
        else:
            return self.match_way(way_or_collection)

    def match_collection(self, collection):
        if not 'ways' in collection:
            raise ValueError('Collections must be a dict with a "ways" key. Received {}'.format(collection))
        for way in collection['ways']:
            if self.match_way(way):
                return True
        return False

class TagEmpty(WayMatcher):

    def __init__(self, tag):
        if not tag:
            raise ValueError('tag must not be empty')
        self.tag = tag

    def match_way(self, way):
        return self.tag not in way['tags'] or way['tags'][self.tag] == ''

class TagEquals(WayMatcher):

    def __init__(self, tag, value):
        if not tag:
            raise ValueError('tag must not be empty')
        self.tag = tag
        if not value:
            raise ValueError('value must not be empty')
        self.value = value

    def match_way(self, way):
        if 'tags' not in way:
            raise ValueError('Ways must be a dict with a "tags" key. Received {}'.format(way))
        if self.tag not in way['tags']:
            return False
        return way['tags'][self.tag] == self.value