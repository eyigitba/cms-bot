#!/usr/bin/env python
"""
Gets list of files that will be modified by all PRs for the branch.
Dumps to file to be loaded by other script.
"""

from github import Github
from github_utils import *
from os.path import expanduser
from repo_config import GH_TOKEN
from argparse import ArgumentParser
import json


def main():
    parser = ArgumentParser()
    parser.add_argument("-r", "--repo")
    parser.add_argument("-d", "--destination")
    args = parser.parse_args()

    gh = Github(login_or_token=open(expanduser(GH_TOKEN)).read().strip())
    repo = gh.get_repo(args.repo)
    pr_list = get_pull_requests(repo)

    rez = {}
    for pr in pr_list:
        rez[int(pr.number)] = {
            'number': int(pr.number),
            'state': pr.state,
            'created_at': int(pr.created_at.strftime("%s")),
            'updated_at': int(pr.updated_at.strftime("%s")),
            'changed_files_names': pr_get_changed_files(pr)
        }
    with open(args.destination, 'w') as d:
        json.dump(rez, d)


if __name__ == '__main__':
    main()
