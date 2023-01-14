import os
import shutil
import const
import re

from helper import get_ms_list, push_changes, cancel_pipeline, change_str, login_git, define_flow, detect_change, \
    change_yml


def edit(data):
    github = data.get('github')
    org = os.getenv('GITHUB_ORG')
    ms_list = get_ms_list(data.get('repos'))
    for ms in ms_list:
        ms = ms.replace('\n', '')
        if not login_git(org, ms, github.get('branch')):
            continue

        is_changed = edit_file(data)

        if is_changed:
            push_changes(github)
            cancel_pipeline(github)
        os.chdir('../')
        shutil.rmtree(ms)


def edit_file(data):
    is_changed = False
    conf_type = const.NONE
    if data.get("files") is not None:
        conf_type = const.FILE
    if data.get("config") is not None:
        conf_type = const.CONFIG
    if conf_type == const.FILE:
        data = data.get("files")
    elif conf_type == const.CONFIG:
        data = data.get("config")

    for conf in data:
        flow = define_flow(conf)
        if flow == const.ABSOLUTE:
            is_changed = detect_change(is_changed, edit_absolute(conf, conf_type))
        elif flow == const.FIND_FOLDER:
            is_changed = detect_change(is_changed, edit_folder_files(conf, conf_type))
        elif flow == const.FIND_FILE:
            is_changed = detect_change(is_changed, edit_file_by_name(conf, conf_type))
        else:
            continue
    return is_changed


def edit_absolute(data, conf_type):
    return do_changes(data.get('absolute-path'), data.get('changes'), conf_type)


def edit_folder_files(data, conf_type):
    folder_name = data.get(const.FIND_FOLDER)
    is_changed = False
    for root, sub_dirs, _ in os.walk('.'):
        for d in sub_dirs:
            if d == folder_name or re.compile(folder_name).search(d):
                folder_path = root + "/{}".format(d)
                for r, sub, files in os.walk(folder_path):
                    for file in files:
                        path = r + '/' + file
                        is_changed = detect_change(is_changed, do_changes(path, data.get('changes'), conf_type))
    return is_changed


def edit_file_by_name(data, conf_type):
    file_name = data.get(const.FIND_FILE)
    is_changed = False

    for root, sub_dirs, files in os.walk('.'):
        for name in files:
            if (name == file_name or re.compile(file_name).search(name)) and "main" in root:
                path = root + '/{}'.format(name)
                is_changed = detect_change(is_changed, do_changes(path, data.get('changes'), conf_type))
    return is_changed


def do_changes(path, data, conf_type):
    try:
        current_change = False
        if conf_type == const.FILE:
            current_change = change_str(path, data)
        if conf_type == const.CONFIG:
            current_change = change_yml(path, data)
        if not current_change:
            print("No changes in {}", path)
        return current_change
    except:
        print("An exception occurred in path {}".format(path))
        return False
