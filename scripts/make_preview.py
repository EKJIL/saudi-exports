# Builds preview.png: the link-preview image LinkedIn shows (1200x627).
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

for f in font_manager.findSystemFonts():
    if "Inter" in f:
        font_manager.fontManager.addfont(f)
plt.rcParams["font.family"] = "Inter"

df = pd.read_csv("exports_clean.csv", parse_dates=["date"])
tot = df.groupby("date")["value"].sum()
man = df[df["category"] == "مصنعة"].set_index("date")["value"]
share = (man / tot * 100).sort_index()
yearly = share.groupby(share.index.year).mean()

BG, INK, INK2, BLUE, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#2a78d6", "#e6e5e1"
fig = plt.figure(figsize=(12, 6.27), dpi=100, facecolor=BG)
fig.text(0.05, 0.88, "Has the composition of Saudi exports shifted?",
         fontsize=30, fontweight="bold", color=INK)
fig.text(0.05, 0.81, "Manufactured goods' share of monthly exports, Jan 2015 – May 2026",
         fontsize=16, color=INK2)

ax = fig.add_axes([0.07, 0.13, 0.57, 0.6], facecolor=BG)
ax.plot(share.index, share.values, color=BLUE, lw=2)
ax.set_ylim(0, 40)
ax.set_yticks([0, 10, 20, 30, 40])
ax.set_yticklabels([f"{v}%" for v in [0, 10, 20, 30, 40]])
ax.grid(axis="y", color=GRID, lw=1)
for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(colors=INK2, labelsize=13, length=0)

fig.text(0.69, 0.62, f"{yearly[2015]:.1f}% → {yearly[2025]:.1f}%",
         fontsize=28, fontweight="bold", color=INK)
fig.text(0.69, 0.56, "manufactured share, 2015 → 2025", fontsize=14, color=INK2)
fig.text(0.69, 0.42, "+0.95 pts / year", fontsize=24, fontweight="bold", color=INK)
fig.text(0.69, 0.37, "trend, Newey-West p = 0.003", fontsize=14, color=INK2)
fig.text(0.69, 0.23, "36.9% by 2030", fontsize=24, fontweight="bold", color=INK)
fig.text(0.69, 0.18, "ARIMA(0,1,2) forecast", fontsize=14, color=INK2)
fig.text(0.05, 0.035, "Data: GASTAT  ·  Analysis in R  ·  Abdullah Adel Al-Madhi",
         fontsize=12, color=INK2)
fig.savefig("preview.png", facecolor=BG)
