import sys
import yaml
from cerberus import Validator

from schema import schema

from edit import *

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("The necessary arguments were not provided : <changelog-file>")
        sys.exit(5)

    filepath = "changelog/" + sys.argv[1] + ".yml"
    if not os.path.exists(filepath):
        print("The necessary file is not exist :" + filepath)
        sys.exit(5)

    with open(filepath, "r") as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            print("Cannot parce yml file: " + filepath)
            sys.exit(5)

    v = Validator(schema)
    if not v.validate(data, schema):
        print("Validation error of file: " + filepath)
        print("Error description: ")
        print(v.errors)
        sys.exit(5)

    data = data['bulk']

    if data.get('edit'):
        edit_file(data.get('edit'))
        print("edit")

    if data.get('create'):
        print("create")

    if data.get('pr'):
        print('pr')
