import resource
import sys


def limit_memory(memlimit):
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (memlimit, hard))


def get_data(input_fn):
    metadata = open('Metadata.txt', 'r')
    data = {}
    while True:
        col = metadata.readline()
        if not col:
            break
        col = col.strip().split(',')
        data[col[0]] = []
    datafile = open(input_fn, 'r')

    while True:
        row = datafile.readline()
        if not row:
            break
        row = row.strip().split('  ')
        j = 0
        for col in data.keys():
            data[col].append(row[j])
            j += 1
    
    return data


def main():
    n_args = len(sys.argv)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    memlimit = int(sys.argv[3])
    sorttype = sys.argv[4]
    user_cols = []
    for i in range(5, n_args):
        user_cols.append(sys.argv[i])
    limit_memory(memlimit)

    data = get_data(input_file)
    print(data)


if __name__ == '__main__':
    main()
