import os
import time


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


def cancel_pipeline(github):
    if github.get('cancel').get('pipeline'):
        # waiting to create workflow runs
        time.sleep(3)
        os.system(" gh run list --limit 1 --json databaseId -q '.[].databaseId' \
                | tr -s  '\n' | xargs  -n1 gh run cancel")
