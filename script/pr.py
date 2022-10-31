import os
import shutil
import time

from helper import get_ms_list, cancel_pipeline, validate_ms


def open_pr(data):
    org = os.getenv('GITHUB_ORG')
    ms_list = get_ms_list(data.get('repos'))
    for ms in ms_list:
        ms = ms.replace('\n', '')
        url = "https://oauth2:{}@github.com/{}/{}.git".format(os.getenv('GITHUB_TOKEN'), org, ms)
        os.system('git clone {}'.format(url))
        if not validate_ms(ms):
            continue
        os.system('git remote set-url origin {}'.format(url))
        os.chdir(ms)
        os.system("git checkout {}".format(data.get('from')))
        os.system('gh pr create -B {} -a {} -t "{}" -b "{}" '.format(data.get('to'), data.get('assignee'),
                                                                     data.get('name'), data.get('body')))
        cancel_pipeline(data)
        os.chdir('../')
        shutil.rmtree(ms)
        time.sleep(5)
