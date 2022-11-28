import os
import shutil
import const
import re

from helper import get_ms_list, push_changes, cancel_pipeline, change_str, login_git, define_flow


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
            flow = define_flow(file)

            if flow == const.ABSOLUTE:
                is_changed = edit_absolute(file)
            elif flow == const.FIND_FOLDER:
                is_changed = edit_folder_files(file)
            elif flow == const.FIND_FILE:
                is_changed = edit_file_by_name(file)
            else:
                continue

        if is_changed:
            push_changes(github)
            cancel_pipeline(github)
        os.chdir('../')
        shutil.rmtree(ms)


def edit_absolute(file):
    is_changed = True \
        if change_str(file.get('absolute-path'), file.get('changes')) \
        else print("No changes in {}", file.get('absolute-path'))
    return is_changed


def edit_folder_files(data):
    folder_name = data.get(const.FIND_FOLDER)
    for root, sub_dirs, _ in os.walk('.'):
        for d in sub_dirs:
            if (d == folder_name or re.compile(folder_name).search(d)) and "main" in root:
                folder_path = root + "/{}".format(d)
                for _, _, files in os.walk(folder_path):
                    for file in files:
                        if not change_str(folder_path + '/' + file, data.get('changes')):
                            print("No changes in {}", folder_path + '/' + file)
    return True


def edit_file_by_name(data):
    file_name = data.get(const.FIND_FILE)
    for root, sub_dirs, files in os.walk('.'):
        for name in files:
            if (name == file_name or re.compile(file_name).search(name)) and "main" in root:
                if not change_str(root + '/{}'.format(name), data.get('changes')):
                    print("No changes in {}", root + '/{}'.format(name))
    return True
