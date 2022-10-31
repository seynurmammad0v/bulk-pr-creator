import os
import shutil

from helper import get_ms_list, push_changes, cancel_pipeline, change_str, validate_ms, login_git


def edit_file(data):
    github = data.get('github')
    org = os.getenv('GITHUB_ORG')
    ms_list = get_ms_list(data.get('repos'))
    for ms in ms_list:
        ms = ms.replace('\n', '')
        if not login_git(org, ms, github.get('branch')):
            continue
        is_changed = False
        for file in data.get('files'):
            is_changed = True if change_str(file.get('path'), file.get('changes')) else print("No changes in {}",
                                                                                              file.get('path'))
        if is_changed:
            push_changes(github)
            cancel_pipeline(github)
        os.chdir('../')
        shutil.rmtree(ms)
