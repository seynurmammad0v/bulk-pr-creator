import os
import shutil
import subprocess

from helper import get_ms_list, login_git


def get_git_revision_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()


def get_last_commit_name() -> str:
    return subprocess.check_output(['git', 'show', '-s', '--format=%s']).decode('ascii').strip()


if __name__ == '__main__':
    print(get_last_commit_name())


def revert(data):
    org = os.getenv('GITHUB_ORG')
    ms_list = get_ms_list(data.get('repos'))
    for ms in ms_list:
        ms = ms.replace('\n', '')
        if not login_git(org, ms, data.get('branch')):
            continue
        last_commit_hash = get_git_revision_hash()
        last_commit_name = get_last_commit_name()
        if last_commit_name == data.get('commit'):
            os.system('git push origin +{}^:bulk-{}'.format(last_commit_hash, data.get('branch')))
        os.chdir('../')
        shutil.rmtree(ms)
