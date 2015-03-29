#! -*- coding:utf-8 -*-


class LineReader:
    def __init__(self,f):
        self.file = f
        self.line_no = 0

    def read(self):
        self.line_no += 1
        return self.file.readline()

    def close(self):
        self.file.close()


