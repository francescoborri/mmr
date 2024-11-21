import pandas as pd
import matplotlib
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


def msb(num):
    return num & (1 << (num.bit_length() - 1))


def subplot(ylabel, title=None, log=False):
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlabel("Numero di NFT")
    ax.set_ylabel(ylabel)

    if log:
        ax.set_xscale("log")

    if title:
        fig.suptitle(title)

    return fig, ax


def save(fig, ax, filename):
    legend = ax.legend(fancybox=False, edgecolor="black", loc="center right")
    legend.get_frame().set_linewidth(0.5)
    fig.savefig(filename)


if __name__ == "__main__":
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print("usage: python %s <gas_csv_path> <ext_gas_mint_csv> <out_dir> [<ext>]" % sys.argv[0])
        sys.exit(1)

    gas_csv_path = sys.argv[1]
    ext_gas_mint_csv = sys.argv[2]
    out_dir = sys.argv[3]
    ext = sys.argv[4] if len(sys.argv) == 5 else "pdf"

    if ext not in ["pdf", "pgf"]:
        print("invalid extension")

    data = pd.read_csv(gas_csv_path)
    data.set_index(data["mmr_leaves"], inplace=True)

    mint_data = pd.read_csv(ext_gas_mint_csv)
    mint_data.index += 1
    mint_data = mint_data["gas_mint"]

    os.makedirs(out_dir, exist_ok=True)
    os.chdir(out_dir)

    fig, ax = subplot("Gas")
    ax.plot(mint_data, label="\\texttt{mint}")
    ax.plot(data["gas_verify"], label="\\texttt{verify}", drawstyle="steps")
    save(fig, ax, f"gas_mint_verify.{ext}")

    fig, ax = subplot("Gas")
    ax.plot(mint_data, label="\\texttt{mint}")
    save(fig, ax, f"gas_mint.{ext}")

    fig, ax = subplot("Gas")
    ax.plot(data["gas_verify"], label="\\texttt{verify}", drawstyle="steps")
    save(fig, ax, f"gas_verify.{ext}")

    # fig, ax = subplot("Altezza", log=True)
    # ax.plot(data["mmr_height"], label="Altezza del MMR", drawstyle="steps")
    # save(fig, ax, "mmr_height_log.pdf")
