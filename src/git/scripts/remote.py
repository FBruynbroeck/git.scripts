# encoding: utf-8
from utils import gitFoldersPath

import argparse
import subprocess
import urllib
import yaml


def changeRemoteFolder(dirpath, url):
    yaml_content = yaml.load(urllib.urlopen(url).read())
    p = subprocess.Popen(["git remote -v | grep push | sed 's$.*/\(.*\).git.*$\\1$g'"], cwd=dirpath, stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    name = out.replace('\n', '')
    if name in yaml_content.keys():
        namespace = yaml_content[name]['namespace']
        p = subprocess.Popen(['git remote set-url origin git@git.affinitic.be:{0}/{1}.git'.format(namespace, name)], cwd=dirpath, shell=True)
        p.wait()


def change_remote():
    parser = argparse.ArgumentParser(description='Change remote.')
    parser.add_argument('path', type=str,
                        help='Path. Example: /Users/Francois/buildout/')
    parser.add_argument('url', type=str,
                        help='Url. Example: http://gitlab.com/repo/bitbucket-migration.yaml')
    args = parser.parse_args()
    for dirpath in gitFoldersPath(args.path):
        changeRemoteFolder(dirpath, args.url)
