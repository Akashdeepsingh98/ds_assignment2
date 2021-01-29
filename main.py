import resource
import sys
import heapq


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


def radix_sort(l, sorttype):
    for i in range(len(l[0])):
        sorted(l, key=lambda x: x[len(l[0])-i-1],
               reverse=True if sorttype == 'desc' else False)


def big_merge_sort(input_fn, output_fn, partsize, sorttype='asc'):
    input_file = open(input_fn, 'r')
    intermed_fnum = 0
    canread = True
    while canread:
        lines = []

        for i in range(partsize):
            t = input_file.readline()
            if not t:
                canread = False
                break
            t = t.strip().split('  ')
            lines.append(t)

        radix_sort(lines, sorttype)

        intermedfile = open('intermed'+str(intermed_fnum)+'.txt', 'w')
        intermed_fnum+=1
        for i in range(len(lines)):
            lines[i] = '  '.join([ele for ele in lines[i]])
            lines[i] += '\n'
        intermedfile.writelines(lines)
        intermedfile.close()
    input_file.close()

    output_file = open(output_fn, 'w')
    


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

    #data = get_data(input_file)
    partsize = 1000
    big_merge_sort(input_file, output_file, partsize, sorttype)


if __name__ == '__main__':
    main()
