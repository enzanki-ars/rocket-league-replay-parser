import json

data = None

data_end = None


def load_data(out_prefix):
    global data
    global data_end

    with open(out_prefix) as data_file:
        data = json.load(data_file)

    data_end = max_data_end()


def get_data():
    return data


def set_data_end(new_data_end):
    global data_end

    if new_data_end < max_data_end():
        data_end = new_data_end
    else:
        print('Warning: Supplied data end is greater than max of',
              max_data_end(), '.', 'Using max instead.')
        data_end = max_data_end()


def get_data_end():
    return data_end


def max_data_end():
    return len(data['content']['frames'])
