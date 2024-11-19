import csv
import sys


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python %s <csv_path>" % sys.argv[0])
        sys.exit(1)

    csv_path = sys.argv[1]
    mints = 0
    transfers = 0

    with open(csv_path, mode="r", encoding="utf-8") as csv_file:
        csv_iter = csv.reader(csv_file)

        fromId_col = None
        toId_col = None
        header = next(csv_iter, None)

        if header:
            try:
                fromId_col = header.index("fromId")
                toId_col = header.index("toId")
            except ValueError:
                print(f"column not found: {csv_path}")
                sys.exit(1)
        else:
            print("empty CSV file")
            sys.exit(1)

        for row in csv_iter:
            if len(row) > fromId_col:
                if row[fromId_col] == "0" and row[toId_col] != "0":
                    mints += 1
                if row[fromId_col] != "0" and row[toId_col] != "0":
                    transfers += 1

    print(f"mints: {mints}")
    print(f"transfers: {transfers}")
