#! /usr/bin/python

import os
import sys
import argparse
from pathlib import Path
from contextlib import contextmanager
import codecs
import yaml
from gitlab import Gitlab


def loadConfig(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as settingsfile:
        return yaml.load(settingsfile)
    return None


def getGitlabGroupId(gl, name):
    try:
        return gl.groups.search(name)[0].id
    except:
        print(name, 'is not an organization. error')
        return None

def getGitlabUserId(gl, name):
    try:
        return gl.users.list(username=name)[0].id
    except:
        print(name, 'is not an user. error')
        return None

def getGitlabOwnerId(gl, path):
    repoOwner = str(Path(str(Path(path).parent).replace(':', '/')).stem)
    groupId = getGitlabGroupId(gl, repoOwner)
    if groupId:
        return groupId, False

    userId = getGitlabUserId(gl, repoOwner)
    if userId and userId == gl.user.id:
        print(repoOwner, "is authorized user")
        return userId, True

    print("only authorized user can create repos in his profile")
    return None, None



def getGitlabUserRepoNames(gl, userId):
    user = gl.users.get(userId)
    return [p.name for p in user.projects.list()]

def getGitlabUserGroupNames(gl, groupId):
    group = gl.groups.get(userId)
    return [p.name for p in group.projects.list()]


def createGitlabUserRepo(gl, config, userId, repoName, repoDesc):
    p = gl.projects.create({
        'name': repoName,
        'description': repoDesc,
        'user_id': userId,
        'lfs_enabled': config['lfs_enabled'],
        'visibility': config['visibility']
        })

def createGitlabGroupRepo(gl, config, groupId, repoName, repoDesc):
    p = gl.projects.create({
        'name': repoName,
        'description': repoDesc,
        'namespace_id': groupId,
        'lfs_enabled': config['lfs_enabled'],
        'visibility': config['visibility']
        })





def main(args):
    repoName = str(args.repopath.stem)
    repoOwner = str(Path(str(args.repopath.parent).replace(':', '/')).stem)

    config = loadConfig(args.config)
    assert config, "could not load configuation at {}".format(str(args.config))

    # Gitlab or custom hostname
    gl = Gitlab("https://{}".format(config['hostname']), private_token=args.token)
    gl.auth()

    ownerId, isUser = getGitlabOwnerId(gl, args.repopath)

    if not ownerId:
        print("could not find project owner", repoOwner)

    if isUser:
        if ownerId and repoName not in getGitlabUserRepoNames(gl, ownerId):
            createGitlabUserRepo(gl, config, ownerId, repoName, args.repodesc)
        else:
            print(args.repopath, "already exists")
    else:
        if ownerId and repoName not in getGitlabUserGroupNames(gl, ownerId):
            createGitlabGroupRepo(gl, config, ownerId, repoName, args.repodesc)
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
