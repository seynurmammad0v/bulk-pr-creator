import os
import shutil

from helper import get_ms_list, push_changes, cancel_pipeline, copy_file, validate_ms, login_git


def create_file(data):
    github = data.get('github')
    org = os.getenv('GITHUB_ORG')
    ms_list = get_ms_list(data.get('repos'))
    for ms in ms_list:
        ms = ms.replace('\n', '')
        if not login_git(org, ms, github.get('branch')):
            continue
        for file in data.get('files'):
            copy_file(file.get('filename'), file.get('destination'))

        push_changes(github)
        cancel_pipeline(github)
        os.chdir('../')
        shutil.rmtree(ms)
