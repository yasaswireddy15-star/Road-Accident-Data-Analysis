import matplotlib.pyplot as plt

def bar_chart(data, x, y, title, xlabel=None, ylabel="Number of recorded accidents", rotate=30):
    fig, ax = plt.subplots(figsize=(9, 4.5))
    if not data.empty:
        ax.bar(data[x].astype(str), data[y])
    ax.set_title(title)
    ax.set_xlabel(xlabel or x.replace("_", " ").title())
    ax.set_ylabel(ylabel)
    ax.tick_params(axis="x", rotation=rotate)
    fig.tight_layout()
    return fig

def line_chart(data, x, y, title):
    fig, ax = plt.subplots(figsize=(9, 4.5))
    if not data.empty:
        ax.plot(data[x].astype(str), data[y], marker="o")
    ax.set_title(title)
    ax.set_xlabel(x.replace("_", " ").title())
    ax.set_ylabel("Number of recorded accidents")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    return fig
