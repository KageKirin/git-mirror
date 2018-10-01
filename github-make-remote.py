#! /usr/bin/python

import os
import sys
import argparse
from pathlib import Path
from contextlib import contextmanager
import codecs
import yaml
from github import Github


def loadConfig(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as settingsfile:
        return yaml.load(settingsfile)
    return None


def getGhOrganization(gh, name):
    try:
        return gh.get_organization(name)
    except:
        print(name, 'is not an organization. error')
        return None


def getGhUser(gh, name):
    try:
        return gh.get_user(name)
    except:
        print(name, 'is not an user. error')
        return None


def getGhRepo(gh, path):
    try:
        return gh.get_repo(str(path))
    except:
        print('repo error', path)
        return None


def getGhOwner(gh, path):
    repoOwner = str(Path(str(Path(path).parent).replace(':', '/')).stem)
    org = getGhOrganization(gh, repoOwner)
    if org:
        return org

    user = getGhUser(gh, repoOwner)
    if user and user.name == gh.get_user().name:
        print(repoOwner, "is authorized user")
        return gh.get_user()

    print("only authorized user can create repos in his profile")
    return None


def main(args):
    print('using token:', args.token)
    repoName = str(args.repopath.stem)
    repoOwner = str(Path(str(args.repopath.parent).replace(':', '/')).stem)

    config = loadConfig(args.config)
    assert config, "could not load configuation at {}".format(str(args.config))

    # Github Enterprise with custom hostname
    gh = Github(base_url="https://{}/api/v3".format(config['hostname']), login_or_token=args.token)

    owner = getGhOwner(gh, args.repopath)

    if owner and repoName not in [r.name for r in owner.get_repos()]:
        owner.create_repo(repoName, args.repodesc)
    else:
        print(args.repopath, "already exists")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='config file', type=Path)
    parser.add_argument('-t', '--token', help='user token')
    parser.add_argument('repopath', help='remote repo path', type=Path)
    parser.add_argument('repodesc', help='remote description', type=str)
    args = parser.parse_args()
    main(args)
