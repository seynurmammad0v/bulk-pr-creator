import os
import sys

import yaml

from edit import edit
from helper import validate, validate_yml
from pr import open_pr
from create import create_file
from revert import revert

if __name__ == '__main__':
    N = len(sys.argv)
    validate(N)

    # for local run
    if N == 4:
        os.environ["GITHUB_ORG"] = sys.argv[2]
        os.environ["GITHUB_TOKEN"] = sys.argv[3]
        os.system("git config --global --unset https.proxy")

    filepath = "changelog/" + sys.argv[1] + ".yml"
    with open(filepath, "r") as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            print("Cannot parce yml file: " + filepath)
            sys.exit(5)

    validate_yml(data, filepath)

    data = data['bulk']
    if data.get('revert'):
        revert(data.get('revert'))

    if data.get('edit'):
        edit(data.get('edit'))

    if data.get('create'):
        create_file(data.get('create'))

    if data.get('pr'):
        open_pr(data.get('pr'))
