import tomllib

def exec_test():
    return

if __name__ == '__main__':
    data = None
    filename = 'test.toml'

    with open(filename, 'rb') as file:
        data = tomllib.load(file)

    glob = data['global']
    data.pop('global')

    if not glob:
        raise Exception(f"{filename}: missing global section")

    for test in data:
        print(f"{test}: {data[test]}")
