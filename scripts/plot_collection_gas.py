import pandas as pd
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import scienceplots
import locale
import sys
import os


textwidth = 5.9066
aspect_ratio = 6 / 8
scale = 1.0
width = textwidth * scale
height = width * aspect_ratio

locale.setlocale(locale.LC_ALL, "it_IT.UTF-8")
plt.style.use(["science", "grid"])
matplotlib.use("pgf")
matplotlib.rcParams.update(
    {
        "pgf.texsystem": "pdflatex",
        "font.family": "serif",
        "text.usetex": True,
        "pgf.rcfonts": False,
    }
)

MIN_GAS_MINT = 87701
MIN_GAS_VERIFY = 15000 # TODO


def plot_mint(data, ext):
    fig, ax1 = plt.subplots(figsize=(width, height))
    ax2 = ax1.twinx()

    color1 = "tab:blue"
    color2 = "tab:green"

    ax1.set_xlabel("Data")

    ax1.set_ylabel("Gas", color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)

    ax2.set_ylabel("Numero di NFT", color=color2)
    ax2.tick_params(axis="y", labelcolor=color2)

    l1 = ax1.plot(data["gas_mint"], color=color1, label="Costo di \\texttt{mint}")
    l2 = ax2.plot(data["num_tokens"], color=color2, label="NFT creati")

    bottom, top = ax1.get_ylim()
    ax2.set_ylim(bottom=bottom / MIN_GAS_MINT, top=top / MIN_GAS_MINT)

    ax1.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax1.xaxis.get_major_locator()))
    fig.autofmt_xdate()

    legend = ax2.legend(fancybox=False, edgecolor="black", handles=l1 + l2)
    legend.get_frame().set_linewidth(0.5)

    fig.savefig(f"gas_mint.{ext}")


def plot_total_mint(data, ext):
    fig, ax1 = plt.subplots(figsize=(width, height))
    ax2 = ax1.twinx()

    color1 = "tab:blue"
    color2 = "tab:green"

    ax1.set_xlabel("Data")

    ax1.set_ylabel("Gas", color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)

    ax2.set_ylabel("Numero di NFT", color=color2)
    ax2.tick_params(axis="y", labelcolor=color2)

    l1 = ax1.plot(data["total_gas_mint"], color=color1, label="Costo totale di \\texttt{mint}")
    l2 = ax2.plot(data["total_num_tokens"], color=color2, label="NFT totali")

    bottom, top = ax1.get_ylim()
    ax2.set_ylim(bottom=bottom / MIN_GAS_MINT, top=top / MIN_GAS_MINT)

    ax1.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax1.xaxis.get_major_locator()))
    fig.autofmt_xdate()

    legend = ax2.legend(fancybox=False, edgecolor="black", handles=l1 + l2, loc="upper left")
    legend.get_frame().set_linewidth(0.5)

    fig.savefig(f"total_gas_mint.{ext}")


def plot_verify(data, ext):
    fig, ax1 = plt.subplots(figsize=(width, height))
    ax2 = ax1.twinx()

    color1 = "tab:blue"
    color2 = "tab:green"

    ax1.set_xlabel("Data")

    ax1.set_ylabel("Gas", color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)

    ax2.set_ylabel("Numero di NFT", color=color2)
    ax2.tick_params(axis="y", labelcolor=color2)

    l1 = ax1.plot(data["gas_verify"], color=color1, label="Costo di \\texttt{verify}")
    l2 = ax2.plot(data["num_tokens"], color=color2, label="NFT creati")

    bottom, top = ax1.get_ylim()
    ax2.set_ylim(bottom=bottom / MIN_GAS_VERIFY, top=top / MIN_GAS_VERIFY)

    ax1.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax1.xaxis.get_major_locator()))
    fig.autofmt_xdate()

    legend = ax2.legend(fancybox=False, edgecolor="black", handles=l1 + l2)
    legend.get_frame().set_linewidth(0.5)

    fig.savefig(f"gas_verify.{ext}")


def plot_total_verify(data, ext):
    fig, ax1 = plt.subplots(figsize=(width, height))
    ax2 = ax1.twinx()

    color1 = "tab:blue"
    color2 = "tab:green"

    ax1.set_xlabel("Data")

    ax1.set_ylabel("Gas", color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)

    ax2.set_ylabel("Numero di NFT", color=color2)
    ax2.tick_params(axis="y", labelcolor=color2)

    l1 = ax1.plot(data["total_gas_verify"], color=color1, label="Costo totale di \\texttt{verify}")
    l2 = ax2.plot(data["total_num_tokens"], color=color2, label="NFT totali")

    bottom, top = ax1.get_ylim()
    ax2.set_ylim(bottom=bottom / MIN_GAS_VERIFY, top=top / MIN_GAS_VERIFY)

    ax1.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax1.xaxis.get_major_locator()))
    fig.autofmt_xdate()

    legend = ax2.legend(fancybox=False, edgecolor="black", handles=l1 + l2)
    legend.get_frame().set_linewidth(0.5)

    fig.savefig(f"total_gas_verify.{ext}")


def test(data, ext):
    fig, ax1 = plt.subplots(figsize=(width, height))
    ax2 = ax1.twinx()

    color1 = "tab:blue"
    color2 = "tab:green"

    ax1.set_xlabel("Data")

    ax1.set_ylabel("Gas", color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)

    ax2.set_ylabel("Numero di NFT", color=color2)
    ax2.tick_params(axis="y", labelcolor=color2)

    l1 = ax1.plot(data["total_gas_verify"], color=color1, label="Costo totale di \\texttt{verify}")
    # l3 = ax1.plot(data["total_gas_mint"], color="tab:red", label="Costo totale di \\texttt{mint}")
    l2 = ax2.plot(data["total_num_tokens"], color=color2, label="NFT totali")

    # bottom, top = ax1.get_ylim()
    # ax2.set_ylim(bottom=bottom / MIN_GAS_VERIFY, top=top / MIN_GAS_VERIFY)

    ax1.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax1.xaxis.get_major_locator()))
    fig.autofmt_xdate()

    legend = ax2.legend(fancybox=False, edgecolor="black", handles=l1 + l2)
    legend.get_frame().set_linewidth(0.5)

    fig.savefig(f"test.{ext}")



if __name__ == "__main__":
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("usage: python %s <gas_csv_path> <out_dir> [<ext>]" % sys.argv[0])
        sys.exit(1)

    gas_csv_path = sys.argv[1]
    out_dir = sys.argv[2]
    ext = sys.argv[3] if len(sys.argv) == 4 else "pdf"

    if ext not in ["pdf", "pgf"]:
        print("invalid extension")

    data = pd.read_csv(gas_csv_path)
    index = pd.to_datetime(data["ts"], unit="s")
    data.set_index(index, inplace=True)

    os.makedirs(out_dir, exist_ok=True)
    os.chdir(out_dir)

    # plot_mint(data, ext)
    # plot_total_mint(data, ext)
    # plot_verify(data, ext)
    # plot_total_verify(data, ext)
    test(data, ext)
