import json
import os
import subprocess
import time

from helper import get_ms_list


def open_pr(data):
    org = os.getenv('GITHUB_ORG')
    ms_list = get_ms_list(data.get('repos'))

    index = 0
    while index < len(ms_list):
        ms = ms_list[index]
        ms = ms.replace('\n', '')

        print('Creating pull request for bulk-{} into {} in {}/{}'.format(data.get('from'), data.get('to'), org, ms))

        try:
            subprocess.check_output(
                ['gh', 'api',
                 '--method', 'POST',
                 '-H', 'Accept:application/vnd.github+json',
                 '/repos/{}/{}/pulls'.format(org, ms),
                 '-f', 'title=\'{}\''.format(data.get('name')),
                 '-f', 'body=\'{}\''.format(data.get('body')),
                 '-f', 'head=PB-Digital:bulk-{}'.format(data.get('from')),
                 '-f', 'base={}'.format(data.get('to'))])
            print('Success {}'.format(ms))
        except subprocess.CalledProcessError as e:
            message = str(e.output, "utf-8")
            if 'You have exceeded a secondary rate limit' in message:
                print("403 exceeded a secondary rate limit service {} \nTrying again after few minutes".format(ms))
                time.sleep(180)
                continue
            if 'A pull request already exists for' in message:
                print("PR exist {}".format(ms))
                index = index + 1
                continue
            if "No commits between develop and bulk-change-checkout-version" in message:
                print("No changes {}".format(ms))
                index = index + 1
                continue
            else:
                print("Service - {} message - {}".format(ms, message))
                index = index + 1
                continue
        index = index + 1
        time.sleep(7)
