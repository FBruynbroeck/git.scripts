# encoding: utf-8
"""
hooks.py

Created by FBruynbroeck on 2015-09-22.
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl
"""
import argparse
import os
import subprocess


def removeFolder(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path)


def gitFoldersPath(path):
    result = []
    for dirpath, dirnames, files in os.walk(path):
        for dirname in dirnames:
            if dirname == '.git':
                result.append(dirpath)
    return result


def gitInit(path):
    p = subprocess.Popen(['git', 'init'], cwd=path)
    p.wait()


def removeGitHooksFolder(path):
    path = os.path.join(path, '.git', 'hooks')
    if os.path.exists(path):
        print 'Remove Hooks repository in %s/.git' % path
        removeFolder(path)


def reload_hooks():
    parser = argparse.ArgumentParser(description='Reload Hooks.')
    parser.add_argument('path', type=str,
                        help='Path. Example: /Users/Francois/buildout/')
    args = parser.parse_args()
    for dirpath in gitFoldersPath(args.path):
        removeGitHooksFolder(dirpath)
        gitInit(dirpath)


def remove_hooks():
    parser = argparse.ArgumentParser(description='Remove Hooks.')
    parser.add_argument('path', type=str,
                        help='Path. Example: /Users/Francois/buildout/')
    args = parser.parse_args()
    for dirpath in gitFoldersPath(args.path):
        removeGitHooksFolder(dirpath)
