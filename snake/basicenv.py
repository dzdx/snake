#!/usr/bin/env python
# coding=utf-8


class BasicEnv(object):

    def __init__(self):
        self.value = dict()

    def put(self, name, value):
        self.value[name] = value

    def get(self, name):
        return self.value.get(name)


class BasicEvaluator(object):
    TRUE = 1
    FALSE = 0
