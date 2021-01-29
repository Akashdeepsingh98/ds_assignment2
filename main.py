import resource
import sys


def main():
    n_args = len(sys.argv)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    memlimit = int(sys.argv[3])
    sorttype = sys.argv[4]
    user_cols = []
    for i in range(5, n_args):
        user_cols.append(sys.argv[i])


if __name__ == '__main__':
    main()
