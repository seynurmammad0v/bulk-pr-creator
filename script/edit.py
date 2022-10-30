import os
import shutil

from helper import *


def edit_file(data):
    github = data.get('github')
    org = os.getenv('GITHUB_ORG')
    repos_file = "repo_list/{}".format(data.get('repos'))
    ms_list = open(repos_file, 'r').readlines()
    for ms in ms_list:
        ms = ms.replace('\n', '')
        url = "https://oauth2:{}@github.com/{}/{}.git".format(os.getenv('GITHUB_TOKEN'), org, ms)
        os.system('git clone {}'.format(url))
        os.system('git remote set-url origin {}'.format(url))
        os.chdir(ms)
        is_changed = False
        for file in data.get('files'):
            is_changed = True if change_str(file.get('path'), file.get('changes')) else print("No changes in {}",
                                                                                              file.get('path'))
        if is_changed:
            os.system('git checkout -b {}'.format(github['branch']))
            os.system('git add .')
            os.system('git commit -m "{}"'.format(github.get('commit')))
            os.system('git push -u origin {}'.format(github.get('branch')))
            if github.get('cancel').get('pipeline'):
                os.system(" gh run list --limit 1 --json databaseId -q '.[].databaseId' \
                | tr -s  '\n' | xargs  -n1 gh run cancel")
        os.chdir('../')
        shutil.rmtree(ms)
