import os
import sys
import time

from cerberus import Validator
from schema import schema


def change_str(path, changes):
    with open(path) as f:
        s = f.read()
        is_changed = False
        for change in changes:
            if change.get('from') in s:
                is_changed = True
                with open(path, 'w') as f:
                    s = s.replace(change.get('from'), change.get('to'))
                    f.write(s)
            else:
                print('{} NOT FOUND in {}'.format(change.get('from'), path))
        return is_changed


def push_changes(github):
    os.system('git checkout -b {}'.format(github.get('branch')))
    os.system('git add .')
    os.system('git commit -m "{}"'.format(github.get('commit')))
    os.system('git push -u origin {}'.format(github.get('branch')))


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
