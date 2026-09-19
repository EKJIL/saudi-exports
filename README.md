# Has the Composition of Saudi Exports Shifted?

A time series analysis of Saudi export composition by nature of materials,
January 2015 – May 2026.

**The question:** has the composition of Saudi exports shifted from raw
materials toward manufactured goods — and if so, is it real growth or an
arithmetic side effect of falling oil exports?

📄 **[Read the report](https://rpubs.com/YOUR_USERNAME/XXXXXX)** ·
Built in R Markdown.

---

## Key findings

| | 2015 | 2025 | Change |
|---|---|---|---|
| Manufactured share | 16.5% | 29.1% | **+12.6 points** |
| Semi-manufactured share | 18.1% | 16.4% | −1.7 points |
| Raw materials share | 65.4% | 54.6% | −10.8 points |

**Every category grew in absolute terms.** Manufactured exports rose 173%
over the decade (10.6% a year compounded), against 40% for
semi-manufactured and 27% for raw materials (2.4% a year). The
compositional shift comes entirely from differential growth rates — there
was no contraction anywhere in the denominator.

- **Trend:** +0.95 percentage points a year, significant at the 1% level
  after correcting standard errors for autocorrelation (Newey-West,
  *p* = 0.0034).
- **Structure:** trend strength 0.883, seasonal strength 0.082 — the
  series is almost entirely trend, with no annual seasonality.
- **Model:** ARIMA(0,1,2) with drift, selected by AICc and confirmed by
  visual ACF/PACF identification.
- **Validation:** out-of-sample MASE 0.723 on twelve held-out months
  (below 1, so better than a naive forecast); Ljung-Box *p* = 0.64.
- **Forecast:** 36.9% by December 2030, 95% prediction interval
  27.5% – 46.3%.

---

## Repository structure

```
.
├── export-analysis.Rmd     # the analysis
├── exports_clean.csv       # aggregated monthly data
└── README.md
```

### `exports_clean.csv`

411 rows, 3 columns, UTF-8 encoded without BOM.

| Column | Type | Description |
|---|---|---|
| `category` | text | Arabic category label as published by GASTAT: `مواد خام` (raw materials), `نصف مصنعة` (semi-manufactured), `مصنعة` (manufactured) |
| `date` | date | First day of the month, `YYYY-MM-DD` |
| `value` | numeric | Export value in **millions of Saudi riyals** |

137 months × 3 categories. Category labels are kept in Arabic as they
appear in the source; the analysis maps them to English at load time.

> **Opening the file:** R, Python and pandas read it directly. Opening it
> by double-click in Excel shows mojibake — use **Data → From Text/CSV**
> with File Origin set to *65001: Unicode (UTF-8)* and Delimiter set to
> *Comma* instead.

---

## Reproducing the analysis

**Requirements:** R ≥ 4.1 (the native pipe `|>` is used) and RStudio.

```r
install.packages(c("ggplot2", "forecast", "tseries", "patchwork",
                   "sandwich", "lmtest", "kableExtra", "rmarkdown"))
```

Then:

1. Clone or download this repository.
2. Keep the `.Rmd` and `.csv` **in the same folder** — the file is read by
   a relative path.
3. Open the `.Rmd` in RStudio and click **Knit**, or run:

```r
rmarkdown::render("export-analysis.Rmd")
```

The document includes `stopifnot` guards that halt the knit if a category
label fails to match or a column goes missing, so a failure points at its
own cause rather than surfacing several sections later.

---

## Method

The analysis works with each category's **share** of monthly exports
rather than its value, because shares are invariant to any common scaling
of the three series:

```
s̃ᵢ,ₜ = λₜVᵢ,ₜ / Σⱼ λₜVⱼ,ₜ × 100 = sᵢ,ₜ
```

A rise in oil prices that lifts every category leaves the shares
unchanged, so what remains is the structure itself.

Shares carry a cost: they sum to 100 by construction, so a rise in one is
arithmetically a fall in the others and cannot by itself distinguish
growth from contraction elsewhere. The analysis therefore checks the
absolute values separately, which is what establishes that the shift is
driven by growth rather than by decline.

The pipeline:

1. **Descriptive statistics** — five-number summary, standard deviation
   and coefficient of variation for shares and values.
2. **Composition over time** — chart, 2015 vs 2025 comparison, absolute
   value check.
3. **Trend test** — OLS with Newey-West HAC standard errors.
4. **Decomposition** — STL, component strength measures (Wang, Smith &
   Hyndman), seasonality check, shock analysis.
5. **Modelling** — ADF stationarity test, ACF/PACF identification,
   `auto.arima` selection, AIC comparison against alternatives.
6. **Validation** — twelve-month out-of-sample hold-out, residual
   diagnostics.
7. **Forecast** — refit on the full series, projection to December 2030.

---

## Limitations

Stated in full in the report. In short:

1. The three shares sum to 100, so they cannot move independently. The
   absolute-value check in the report is what separates real growth from
   a denominator effect.
2. The forecast horizon (55 months) is long relative to the sample (137
   observations). Prediction intervals widen with √h.
3. An ARIMA model with drift does not know that a share is bounded by 0
   and 100. The upper limit stays at 46.3% here, so the problem does not
   bind, but a logit transform would respect the bound at any horizon.
4. The 2020 shock is absorbed into the remainder rather than modelled as
   a structural break.
5. The most recent months may be provisional. Trade statistics are
   commonly revised after first publication, and the ARIMA forecast
   anchors on the latest observations.

The model also under-forecast the held-out months (mean error +1.55
points), so the 2030 projection may be conservative.

---

## Data

Source: General Authority for Statistics (GASTAT), *International Trade
Statistics — Exports by Nature of Materials*, monthly series,
January 2015 – May 2026. Statistical Database, accessed 17 September 2026.

**`exports_clean.csv` is a modified derivative, not an official GASTAT
release.** The raw download came at transaction level (1,611,855 rows)
and was aggregated by category and month to 411 rows. Two date formats
were reconciled and values converted from text with thousand separators.
No values were imputed, adjusted or reweighted. Any error in the
aggregation is the author's, not GASTAT's.

Reused under the GASTAT Data Usage Policy, which permits copying,
distribution and derivative works provided GASTAT is acknowledged as the
source and modifications are clearly indicated.

---

## License

The **code and written analysis** in this repository are released under
the MIT License.

The **data** is reused under the GASTAT Data Usage Policy as stated above
and is not relicensed by this repository.

---

## Author

**Abdullah Adel Al-Madhi**
Statistics and Operations Research, King Saud University
