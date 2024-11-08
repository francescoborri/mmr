from datetime import datetime, timedelta
import csv
import sys
import math


def get_week_ts(ts):
    ds = datetime.fromtimestamp(ts)
    week_start = ds - timedelta(days=ds.weekday()) - timedelta(hours=ds.hour, minutes=ds.minute, seconds=ds.second)
    return math.floor(week_start.timestamp())


def get_cols_idx(header):
    idx = {}

    for pos, name in enumerate(header):
        idx[name] = pos

    return idx


def msb(num):
    return num & (1 << (num.bit_length() - 1))


def get_gas_info(gas_dict, mmr_leaves):
    if str(msb(mmr_leaves)) in gas_dict:
        return gas_dict[str(msb(mmr_leaves))]
    else:
        print(f"no gas data for mmr_leaves='{mmr_leaves}'")
        sys.exit(1)


def gas_per_leaves(gas_csv_path):
    gas_dict = {}

    with open(gas_csv_path, mode="r", encoding="utf-8") as gas_file:
        gas_iter = csv.reader(gas_file)
        gas_header = next(gas_iter, None)
        if gas_header is None:
            print(f"empty gas CSV file: {gas_csv_path}")
            sys.exit(1)

        idx = get_cols_idx(gas_header)

        for gas_row in gas_iter:
            leaves = gas_row[idx["mmr_leaves"]]
            gas_dict[leaves] = {key: int(gas_row[idx[key]]) for key in idx.keys() if key != "mmr_leaves"}

    return gas_dict


if __name__ == "__main__":
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("usage: python %s <gas_csv_path> <transfers_csv_path> [<out_csv_path>]" % sys.argv[0])
        sys.exit(1)

    gas_csv_path = sys.argv[1]
    transfers_csv_path = sys.argv[2]
    out_csv_path = sys.argv[3] if len(sys.argv) == 4 else "out.csv"

    gas_dict = gas_per_leaves(gas_csv_path)

    with open(transfers_csv_path, mode="r", encoding="utf-8") as transfers_file, open(
        out_csv_path, mode="w", encoding="utf-8"
    ) as out_file:
        transfers = csv.reader(transfers_file)
        out = csv.writer(out_file)
        out.writerow(
            [
                "week_ts",
                "mmr_height",
                "mmr_leaves",
                "num_mints",
                "num_verifies",
                "total_extra_gas_mint",
                "total_gas_verify",
                "avg_extra_gas_mint",
                "avg_gas_verify",
            ]
        )

        header = next(transfers, None)
        idx = get_cols_idx(header)
        if header is None:
            print(f"empty transfers CSV file: {transfers_csv_path}")
            sys.exit(1)

        first_mint = next(transfers, None)
        if first_mint is None:
            print(f"empty transfers CSV file: {transfers_csv_path}")
            sys.exit(1)
        elif first_mint[idx["fromId"]] != "0":
            print(f"first row in transfers CSV file should be a mint: {transfers_csv_path}")
            sys.exit(1)

        last_week = get_week_ts(int(first_mint[idx["timestamp"]]))
        mmr_leaves = 1
        num_mints = 1
        num_verifies = 0
        total_extra_gas_mint = get_gas_info(gas_dict, mmr_leaves)["extra_gas_mint"]
        total_gas_verify = 0

        for transfer_row in transfers:
            week = get_week_ts(int(transfer_row[idx["timestamp"]]))

            if week != last_week:
                gas_info = get_gas_info(gas_dict, mmr_leaves)
                out.writerow(
                    [
                        last_week,
                        gas_info["mmr_height"],
                        mmr_leaves,
                        num_mints,
                        num_verifies,
                        total_extra_gas_mint,
                        total_gas_verify,
                        total_extra_gas_mint // num_mints if num_mints > 0 else gas_info["extra_gas_mint"],
                        total_gas_verify // num_verifies if num_verifies > 0 else gas_info["gas_verify"],
                    ]
                )

                last_week = week
                num_mints = 0
                num_verifies = 0
                total_extra_gas_mint = 0
                total_gas_verify = 0

            if transfer_row[idx["fromId"]] == "0":
                mmr_leaves += 1
                num_mints += 1
                total_extra_gas_mint += get_gas_info(gas_dict, mmr_leaves)["extra_gas_mint"]
            else:
                num_verifies += 1
                total_gas_verify += get_gas_info(gas_dict, mmr_leaves)["gas_verify"]
