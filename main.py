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
    if len(l) == 0:
        return
    for i in range(len(l[0])):
        sorted(l, key=lambda x: x[len(l[0])-i-1],
               reverse=True if sorttype == 'desc' else False)


def radix_sort2(l, sorttype):
    if len(l) == 0:
        return

    #for i in l:
    #    print(i)
    for i in range(len(l[0][2])):
        #print(i, end=' ')
        # print(len(l[0][2]))
        sorted(l, key=lambda x: x[2][len(x[2])-i-1],
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
            #if len(t) < 5:
            #    print(t)
            #    canread = False
            #    break
            t = t.strip().split('  ')
            lines.append(t)

        radix_sort(lines, sorttype)

        if len(lines)>0:
            intermedfile = open('intermed'+str(intermed_fnum)+'.txt', 'w')
            intermed_fnum += 1
            for i in range(len(lines)):
                lines[i] = '  '.join([ele for ele in lines[i]])
                lines[i] += '\n'
            intermedfile.writelines(lines)
            intermedfile.close()
    input_file.close()

    output_file = open(output_fn, 'w')
    fileheap = []
    for i in range(intermed_fnum):
        intermedfile = open('intermed'+str(i)+'.txt', 'r')
        t = intermedfile.readline()
        t = t.strip().split('  ')
        fileheap.append([i, 0, t])
        intermedfile.close()
    #if len(fileheap[-1][2])==1:
    #    fileheap=fileheap[:-1]
    if sorttype == 'asc':
        radix_sort2(fileheap, sorttype)
        intermedsdone = 0
        while intermedsdone < intermed_fnum:
            top = fileheap[0]
            line = '  '.join([ele for ele in top[2]])
            topfile = top[0]
            toplinenum = top[1]
            intermedfile = open('intermed'+str(topfile)+'.txt', 'r')
            newline = intermedfile.readline()
            for i in range(toplinenum+1):
                newline = intermedfile.readline()
            if newline:
                fileheap[0][2] = newline.strip().split('  ')
                fileheap[0][1] = toplinenum+1
            else:
                intermedsdone += 1
                fileheap = fileheap[1:]
            radix_sort2(fileheap, sorttype)
            output_file.write(line+'\n')
            intermedfile.close()
        pass
    else:
        pass

    output_file.close()


def main():
    n_args = len(sys.argv)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    memlimit = int(sys.argv[3])
    sorttype = sys.argv[4]
    user_cols = []
    for i in range(5, n_args):
        user_cols.append(sys.argv[i])
    # limit_memory(memlimit)

    #data = get_data(input_file)
    partsize = 1000
    big_merge_sort(input_file, output_file, partsize, sorttype)


if __name__ == '__main__':
    main()
