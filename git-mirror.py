#! /usr/bin/python

import os
import sys
import argparse
from pathlib import Path
from contextlib import contextmanager
import codecs
import yaml


def loadConfig(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as settingsfile:
        return yaml.load(settingsfile)
    return None

@contextmanager
def pushPath(path):
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)


def mirrorRepo(repo, config):
    print('repo', repo, config)

    repopath = Path.cwd().joinpath(repo)
    if args.do_fetch:
        if not repopath.exists():
            createMirrorRepo(repopath, config)
        else:
            updateMirrorRepo(repopath, config)
    if args.do_push:
        pushMirrors(repopath, config)


def createMirrorRepo(repopath, config):
    cmd_args = ['git', 'clone', '--mirror']
    cmd_args.extend([config['origin']])
    cmd_args.extend([str(repopath)])
    cmd = " ".join(cmd_args)
    print(cmd)
    os.system(cmd)


def updateMirrorRepo(repopath, config):
    with pushPath(repopath):
        cmd_args = ['git', 'fetch', '--all']
        cmd = " ".join(cmd_args)
        print(cmd)
        os.system(cmd)


def pushMirrors(repopath, config):
    with pushPath(repopath):
        for mirror in config['mirrors']:
            cmd_args = ['git', 'push', '--all']
            cmd_args.extend([mirror])
            cmd = " ".join(cmd_args)
            print(cmd)
            os.system(cmd)


def main(args):
    config = loadConfig(args.config)
    assert config, "could not load configuation at {}".format(str(args.config))

    for repo in config:
        mirrorRepo(repo, config[repo])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='config file', type=Path)
    parser.add_argument('--no-fetch', dest='do_fetch',  help='skip fetching remotes', action='store_false')
    parser.add_argument('--no-push', dest='do_push', help='skip pushing back to mirrors', action='store_false')
    args = parser.parse_args()
    main(args)


