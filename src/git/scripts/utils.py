# encoding: utf-8
import os


def gitFoldersPath(path):
    result = []
    for dirpath, dirnames, files in os.walk(path):
        for dirname in dirnames:
            if dirname == '.git':
                result.append(dirpath)
    return result
