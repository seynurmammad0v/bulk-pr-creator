import os
import re
import shutil
import sys
import time

import hiyapyco
from cerberus import Validator
from schema import schema
import const


def change_str(path, changes):
    with open(path) as f:
        s = f.read()
        is_changed = False
        for change in changes:
            if change.get('from') in s or re.compile(change.get('from')).search(s):
                is_changed = True
                s = re.sub(change.get('from'), change.get('to'), s)
            else:
                print('{} NOT FOUND in {}'.format(change.get('from'), path))
        with open(path, 'w') as f:
            f.write(s)
        return is_changed


def push_changes(github):
    os.system('git add .')
    os.system('git commit -m "{}"'.format(github.get('commit')))
    os.system('git push -u origin bulk-{}'.format(github.get('branch')))


def cancel_pipeline(data):
    if data.get('cancel').get('pipeline'):
        # waiting to create workflow runs
        time.sleep(3)
        os.system(" gh run list --limit 1 --json databaseId -q '.[].databaseId' \
                | tr -s  '\n' | xargs  -n1 gh run cancel")


def validate(n):
    if n < 2:
        print("The necessary arguments were not provided : <changelog-file>")
        sys.exit(5)
    if n > 4:
        print("Provided much arguments then expected")
        sys.exit(5)
    filepath = "changelog/" + sys.argv[1] + ".yml"
    validate_file(filepath)


def validate_yml(data, filepath):
    v = Validator(schema)
    if not v.validate(data, schema):
        print("Validation error of file: " + filepath)
        print("Error description: ")
        print(v.errors)
        sys.exit(5)


def validate_file(path):
    if not os.path.exists(path):
        print("The necessary file is not exist :" + path)
        sys.exit(5)


def validate_ms(path):
    if not os.path.exists(path):
        print("The necessary file is not exist :" + path)
        return False
    return True


def get_ms_list(filename):
    path = "repo_list/{}".format(filename)
    validate_file(path)
    return open(path, 'r').readlines()


def copy_file(filename, destination):
    file_path = "../changelog/files/{}".format(filename)
    # print('chmod -R 777 {}{}'.format(os.getcwd(), destination))
    if destination == '':
        destination = os.getcwd()
    shutil.copy2(file_path, '{}'.format(destination))


def login_git(org, ms, branch):
    url = "https://oauth2:{}@github.com/{}/{}.git".format(os.getenv('GITHUB_TOKEN'), org, ms)
    os.system('git clone {}'.format(url))
    if not validate_ms(ms):
        return False
    os.chdir(ms)
    os.system('git remote set-url origin {}'.format(url))
    os.system('git checkout bulk-{} 2>/dev/null || git checkout -b bulk-{}'.format(branch, branch))
    return True


def define_flow(data):
    if data.get(const.ABSOLUTE) is not None:
        return const.ABSOLUTE
    elif data.get(const.FIND_FOLDER) is not None:
        return const.FIND_FOLDER
    elif data.get(const.FIND_FILE) is not None:
        return const.FIND_FILE
    else:
        return const.NONE


def detect_change(prev, new):
    if prev:
        return prev
    if new:
        return new
    return False


def change_yml(path, changes):
    for change in changes:
        merged_yaml = hiyapyco.load([path, "../changelog/files/{}".format(change.get('file'))], method=hiyapyco.METHOD_MERGE)
        with open(path, 'w') as stream:
            stream.write(hiyapyco.dump(merged_yaml))

    return True
