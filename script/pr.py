import os
import time

from helper import get_ms_list


def open_pr(data):
    org = os.getenv('GITHUB_ORG')
    ms_list = get_ms_list(data.get('repos'))
    for ms in ms_list:
        ms = ms.replace('\n', '')
        print('Creating pull request for {} into {} in {}/{}'.format(data.get('from'), data.get('to'), org, ms))
        os.system('gh api --method POST -H "Accept: application/vnd.github+json" /repos/{}/{}/pulls -f title=\'{}\' '
                  '-f body=\'{}\' -f head=\'PB-Digital:{}\' -f base=\'{}\' '.format(org,
                                                                                    ms,
                                                                                    data.get('name'),
                                                                                    data.get('body'),
                                                                                    data.get('from'),
                                                                                    data.get('to')))
        time.sleep(1.5)
