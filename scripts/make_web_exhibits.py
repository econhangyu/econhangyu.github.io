"""Re-render the five report exhibits as web figures.

Every value, confidence interval and fit coefficient is READ FROM the exhibit CSVs
that the analysis pipeline wrote next to the print PNGs, so nothing here can change
a number -- only how it is drawn. The print PNGs in figs_v5/ are left untouched;
these outputs are for the web page only.

Why these differ from the print figures: the page's text column is about 645 css px.
Two panels side by side leave ~300 px each, which is not enough for category labels
like "Content, skills change" -- they collide with the plot. So the panels are
STACKED, each getting the full column width.

Design (per the data-viz method):
  * Colour does two jobs, never mixed inside a panel.
      identity  -- Students = orange, Workers = blue  (categorical slots 2 and 1)
      polarity  -- gain/toward = blue, loss/away/worry = red  (the diverging pair)
    Both pairs pass the six checks on the light surface (worst CVD dE 24.7 and 21.6,
    normal-vision 33.6 and 32.3, all >= 3:1 contrast).
  * Text always wears ink tokens, never the series colour.
  * Every panel carries its own legend, placed in the gap between title and plot so
    it can never overlap the data.
  * Thin marks, hairline solid grid, no frames, generous padding.
  * SVG with text converted to paths, so the type is crisp at any zoom and renders
    identically everywhere regardless of which fonts the reader has.

Usage:  python3 scripts/make_web_exhibits.py
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

SRC = ("/Users/hangyu/Library/CloudStorage/Dropbox/Topic Explore/AI diffusion impact/"
       "mywork/pilot_analysis/report/figs_v5")
OUT = ("/Users/hangyu/Library/CloudStorage/Dropbox/_professional documents/website/"
       "images/reports/ai-perception")

BLUE, ORANGE, RED = "#2a78d6", "#eb6834", "#e34948"
STUDENT, WORKER = ORANGE, BLUE
INK, INK2, MUTED = "#1a1a1a", "#4a4a48", "#7a7a75"
GRID = "#e6e6e2"

WIDTH = 9.0          # inches; the page renders it about 645 css px wide, so 1pt ~ 1px
FS_TITLE, FS_TICK, FS_AXIS, FS_LEG, FS_VAL, FS_NOTE = 13.5, 11.5, 12, 11.5, 11, 11
TITLE_PAD = 30       # leaves a clear band under the title for that panel's legend


def style():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "svg.fonttype": "path",       # bake glyphs so readers' fonts cannot shift the layout
        "figure.facecolor": "none",
        "axes.facecolor": "none",
        "text.color": INK,
        "axes.labelcolor": INK2,
        "xtick.color": INK2,
        "ytick.color": INK2,
        "axes.edgecolor": GRID,
        "axes.linewidth": 0.8,
        "xtick.labelsize": FS_TICK,
        "ytick.labelsize": FS_TICK,
        "axes.labelsize": FS_AXIS,
        "legend.fontsize": FS_LEG,
        "xtick.major.size": 0,
        "ytick.major.size": 0,
        "axes.grid": False,
    })


def panel(ax, title, xgrid=False, ygrid=False, pad=TITLE_PAD):
    """Title, a stripped frame, and one direction of hairline grid.

    `pad` must clear the panel's legend: ~30pt for a one-row legend, ~48 for two.
    """
    ax.set_title(title, fontsize=FS_TITLE, color=INK, fontweight="600",
                 loc="left", pad=pad)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.set_axisbelow(True)
    if xgrid:
        ax.xaxis.grid(True, color=GRID, linewidth=0.8, linestyle="-")
        ax.spines["left"].set_visible(False)
    if ygrid:
        ax.yaxis.grid(True, color=GRID, linewidth=0.8, linestyle="-")
        ax.spines["left"].set_visible(False)


def legend(ax, handles, labels, ncol=None):
    """Sit the legend in the band the title pad reserved -- never over the data."""
    ax.legend(handles, labels, loc="lower left", bbox_to_anchor=(0, 1.005),
              ncol=ncol or len(labels), frameon=False, fontsize=FS_LEG,
              handlelength=1.5, handletextpad=0.55, columnspacing=1.6,
              borderpad=0, labelcolor=INK2)


def swatch(colour):
    return plt.Rectangle((0, 0), 1, 1, color=colour)


def dot(colour, marker="o"):
    return Line2D([], [], color=colour, marker=marker, ms=8, lw=0,
                  markeredgecolor="white", markeredgewidth=1.4)


def line_dot(colour, dash="-"):
    return Line2D([], [], color=colour, lw=2.4, ls=dash, marker="o", ms=7,
                  markeredgecolor="white", markeredgewidth=1.2)


def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name + ".svg")
    fig.savefig(path, format="svg", bbox_inches="tight", pad_inches=0.06,
                transparent=True)
    plt.close(fig)
    print(f"  {name}.svg  {os.path.getsize(path)/1024:.0f} KB")


def load(stem):
    return pd.read_csv(os.path.join(SRC, stem + ".csv"))


def label_right(ax, x, y, value):
    """Value label clear of the whisker: anchored at the CI's upper end."""
    ax.annotate(f"{value:.0f}", (x, y), textcoords="offset points", xytext=(7, 0),
                ha="left", va="center", fontsize=FS_VAL, color=MUTED)


def label_outward(ax, y, a, b):
    """Two marks share a row -- label each on the side away from the other."""
    lo, hi = (a, b) if a["value"] <= b["value"] else (b, a)
    ax.annotate(f"{lo['value']:.0f}", (lo["ci_lo"], y), textcoords="offset points",
                xytext=(-7, 0), ha="right", va="center", fontsize=FS_VAL, color=MUTED)
    label_right(ax, hi["ci_hi"], y, hi["value"])


def blocks(n, per=2, gap=0.7):
    """Row positions, top to bottom, with a gap between every block of `per` rows."""
    pos, p = [], 0.0
    for i in range(n):
        if i and i % per == 0:
            p += gap
        pos.append(p)
        p += 1.0
    pos = np.array(pos)
    return pos.max() - pos


# --------------------------------------------------------------------- exhibit 1
def exhibit1():
    d = load("exhibit1_expectations")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(WIDTH, 7.0),
                                   gridspec_kw={"height_ratios": [1, 1.15], "hspace": 0.62})

    # Panel A -- replacement chance across horizons, plus the 5-year task share
    a = d[d.panel == "A"]
    chance, share = a[a.series.str.startswith("chance")], a[a.series.str.startswith("share")]
    x = np.arange(3)
    for samp, colour, dy in [("student", STUDENT, 8), ("worker", WORKER, -12)]:
        s = chance[chance["sample"] == samp].set_index("horizon").loc[["1yr", "5yr", "10yr"]]
        ax1.errorbar(x, s.value, yerr=[s.value - s.ci_lo, s.ci_hi - s.value],
                     color=colour, lw=2.2, marker="o", ms=7, capsize=0, elinewidth=1.3,
                     zorder=3, markeredgecolor="white", markeredgewidth=1.2)
        ax1.annotate(f"{s.value.iloc[-1]:.0f}", (x[-1], s.value.iloc[-1]),
                     textcoords="offset points", xytext=(10, dy),
                     fontsize=FS_VAL, color=MUTED)
        t = share[share["sample"] == samp].iloc[0]
        dx = -0.05 if samp == "student" else 0.05
        ax1.errorbar([1 + dx], [t.value], yerr=[[t.value - t.ci_lo], [t.ci_hi - t.value]],
                     color=colour, marker="D", ms=7, capsize=0, elinewidth=1.3, lw=0,
                     zorder=3, markeredgecolor="white", markeredgewidth=1.2)
        ax1.annotate(f"{t.value:.0f}", (1 + dx, t.value), textcoords="offset points",
                     xytext=(-22 if samp == "student" else 12, -4),
                     fontsize=FS_VAL, color=MUTED)
    ax1.set_xticks(x)
    ax1.set_xticklabels(["1 yr", "5 yrs", "10 yrs"])
    ax1.set_xlim(-0.2, 2.3)
    ax1.set_ylim(0, 62)
    ax1.set_yticks([0, 20, 40, 60])
    ax1.set_ylabel("Percent")
    panel(ax1, "A. Expected task share and replacement chance", ygrid=True)
    legend(ax1, [line_dot(STUDENT), line_dot(WORKER), dot(MUTED), dot(MUTED, "D")],
           ["Students", "Workers", "Chance the job is replaced", "Tasks AI could do in 5 yrs"])

    # Panel B -- what the job looks like in five years
    b = d[d.panel == "B"]
    cats = ["Content, skills change", "AI assists, work same", "New tasks appear",
            "Mostly replaced by AI", "Unimaginable change", "No change"]
    y = np.arange(len(cats))[::-1]
    h = 0.38
    for samp, colour, off in [("student", STUDENT, h / 2), ("worker", WORKER, -h / 2)]:
        s = b[b["sample"] == samp].set_index("horizon").loc[cats]
        ax2.barh(y + off, s.value, height=h - 0.05, color=colour, zorder=3)
        for yy, vv in zip(y + off, s.value):
            ax2.annotate(f"{vv:.0f}", (vv, yy), textcoords="offset points", xytext=(6, 0),
                         va="center", fontsize=FS_VAL, color=MUTED)
    ax2.set_yticks(y)
    ax2.set_yticklabels(cats)
    ax2.set_xlim(0, 40)
    ax2.set_xlabel("Share of respondents (%)")
    panel(ax2, "B. What the job looks like in five years", xgrid=True)
    legend(ax2, [swatch(STUDENT), swatch(WORKER)], ["Students", "Workers"])
    save(fig, "exhibit1_expectations")


# --------------------------------------------------------------------- exhibit 2
def exhibit2():
    d = load("exhibit2_gain_lose")
    groups = ["Students", "All workers",
              "Workers: AI at work less than daily", "Workers: AI at work daily or more"]
    shown = ["Students", "All workers",
             "Workers: AI at work\nless than daily", "Workers: AI at work\ndaily or more"]
    y = np.arange(len(groups))[::-1]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(WIDTH, 7.0),
                                   gridspec_kw={"height_ratios": [1.15, 1], "hspace": 0.55})

    # Panel A -- expected direction of own income
    a = d[d.panel == "A"]
    h = 0.38
    for meas, colour, off in [("expects own income to rise (%)", BLUE, h / 2),
                              ("expects own income to fall (%)", RED, -h / 2)]:
        s = a[a.measure == meas].set_index("group").loc[groups]
        ax1.barh(y + off, s.value, height=h - 0.05, color=colour, zorder=3)
        ax1.errorbar(s.value, y + off, xerr=[s.value - s.ci_lo, s.ci_hi - s.value],
                     fmt="none", ecolor=MUTED, elinewidth=1.1, capsize=0, zorder=4)
        for yy, vv, hi in zip(y + off, s.value, s.ci_hi):
            label_right(ax1, hi, yy, vv)
    ax1.set_yticks(y)
    ax1.set_yticklabels(shown)
    ax1.set_xlim(0, 60)
    ax1.set_xlabel("Share of respondents (%)")
    panel(ax1, "A. Own income in five years: expects a rise or a fall", xgrid=True)
    legend(ax1, [swatch(BLUE), swatch(RED)], ["Income will rise", "Income will fall"])

    # Panel B -- worry. One series, so the title names it and no legend is needed.
    b = d[d.panel == "B"].set_index("group").loc[groups]
    ax2.barh(y, b.value, height=0.44, color=RED, zorder=3)
    ax2.errorbar(b.value, y, xerr=[b.value - b.ci_lo, b.ci_hi - b.value],
                 fmt="none", ecolor=MUTED, elinewidth=1.1, capsize=0, zorder=4)
    for yy, vv, hi in zip(y, b.value, b.ci_hi):
        label_right(ax2, hi, yy, vv)
    ax2.set_yticks(y)
    ax2.set_yticklabels(shown)
    ax2.set_xlim(0, 85)
    ax2.set_xlabel("Share at least somewhat worried (%)")
    panel(ax2, "B. Worried about AI and own job", xgrid=True)
    save(fig, "exhibit2_gain_lose")


# --------------------------------------------------------------------- exhibit 3
def exhibit3():
    d = load("exhibit3_what_they_do")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(WIDTH, 8.2),
                                   gridspec_kw={"height_ratios": [1, 1.9], "hspace": 0.42})

    # Panel A -- direction of the search, by sample
    a = d[d.panel == "A"]
    keys = ["Toward AI-related work", "Away from AI-exposed work", "No change / not sure"]
    y = np.arange(3)[::-1]
    h = 0.36
    for samp, colour, off in [("student", STUDENT, h / 2), ("worker", WORKER, -h / 2)]:
        s = a[a["sample"] == samp].set_index("group").loc[keys]
        ax1.barh(y + off, s.value, height=h - 0.05, color=colour, zorder=3)
        for yy, vv in zip(y + off, s.value):
            ax1.annotate(f"{vv:.0f}", (vv, yy), textcoords="offset points", xytext=(6, 0),
                         va="center", fontsize=FS_VAL, color=MUTED)
    ax1.set_yticks(y)
    ax1.set_yticklabels(keys)
    ax1.set_xlim(0, 48)
    ax1.set_xlabel("Share of own sample (%)")
    panel(ax1, "A. Direction of the job search, by sample", xgrid=True)
    legend(ax1, [swatch(STUDENT), swatch(WORKER)], ["Students", "Workers"])

    # Panel B -- direction by belief, samples pooled
    b = d[d.panel == "B"]
    rows = ["AI does little now", "AI does a lot now",
            "Not worried", "Worried",
            "Expects income to rise: no", "Expects income to rise: yes",
            "Expects income to fall: no", "Expects income to fall: yes"]
    ypos = blocks(len(rows))
    toward = b[b.measure == "moved toward AI work (%)"].set_index("group").loc[rows]
    away = b[b.measure == "moved away from AI-exposed work (%)"].set_index("group").loc[rows]
    for s, colour in [(toward, BLUE), (away, RED)]:
        ax2.errorbar(s.value, ypos, xerr=[s.value - s.ci_lo, s.ci_hi - s.value],
                     fmt="o", ms=8, color=colour, elinewidth=1.4, capsize=0, zorder=3,
                     markeredgecolor="white", markeredgewidth=1.6)
    for yy, key in zip(ypos, rows):
        label_outward(ax2, yy, toward.loc[key], away.loc[key])
    ax2.set_yticks(ypos)
    ax2.set_yticklabels(rows)
    ax2.set_ylim(-0.7, ypos.max() + 0.7)
    ax2.set_xlim(14, 62)
    ax2.set_xlabel("Share of respondents (%)")
    panel(ax2, "B. Direction by belief, samples pooled", xgrid=True)
    legend(ax2, [dot(BLUE), dot(RED)],
           ["Moved toward AI-related work", "Moved away from AI-exposed work"])
    save(fig, "exhibit3_what_they_do")


# --------------------------------------------------------------------- exhibit 4
def exhibit4():
    d = load("exhibit4_retraining")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(WIDTH, 8.4),
                                   gridspec_kw={"height_ratios": [1, 1.55], "hspace": 0.5})

    # Panel A -- the demand curve. Hue carries the sample and dash the cash split,
    # so four lines need only two hues.
    a = d[d.panel == "A"]
    x = np.arange(3)
    # dy staggers the ¥300 labels: the students-overall and could-raise lines pass
    # within 7 points of each other there, so their labels go opposite ways.
    series = [("worker", "overall", WORKER, "-", "Workers", 11),
              ("student", "overall", STUDENT, "-", "Students", -19),
              ("student", "could raise ¥5,000", STUDENT, (0, (5, 2)),
               "Students: could raise ¥5,000", 11),
              ("student", "could not easily raise ¥5,000", STUDENT, (0, (1.5, 1.8)),
               "Students: could not easily raise ¥5,000", -19)]
    handles, labels = [], []
    for samp, grp, colour, dash, label, dy in series:
        s = a[(a["sample"] == samp) & (a.group == grp)].set_index("price").loc[[0, 300, 800]]
        ax1.plot(x, s.value, color=colour, lw=2.2, ls=dash, marker="o", ms=7,
                 markeredgecolor="white", markeredgewidth=1.2, zorder=3)
        ax1.annotate(f"{s.value.loc[300]:.0f}", (1, s.value.loc[300]),
                     textcoords="offset points", xytext=(0, dy), ha="center",
                     fontsize=FS_VAL, color=MUTED)
        handles.append(line_dot(colour, dash))
        labels.append(label)
    ax1.set_xticks(x)
    ax1.set_xticklabels(["Free", "¥300", "¥800"])
    ax1.set_xlim(-0.15, 2.2)
    ax1.set_ylim(0, 105)
    ax1.set_yticks([0, 25, 50, 75, 100])
    ax1.set_ylabel("Would enroll (%)")
    panel(ax1, "A. Would enroll in a 20-hour AI course, by price", ygrid=True, pad=50)
    legend(ax1, handles, labels, ncol=2)

    # Panel B -- who stays in at ¥300
    b = d[d.panel == "B"]
    rows = ["AI already does a lot of my job", "AI already does little",
            "Replacement chance, top third", "Replacement chance, bottom third",
            "Worried", "Not worried",
            "Could raise ¥5,000", "Could not easily raise ¥5,000"]
    ypos = blocks(len(rows))
    # the caption states this split is not shown for workers -- only 18 of them are
    # cash-constrained, so the estimate is far too noisy to plot
    hide_for_workers = {"Could not easily raise ¥5,000"}
    stu = b[b["sample"] == "student"].set_index("group")
    wrk = b[(b["sample"] == "worker") & (~b.group.isin(hide_for_workers))].set_index("group")
    for s, colour in [(stu, STUDENT), (wrk, WORKER)]:
        r = s.loc[[k for k in rows if k in s.index]]
        yy = [y for y, k in zip(ypos, rows) if k in s.index]
        ax2.errorbar(r.value, yy, xerr=[r.value - r.ci_lo, r.ci_hi - r.value],
                     fmt="o", ms=8, color=colour, elinewidth=1.4, capsize=0, zorder=3,
                     markeredgecolor="white", markeredgewidth=1.6)
    for yy, key in zip(ypos, rows):
        if key in wrk.index:
            label_outward(ax2, yy, stu.loc[key], wrk.loc[key])
        else:                     # workers who cannot raise ¥5,000: only 18, not shown
            label_right(ax2, stu.loc[key].ci_hi, yy, stu.loc[key].value)
    ax2.set_yticks(ypos)
    ax2.set_yticklabels(rows)
    ax2.set_ylim(-0.7, ypos.max() + 0.7)
    ax2.set_xlim(8, 94)
    ax2.set_xlabel("Would enroll at ¥300 (%)")
    panel(ax2, "B. Enrollment at ¥300, by belief and by cash on hand", xgrid=True)
    legend(ax2, [dot(STUDENT), dot(WORKER)], ["Students", "Workers"])
    save(fig, "exhibit4_retraining")


# --------------------------------------------------------------------- exhibit 5
def exhibit5():
    d = load("exhibit5_experience")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(WIDTH, 7.2),
                                   gridspec_kw={"hspace": 0.62})
    ylab = "Chance own job is replaced\nwithin 5 years (%)"

    # Panel A -- by how much AI already does in the job
    a = d[(d.panel == "A") & (d.measure.str.startswith("C0"))]
    x = np.arange(3)
    for samp, colour, dy in [("student", STUDENT, 9), ("worker", WORKER, -14)]:
        s = a[a["sample"] == samp].sort_values("bin")
        ax1.errorbar(x, s.value, yerr=1.96 * s.se.to_numpy(), color=colour, lw=2.2,
                     marker="o", ms=7, capsize=0, elinewidth=1.3, zorder=3,
                     markeredgecolor="white", markeredgewidth=1.2)
        ax1.annotate(f"{s.value.iloc[-1]:.0f}", (x[-1], s.value.iloc[-1]),
                     textcoords="offset points", xytext=(10, dy), fontsize=FS_VAL, color=MUTED)
    r = d[(d.panel == "A") & (d.measure == "individual correlation")].set_index("sample")
    ax1.text(0.985, 0.06, f"Students  r = {r.loc['student'].value:+.2f}\n"
                          f"Workers   r = {r.loc['worker'].value:+.2f}",
             transform=ax1.transAxes, ha="right", va="bottom",
             fontsize=FS_NOTE, color=MUTED, linespacing=1.5)
    ax1.set_xticks(x)
    ax1.set_xticklabels(["none or a few tasks", "a sizable part", "most tasks"])
    ax1.set_xlim(-0.2, 2.3)
    ax1.set_ylim(18, 56)
    ax1.set_xlabel("How much of my job AI already does")
    ax1.set_ylabel(ylab)
    panel(ax1, "A. By how much AI already does in the job", ygrid=True)
    legend(ax1, [line_dot(STUDENT), line_dot(WORKER)], ["Students", "Workers"])

    # Panel B -- by the occupation's exposure score, with the individual-level fit
    b = d[(d.panel == "B") & (d.measure.str.startswith("Eloundou"))]
    sl = d[(d.panel == "B") & (d.measure.str.startswith("OLS"))].set_index("sample")
    for samp, colour in [("student", STUDENT), ("worker", WORKER)]:
        s = b[b["sample"] == samp].sort_values("bin")
        ax2.errorbar(s.bin_x_z, s.value, yerr=[s.value - s.ci_lo, s.ci_hi - s.value],
                     fmt="o", ms=7, color=colour, elinewidth=1.3, capsize=0, lw=0,
                     zorder=3, markeredgecolor="white", markeredgewidth=1.2)
        xs = np.array([s.bin_x_z.min() - 0.15, s.bin_x_z.max() + 0.15])
        ax2.plot(xs, s.intercept.iloc[0] + s.slope_per_sd.iloc[0] * xs,
                 color=colour, lw=1.9, zorder=2)
    ax2.text(0.985, 0.06, f"Students  {sl.loc['student'].value:+.1f} per SD\n"
                          f"Workers   {sl.loc['worker'].value:+.1f} per SD",
             transform=ax2.transAxes, ha="right", va="bottom",
             fontsize=FS_NOTE, color=MUTED, linespacing=1.5)
    ax2.set_ylim(18, 56)
    ax2.set_xlabel("Occupation's Eloundou exposure score (SDs from the sample mean)")
    ax2.set_ylabel(ylab)
    panel(ax2, "B. By the occupation's Eloundou exposure score", ygrid=True)
    legend(ax2, [dot(STUDENT), dot(WORKER)], ["Students", "Workers"])
    save(fig, "exhibit5_experience")


if __name__ == "__main__":
    style()
    print("writing web exhibits to", OUT)
    for fn in (exhibit1, exhibit2, exhibit3, exhibit4, exhibit5):
        fn()
