#! -*- coding:utf-8 -*-


class FileReader:
    def __init__(self, f):
        self.file = f
        self.line_no = 0
        self.tmp_char = ""

    def read_line(self):
        self.line_no += 1
        return self.file.readline()

    def read_char(self):
        char = self.file.read(1)
        if char == '\n':
            self.line_no += 1
        return char


    def close(self):
        self.file.close()
