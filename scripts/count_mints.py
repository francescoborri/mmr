import csv
import sys


def count_mints(csv_path):
    counter = 0

    with open(csv_path, mode="r", encoding="utf-8") as csv_file:
        csv_iter = csv.reader(csv_file)

        col_name = "fromId"
        col_idx = None
        header = next(csv_iter, None)

        if header:
            try:
                col_idx = header.index(col_name)
            except ValueError:
                print(f"column '{col_name}' not found: {csv_path}")
                sys.exit(1)
        else:
            print("empty CSV file")
            sys.exit(1)

        for row in csv_iter:
            if len(row) > col_idx:
                if row[col_idx] == "0":
                    counter += 1

    return counter


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python %s <csv_path>" % sys.argv[0])
        sys.exit(1)
        
    print(count_mints(sys.argv[1]))
