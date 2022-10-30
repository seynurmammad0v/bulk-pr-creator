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
