import resource
import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)


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
    length = len(l[0])
    for i in range(length):
        if sorttype == 'asc':
            l.sort(key=lambda x: x[length-i-1])
        else:
            l.sort(key=lambda x: x[length-i-1], reverse=True)


def radix_sort2(l, sorttype):
    if len(l) == 0:
        return
    length = len(l[0][2])
    for i in range(length):
        if sorttype == 'asc':
            l.sort(key=lambda x: x[2][length-i-1])
        else:
            l.sort(key=lambda x: x[2][length-i-1], reverse=True)

def big_merge_sort(input_fn, output_fn, partsize, sorttype, allcols, user_cols):
    input_file = open(input_fn, 'r')
    intermed_fnum = 0
    canread = True
    while canread:
        lines = []

        for i in range(partsize):
            t = input_file.readline()  # read a line
            if not t:
                canread = False
                break

            rowlist = []  # list of elements in the row
            index = 0  # cuurent index at t
            if t[-1] == '\n':
                t = t[:-1]

            for col in allcols:  # go through all columns
                colname = col[0]  # name of current column
                collen = col[1]  # length of current column
                colstr = ''  # string for this column
                for j in range(collen):  # read collen bytes into colstr
                    colstr += t[index]
                    index += 1
                index += 2  # skip 2 whitespaces
                if colname in user_cols:  # if colname is in user cols only then append to rowlist
                    rowlist.append(colstr)
            lines.append(rowlist)

        radix_sort(lines, sorttype)

        if len(lines) > 0:
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
        rowlist = []
        index = 0
        if t[-1] == '\n':
            t = t[:-1]
        for col in allcols:
            colname = col[0]
            collen = col[1]
            if colname in user_cols:
                colstr = ''
                for j in range(collen):
                    colstr += t[index]
                    index += 1
                index += 2
                rowlist.append(colstr)
        fileheap.append([i, 0, rowlist])
        intermedfile.close()

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
            rowlist = []
            index = 0
            if newline[-1] == '\n':
                newline = newline[:-1]
            for col in allcols:
                colname = col[0]
                collen = col[1]
                if colname in user_cols:
                    colstr = ''
                    for j in range(collen):
                        colstr += newline[index]
                        index += 1
                    index += 2
                    rowlist.append(colstr)

            fileheap[0][2] = rowlist
            fileheap[0][1] = toplinenum+1
        else:
            intermedsdone += 1
            fileheap = fileheap[1:]
        radix_sort2(fileheap, sorttype)
        output_file.write(line+'\n')
        intermedfile.close()

    output_file.close()


def main():
    n_args = len(sys.argv)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    memlimit = int(sys.argv[3]) * 1024 * 1024
    sorttype = sys.argv[4]
    user_cols = []
    for i in range(5, n_args):
        user_cols.append(sys.argv[i])
    limit_memory(memlimit)
    metadata = open('Metadata.txt', 'r')
    allcols = []
    colind = 0
    while True:
        col = metadata.readline()
        if not col:
            break
        col = col.strip().split(',')
        col[1] = int(col[1])
        col.append(colind)
        allcols.append(col)
        colind += 1

    #data = get_data(input_file)
    partsize = 1000
    big_merge_sort(input_file, output_file, partsize,
                   sorttype, allcols, user_cols)


if __name__ == '__main__':
    main()
