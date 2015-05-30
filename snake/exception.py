#! -*- utf-8 -*-
class StoneException(Exception):

    def __init__(self, m, t):
        Exception.__init__(self, m+" "+t.location())
    pass


class ParseException(Exception):
    pass
