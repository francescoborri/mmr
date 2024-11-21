import pandas as pd
from datetime import datetime, timedelta
import sys
import math


def day_of(ts):
    ds = datetime.fromtimestamp(ts)
    return math.floor(ds.replace(hour=0, minute=0, second=0).timestamp())


def week_of(ts):
    ds = datetime.fromtimestamp(ts)
    week_start = ds - timedelta(days=ds.weekday()) - timedelta(hours=ds.hour, minutes=ds.minute, seconds=ds.second)
    return math.floor(week_start.timestamp())


def round_period(ts):
    return week_of(ts)


def msb(num):
    return num & (1 << (num.bit_length() - 1))


def get_gas(gas_data, num_tokens):
    return gas_data.loc[msb(num_tokens)]


if __name__ == "__main__":
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print("usage: python %s <gas_csv_path> <ext_gas_mint_csv> <transfers_csv_path> [<out_csv_path>]" % sys.argv[0])
        sys.exit(1)

    gas_csv_path = sys.argv[1]
    ext_gas_mint_csv = sys.argv[2]
    transfers_csv_path = sys.argv[3]
    out_csv_path = sys.argv[4] if len(sys.argv) == 5 else "out.csv"

    gas_data = pd.read_csv(gas_csv_path)
    gas_data.set_index(gas_data["mmr_leaves"], inplace=True)

    mint_data = pd.read_csv(ext_gas_mint_csv)
    mint_data.index += 1
    mint_data = mint_data["gas_mint"]

    transfers_data = pd.read_csv(transfers_csv_path)
    result = pd.DataFrame(
        columns=[
            "ts",
            "mmr_height",
            "num_tokens",
            "num_transfers",
            "total_num_tokens",
            "total_num_transfers",
            "gas_mint",
            "gas_verify",
            "total_gas_mint",
            "total_gas_verify",
        ]
    )

    first_transfer = transfers_data.iloc[0]
    if first_transfer["fromId"] != 0:
        print(f"first row in transfers CSV file should be a mint: {transfers_csv_path}")
        sys.exit(1)

    last_period = round_period(first_transfer["timestamp"])
    num_tokens = 1
    num_transfers = 0
    total_num_tokens = 1
    total_num_transfers = 0
    gas_mint = mint_data[total_num_tokens]
    gas_verify = 0
    total_gas_mint = mint_data[total_num_tokens]
    total_gas_verify = 0

    iter_transfers = transfers_data.iterrows()
    next(iter_transfers)

    for _, transfer in iter_transfers:
        period = round_period(transfer["timestamp"])

        if period != last_period:
            result.loc[len(result)] = [
                last_period,
                get_gas(gas_data, total_num_tokens)["mmr_height"],
                num_tokens,
                num_transfers,
                total_num_tokens,
                total_num_transfers,
                gas_mint,
                gas_verify,
                total_gas_mint,
                total_gas_verify,
            ]
            last_period = period
            num_tokens = 0
            num_transfers = 0
            gas_mint = 0
            gas_verify = 0

        if transfer["fromId"] == 0:
            num_tokens += 1
            total_num_tokens += 1

            gas = mint_data[total_num_tokens]
            gas_mint += gas
            total_gas_mint += gas
        elif transfer["toId"] != 0:
            num_transfers += 1
            total_num_transfers += 1

            gas = get_gas(gas_data, total_num_tokens)["gas_verify"]
            gas_verify += gas
            total_gas_verify += gas

    result.loc[len(result)] = [
        last_period,
        get_gas(gas_data, total_num_tokens)["mmr_height"],
        num_tokens,
        num_transfers,
        total_num_tokens,
        total_num_transfers,
        gas_mint,
        gas_verify,
        total_gas_mint,
        total_gas_verify,
    ]

    result.to_csv(out_csv_path, index=False)
