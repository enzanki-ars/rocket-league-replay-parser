import json

data = None

data_end = None
data_start = 0


def load_data(out_prefix):
    global data
    global data_end

    with open(out_prefix) as data_file:
        data = json.load(data_file)

    data_end = max_data_end()


def get_data():
    return data


def set_data_start(new_data_start):
    global data_start

    if max_data_end() > new_data_start > 0:
        data_start = new_data_start
    else:
        print('Warning: Supplied data start is not between 0 and max of',
              max_data_end(), '.', 'Using 0 instead.')
        data_start = 0


def get_data_start():
    return data_start


def set_data_end(new_data_end):
    global data_end

    if 0 < new_data_end < max_data_end():
        data_end = new_data_end
    else:
        print('Warning: Supplied data end is not between 0 and max of',
              max_data_end(), '.', 'Using max instead.')
        data_end = max_data_end()


def get_data_end():
    return data_end


def max_data_end():
    return len(data['content']['frames'])
