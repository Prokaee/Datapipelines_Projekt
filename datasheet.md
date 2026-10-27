# Datasheet for Dataset: U.S. Stock Market & Macroeconomic Valuation (Shiller Data)

This datasheet provides technical documentation for the historical financial and macroeconomic time-series dataset utilized in the project. For this, the long-term U.S. stock market dataset (`ie_data.xls`, hosted at Yale University and ShillerData.com), spanning monthly observations from January 1871 to 2026, as well as the cleaned version after preprocessing are described. Following the standardized question framework of Gebru et al. (2021), the datasheet details the dataset's motivation, composition, collection methodology, preprocessing transformations, intended uses, distribution terms, and ongoing maintenance:

---

## 1. Motivation

### For what purpose was the dataset created? Was there a specific task in mind? Was there a specific gap that needed to be filled?
* **Upstream Primary Dataset (Robert J. Shiller):** The original dataset was assembled by Professor Robert J. Shiller (Yale University, 2013 Nobel Laureate in Economic Sciences) to facilitate empirical research into the long-horizon behavior of the aggregate U.S. stock market, speculative price bubbles, excess market volatility, and equity risk premia. Prior to Shiller's work, standard financial market databases commenced only in December 1925, omitting more than half a century of crucial macroeconomic regime shifts. Shiller created this dataset to provide an unbroken, monthly historical record combining stock prices, corporate dividends, trailing earnings, consumer price inflation (CPI), and long-term interest rates starting in January 1871. This dataset famously enabled the development of the Cyclically Adjusted Price-to-Earnings (CAPE) ratio presented in Campbell and Shiller (1988, 1998) and Shiller's book *Irrational Exuberance* (2000, 2005, 2015).
* **Preprocessed Project Version:** The dataset was retrieved and systematically processed to evaluate whether valuation ratios (P/E, CAPE), momentum indicators (6M, 12M), rolling annualized volatility regimes, and historical drawdown depths can accurately forecast 1-year, 5-year, and 10-year forward real equity returns. Furthermore, it serves to empirically test retail market-timing heuristics (e.g., holding cash to "wait for market crashes") against continuous buy-and-hold investing, and analyze the impact of return skewness and volatility drag over secular investment horizons.

### Who created the dataset (e.g., which team, research group) and on behalf of which entity (e.g., company, institution, organization)?
* **Upstream Primary Dataset:** Created and curated by **Professor Robert J. Shiller** and his academic research team at **Yale University** (Department of Economics and the Cowles Foundation for Research in Economics), New Haven, Connecticut, USA.
* **Preprocessed Project Version:** The data extraction, date parsing correction, look-ahead bias mitigation, feature engineering, and forward target calculation were implemented by **Raphael Erler, Richard Zallinger, and Michael Prokop** for this project.

### Who funded the creation of the dataset? If there is an associated grant, please provide the name of the grantor and the grant name and number.
* **Upstream Primary Dataset:** Professor Shiller's historical market data compilation has been supported over several decades by academic research grants from the **Cowles Foundation for Research in Economics at Yale University** and grants from the **U.S. National Science Foundation (NSF)**. No commercial or corporate sponsors funded or restricted the dataset.
* **Preprocessed Project Version:** Conducted as non-commercial academic coursework. No external grants or sponsors were involved.

---

## 2. Composition

### What do the instances that comprise the dataset represent (e.g., documents, photos, people, countries)? Are there multiple types of instances?
Each instance (row) represents a single, discrete calendar month of aggregated macroeconomic, market-wide financial observations and derived econometric indicators for the United States economy. There is exactly one instance type: uniform monthly time-series observations.

### How many instances are there in total (of each type, if appropriate)?
* **Upstream Primary Dataset:** Contains 1,870 monthly observation rows spanning January 1871 (`1871.01`) through October 2026 (`2026.10`), followed by a metadata/footer row.
* **Preprocessed Project Version:** Exactly 1,866 monthly instances, spanning unbroken from January 1, 1871 (`1871-01-01`) to June 1, 2026 (`2026-06-01`), comprising 155.5 years of economic history. The final 4 incomplete months (July–October 2026) were removed due to pending quarterly corporate earnings publications.

### Does the dataset contain all possible instances or is it a sample of instances from a larger set?
* **Temporal Coverage:** The dataset contains the complete, unbroken sequence of all 1,866 consecutive calendar months over the 155.5-year span. There are no omitted calendar months or temporal gaps between 1871-01-01 and 2026-06-01.
* **Market Universe:** It is not a global sample; it specifically represents the aggregate large-cap U.S. public equity market. Before March 1957, the market is represented by historical aggregations (the Standard & Poor's 90-stock index from 1926–1957, and Cowles Commission retrospective common stock indices from 1871–1925). From March 1957 onwards, it represents the Standard & Poor's 500 Composite Index (S&P 500), which encompasses approximately 80–85% of total U.S. equity market capitalization.
* **Intra-Month Sampling:** Price observations ($P$) represent the arithmetic average of daily closing prices during the calendar month, rather than instantaneous month-end closing prices.

### What data does each instance consist of? "Raw" data or features?
Each instance consists of 20 continuous numerical attributes (plus a primary datetime index):
1. **Raw / Base Macroeconomic Variables (from `ie_data.xls`):**
   * `P` (*float64*): S&P Composite Index nominal price (monthly average of daily closing prices). Range: [2.73, 7,450.03].
   * `D` (*float64*): Nominal dividends per share, expressed as a 12-month trailing moving total. Range: [0.18, 81.70].
   * `E` (*float64*): Nominal corporate earnings per share, expressed as a 12-month trailing moving total. Range: [0.16, 295.39].
   * `CPI` (*float64*): Consumer Price Index (base: 1982–1984 = 100), combining the BLS CPI-U with the historical Warren-Pearson index. Range: [6.28, 335.12].
   * `GS10` (*float64*): Long-term U.S. government bond yield (10-year Treasury constant maturity rate, in percent per annum). Range: [0.62%, 15.32%].
2. **Point-in-Time Lagged Fundamentals:**
   * `E_lag` (*float64*): Corporate earnings lagged backward by 3 months ($E_{t-3}$) to reflect real-world SEC filing disclosure delays.
   * `D_lag` (*float64*): Corporate dividends lagged backward by 3 months ($D_{t-3}$).
3. **Inflation-Adjusted & Total Return Series:**
   * `P_real` (*float64*): Real (inflation-adjusted) stock price, normalized to the purchasing power of the terminal month (June 2026 dollars): $P_t \cdot \frac{CPI_{\text{June 2026}}}{CPI_t}$.
   * `ret_real` (*float64*): Monthly net real total return, factoring in real capital gains and reinvested monthly dividends: $r_t = \frac{P_t + D_t/12}{P_{t-1}} \cdot \frac{CPI_{t-1}}{CPI_t} - 1$.
   * `tr_index` (*float64*): Cumulative real total return wealth index ($TR_t = \prod_{\tau=1}^t (1 + r_\tau)$), normalized to $TR_0 = 1.0$ at 1871-01-01. Compounded value at 2026-06-01: 42,719.71.
4. **Predictive Features:**
   * `mom_6m` (*float64*): Trailing 6-month real total return momentum: $\frac{TR_t}{TR_{t-6}} - 1$.
   * `mom_12m` (*float64*): Trailing 12-month real total return momentum: $\frac{TR_t}{TR_{t-12}} - 1$.
   * `vol_12m` (*float64*): Trailing 12-month rolling annualized return volatility: $\text{std}(r_{t-11..t}) \cdot \sqrt{12}$.
   * `pe` (*float64*): Trailing Price-to-Earnings ratio using point-in-time lagged earnings: $\frac{P_t}{E_{t-3}}$.
   * `cape` (*float64*): Cyclically Adjusted Price-to-Earnings ratio (P/E10), defined as real price divided by the 10-year (120-month) moving average of real lagged corporate earnings: $\frac{P_t^{real}}{\frac{1}{120}\sum_{i=0}^{119} E_{t-3-i}^{real}}$.
   * `yield_gap` (*float64*): Real equity yield gap (earnings yield minus the 10-year Treasury rate): $\frac{E_{t-3}}{P_t} - \frac{GS10_t}{100}$.
   * `drawdown` (*float64*): Current percentage drawdown of the cumulative real total return index from its preceding historical peak: $\frac{TR_t}{\max_{\tau \le t}(TR_\tau)} - 1$.
5. **Target Variables (Forward Annualized Real Returns):**
   * `fwd_ret_1y` (*float64*): 1-year forward annualized real total return: $\left(\frac{TR_{t+12}}{TR_t}\right)^{1} - 1$.
   * `fwd_ret_5y` (*float64*): 5-year forward annualized real total return: $\left(\frac{TR_{t+60}}{TR_t}\right)^{12/60} - 1$.
   * `fwd_ret_10y` (*float64*): 10-year forward annualized real total return: $\left(\frac{TR_{t+120}}{TR_t}\right)^{12/120} - 1$.

#### Summary Statistics of the Clean Dataset (`shiller_clean.csv`, N=1,866)

| Variable | Valid Count | Missing | Mean | Std. Dev. | Min | 25% | Median | 75% | Max |
|---|---|---|---|---|---|---|---|---|---|
| `P` | 1,866 | 0 | 474.95 | 1089.70 | 2.73 | 8.04 | 19.85 | 264.30 | 7,450.03 |
| `D` | 1,866 | 0 | 8.78 | 16.41 | 0.18 | 0.43 | 0.98 | 8.60 | 81.70 |
| `E` | 1,866 | 0 | 21.44 | 44.11 | 0.16 | 0.59 | 2.11 | 15.88 | 295.39 |
| `CPI` | 1,866 | 0 | 69.82 | 86.20 | 6.28 | 10.42 | 23.70 | 114.25 | 335.12 |
| `GS10` (%) | 1,866 | 0 | 4.48 | 2.28 | 0.62 | 3.18 | 3.83 | 5.05 | 15.32 |
| `P_real` | 1,866 | 0 | 906.19 | 1220.14 | 90.40 | 230.36 | 361.95 | 920.34 | 7,450.03 |
| `ret_real` (mo.) | 1,865 | 1 | 0.0066 | 0.0408 | -0.2619 | -0.0132 | 0.0094 | 0.0294 | 0.5243 |
| `tr_index` | 1,866 | 0 | 3,131.74 | 6,777.08 | 0.99 | 16.54 | 122.04 | 2,001.27 | 42,719.71 |
| `mom_6m` | 1,860 | 6 | 0.0423 | 0.1206 | -0.4005 | -0.0312 | 0.0456 | 0.1114 | 0.6881 |
| `mom_12m` | 1,854 | 12 | 0.0875 | 0.1915 | -0.5812 | -0.0332 | 0.0883 | 0.2044 | 1.5131 |
| `vol_12m` | 1,854 | 12 | 0.1196 | 0.0673 | 0.0321 | 0.0833 | 0.1053 | 0.1346 | 0.6743 |
| `pe` | 1,863 | 3 | 16.46 | 9.21 | 5.06 | 11.79 | 15.27 | 18.90 | 139.09 |
| `cape` | 1,744 | 122 | 17.92 | 7.69 | 4.85 | 12.14 | 16.64 | 21.68 | 44.85 |
| `yield_gap` | 1,863 | 3 | 0.0265 | 0.0319 | -0.0490 | 0.0070 | 0.0266 | 0.0425 | 0.1521 |
| `drawdown` | 1,866 | 0 | -0.1220 | 0.1425 | -0.7680 | -0.2064 | -0.0625 | -0.0007 | 0.0000 |
| `fwd_ret_1y` | 1,854 | 12 | 0.0875 | 0.1915 | -0.5812 | -0.0332 | 0.0883 | 0.2044 | 1.5131 |
| `fwd_ret_5y` | 1,806 | 60 | 0.0723 | 0.0778 | -0.1323 | 0.0210 | 0.0739 | 0.1201 | 0.3335 |
| `fwd_ret_10y` | 1,746 | 120 | 0.0699 | 0.0509 | -0.0592 | 0.0383 | 0.0702 | 0.1060 | 0.1996 |

### Is there a label or target associated with each instance?
Yes. For regression tasks, the continuous targets are `fwd_ret_1y`, `fwd_ret_5y`, and `fwd_ret_10y`. For classification tasks (predicting positive real excess return over cash/bonds), binary labels are derived from these continuous variables.

### Is any information missing from individual instances?
No random or inadvertent missing values exist. The observed missing cells are **structural boundary artifacts** strictly caused by lag operators, moving windows, and forward horizons:
* **Initial Window Missingness:** 
  * Month 0 (`1871-01-01`): `ret_real` is missing because no preceding month $t-1$ exists.
  * Months 0–2: `E_lag`, `D_lag`, `pe`, and `yield_gap` are NaN due to the 3-month backward shift.
  * Months 0–5: `mom_6m` is NaN.
  * Months 0–11: `mom_12m` and `vol_12m` are NaN.
  * Months 0–121: `cape` is NaN because 120 consecutive months of historical real earnings are required plus the 3-month lag; CAPE commences at month 122 (`1881-03-01`).
* **Terminal Horizon Missingness:**
  * Months 1854–1865 (the last 12 months): `fwd_ret_1y` is unobserved because subsequent realized returns extend beyond June 2026.
  * Months 1806–1865 (the last 60 months): `fwd_ret_5y` is unobserved.
  * Months 1746–1865 (the last 120 months): `fwd_ret_10y` is unobserved.

Retaining these rows in `shiller_clean.csv` rather than performing premature global row deletion ensures that shorter-horizon models (e.g., 1-year forecasting) preserve an additional 108 months of modern out-of-sample test data compared to 10-year models.

### Are relationships between individual instances made explicit (e.g., users' movie ratings, social network links)?
Yes. The explicit relationship is strictly temporal and chronological. Every observation is ordered by `date` with regular 1 month spacing. Consecutive instances possess high serial correlation. In multi-year forward targets, overlapping return windows create strong moving-average error structures (e.g., the 10-year return starting in January 1990 shares 119 of 120 months with the 10-year return starting in February 1990).

### Are there recommended data splits (e.g., training, development/validation, testing)?
* **Prohibition of Random Splitting:** Standard random $k$-fold cross-validation is strictly forbidden; randomly permuting time-series observations causes catastrophic data leakage across overlapping windows and violates causality.
* **Recommended Walk-Forward Split:** An expanding-window walk-forward split with a buffer gap equal to the forecast horizon $h$ (12, 60, or 120 months).
* **Macroeconomic Regime Sub-Samples:**
  * *Full Historical Sample:* 1871–2026 (1,866 months).
  * *Modern Institutional Era:* 1926–2026 (post-CRSP, modern corporate governance).
  * *Post-Bretton Woods / Fiat Currency Regime:* 1971–2026 (floating exchange rates, modern Federal Reserve monetary policy).
  * *Out-of-Sample Evaluation Window:* 1995–2026 (encompassing the 1990s tech bubble, 2008 global financial crisis, 2020 pandemic crash, and 2022–2026 inflation cycle).

### Are there any errors, sources of noise, or redundancies in the dataset?
1. **Working's Effect (Time-Averaging Bias):** Averaging daily closing prices over a month smooths price movements, creating artificial positive autocorrelation in monthly returns and making sharp market crashes, such as Black Monday in 1987, appear less severe.
2. **Linear Interpolation of Corporate Fundamentals:** Corporate earnings and dividends are quarterly figures linearly interpolated across monthly steps by S&P and Shiller. This artificially smooths month-to-month fundamentals and suppresses earnings surprises.
3. **Pre-1926 Retrospective Splicing:** Data prior to 1926 relies on Alfred Cowles' retrospective reconstructions from surviving financial periodicals (Cowles Commission Common Stock Indexes, 1939). Dividend yields and earnings from 1871–1925 were estimated from annual distributions and interpolated.
4. **Raw Date Truncation:** In raw Excel storage, `1871.10` is stored as float `1871.1`, confounding October with January (`1871.01`). This was detected and eliminated during preprocessing.

### Is the dataset self-contained, or does it link to or otherwise rely on external resources?
* The dataset is 100% self-contained.
* The external upstream source is hosted at `https://shillerdata.com/` and mirrored on the Yale University Department of Economics server (`http://www.econ.yale.edu/~shiller/data.htm`). Robert Shiller maintains these files publicly without API keys, paywalls, or restrictive authentication.

### Does the dataset contain data that might be considered confidential?
No. All data points reflect public macroeconomic indicators, published financial market indices, and official government interest rates.

### Does the dataset contain data that might be offensive, insulting, threatening, or cause anxiety?
No. The dataset consists purely of impersonal financial metrics and economic time series.

### Questions Relating to People (Subpopulations, Individual Identification, Sensitive Attributes)
* **Subpopulations / Demographics:** Not applicable. The dataset contains macroeconomic market indices, not individual human subjects.
* **Individual Identification:** Not applicable. It is impossible to identify any individual natural person directly or indirectly from aggregate market and macroeconomic figures.
* **Sensitive Attributes (GDPR Special Categories):** Not applicable. Contains no personal, racial, genetic, biometric, political, or healthcare data.

---

## 3. Collection Process

### How was the data associated with each instance acquired? Was the data directly observable, reported by subjects, or indirectly inferred/derived?
* **Nominal Stock Prices ($P$):** Directly observable open-market closing prices of publicly traded equities on the New York Stock Exchange (NYSE), compiled and weighted by market capitalization by Standard & Poor's (post-1926) and Alfred Cowles (1871–1925). Monthly values are the direct arithmetic mean of daily prices.
* **Dividends ($D$) & Earnings ($E$):** Reported by public corporate issuers in financial filings (10-Q and 10-K statements submitted to the U.S. Securities and Exchange Commission post-1934; historical corporate annual reports pre-1934). Standard & Poor's aggregates these into trailing 12-month composite figures, and monthly figures are linearly interpolated.
* **Consumer Price Index ($CPI$):** Published monthly by the **U.S. Bureau of Labor Statistics (BLS)** as the Consumer Price Index for All Urban Consumers (CPI-U) from 1913 to present. Spliced backward from 1871–1912 using Warren and Pearson's wholesale price index.
* **10-Year Treasury Yield ($GS10$):** Published by the **Federal Reserve Board** (Federal Reserve H.15 statistical release / FRED) as the 10-year Treasury constant maturity rate. Pre-1925 yields were compiled from government and high-grade railroad bond yields documented in Homer and Sylla's *A History of Interest Rates*.

### What mechanisms or procedures were used to collect the data? How were these mechanisms validated?
* Historically, the dataset was compiled through manual archival extraction by Professor Shiller and research assistants from printed volumes.
* In modern decades, Shiller maintains the series via automated retrieval and manual verification from primary economic releases.
* **Validation:** Shiller validated the series by cross-verifying with CRSP market totals, NBER macrohistory series, and independent academic pricing studies. After the preprocessing, the total return index was verified by replicating Shiller's native total return price column (`shiller_tr_price`), achieving a 1.0 Pearson correlation and an identical compounded wealth terminal factor of 42,720.

### Who was involved in the data collection process and how were they compensated?
The upstream data was curated by Professor Robert J. Shiller and academic graduate research assistants at Yale University, compensated under standard university research appointment salaries.

### Over what timeframe was the data collected? Does this timeframe match the creation timeframe of the data?
* **Data Observation Timeframe:** January 1871 to June 2026.
* **Collection Timeframe:** The historical foundation was reconstructed retrospectively during the 1980s and 1990s. Since 2000, updates have been collected and published contemporaneously on a monthly cadence.

### Were any ethical review processes conducted (e.g., by an institutional review board)?
No Institutional Review Board (IRB) review was required, as the dataset is strictly non-human subject research utilizing public financial and government statistics.

### Questions Relating to People (Consent, Revocation, Impact Analysis)
Not applicable (no human subjects).

---

## 4. Preprocessing / Cleaning / Labeling

### Was any preprocessing/cleaning/labeling of the data done? If so, please provide a description.
Yes. The entire data engineering pipeline was implemented in `01_preprocessing.ipynb`, transforming raw `ie_data.xls` into `shiller_clean.csv`. The preprocessing consists of eight distinct transformations (described in detail in preprocessing the notebook):

```
[Raw ie_data.xls] (1,870 rows)
   │
   ├─► 1. Metadata Stripping & Non-Data Filter (Skip 8 header rows, drop terminal comment row)
   ├─► 2. Date String Parsing (Repair float truncation: '1871.1' -> '1871-10-01')
   ├─► 3. Data Integrity & Completeness Check (Verify 0 duplicate/missing calendar months)
   ├─► 4. Terminal Unreleased Fundamentals Pruning (Drop 2026-07 to 2026-10 with NaN in E/D)
   ├─► 5. Look-Ahead Bias Mitigation (Lag corporate earnings E and dividends D by 3 months)
   ├─► 6. Inflation Normalization & Real Total Return Construction (CPI deflator, dividend reinvestment)
   ├─► 7. Signal & Feature Engineering (mom_6m, mom_12m, vol_12m, pe, cape, yield_gap, drawdown)
   └─► 8. Forward Multi-Horizon Target Formulation (fwd_ret_1y, fwd_ret_5y, fwd_ret_10y)
   │
[data/shiller_clean.csv] (1,866 rows, 20 feature columns)
```

### Was the "raw" data saved in addition to the preprocessed/cleaned/labeled data?
Yes. The unchanged original Excel workbook is archived.

### Is the software that was used to preprocess/clean/label the data available?
Yes. The full preprocessing pipeline is implemented in the notebook `01_preprocessing.ipynb` using standard open-source Python packages.

---

## 5. Uses

### Has the dataset been used for any tasks already?
* **Academic Literature:** The Shiller dataset has been utilized in hundreds of peer-reviewed finance and economics papers to demonstrate various economic phenomena.
* **Course Project:** Utilized in the project to examine:
  1. *Exploratory Analysis:* Real return distributions, historical drawdown duration curves, and volatility drag in leveraged ETFs.
  2. *Hypothesis Testing:* Formal statistical tests of market timing ("waiting for a crash" vs. buy-and-hold) and risk-adjusted Sharpe ratio differentials across volatility/momentum regimes.
  3. *Predictive Machine Learning:* Walk-forward evaluation of different models against historical mean and CAPE baselines.

### Is there a repository that links to any or all papers or systems that use the dataset?
Robert Shiller maintains bibliographic links on his Yale faculty webpage ([http://www.econ.yale.edu/~shiller/data.htm](http://www.econ.yale.edu/~shiller/data.htm)). Google Scholar records over 12,000 citations to Shiller's foundational works utilizing this dataset.

### What (other) tasks could the dataset be used for?
* Macroeconomic regime clustering.
* Safe Withdrawal Rate (SWR) simulations for long-term retirement planning.
* Cointegration analysis between corporate earnings, consumer price levels, and aggregate market capitalization.
* Econometric testing of structural breaks across major monetary regimes.

### Is there anything about the composition of the dataset or the way it was collected that might impact future uses? (Biases, Risks, and Harms)
1. **Severe Autocorrelation in Overlapping Targets:** Using monthly sampling with 5-year ($h=60$) and 10-year ($h=120$) forecast windows induces extreme serial correlation in the target residuals. A 10-year target in month $t$ shares 119 out of 120 months with month $t+1$.
2. **Working's Effect:** Because monthly prices are daily averages rather than month-end quotes, extreme intra-month crashes (such as Black Monday, October 1987) appear less severe than they actually were. Downstream models should not use this dataset to estimate intraday value-at-risk (VaR).
3. **Survivorship and U.S. Selection Bias ("American Exceptionalism"):** The dataset exclusively reflects the corporate history of the United States, a market that experienced extraordinary economic growth, technological leadership, and geopolitical stability over the 20th century without suffering catastrophic market closures or sovereign collapse (unlike Russia in 1917, Germany in 1944, or China in 1949).
4. **Omission of Trading Costs, Management Fees, and Taxes:** The compounded total return index assumes frictionless reinvestment of dividends without broker commissions, borrow fees, or dividend taxes. Real-world investor wealth compounding would be lower due to fee drag and tax friction.
5. **Macroeconomic Non-Stationarity:** Macroeconomic relationships and federal regulations have fundamentally shifted across eras.

### Are there tasks for which the dataset should NOT be used?
* **High-Frequency or Intraday Algorithmic Trading:** The monthly average granularity makes the dataset completely unsuitable for intraday, daily, or sub-monthly trade execution.
* **Individual Stock Selection:** The dataset represents the broad market index; it contains zero cross-sectional firm-level fundamental metrics.
* **Direct Unsupervised Automated Capital Allocation:** Machine learning models trained on historical macroeconomic data should never execute financial trades without professional oversight, risk limits, and stress testing.

---

## 6. Distribution

### Will the dataset be distributed to third parties outside of the entity on behalf of which the dataset was created?
Yes. The original Shiller dataset is open to the public globally. The project repository containing both raw and preprocessed data is publicly available on GitHub at [https://github.com/Prokaee/Datapipelines_Projekt](https://github.com/Prokaee/Datapipelines_Projekt).

### How will the dataset be distributed? Does the dataset have a digital object identifier (DOI)?
* The raw upstream data is distributed as an Excel binary file (`ie_data.xls`) at `https://shillerdata.com/`.
* The preprocessed project version is available via GitHub repository clone or direct CSV download (`data/shiller_clean.csv`).
* The dataset does not currently have a formal DOI.

### When will the dataset be distributed?
The upstream dataset was first posted publicly in 2000 and is updated monthly. The project derivative dataset was first published on October 26, 2026.

### Will the dataset be distributed under a copyright or other intellectual property (IP) license, and/or under applicable terms of use (ToU)?
* **Robert Shiller Disclaimer & Terms:** Professor Shiller distributes the data freely for educational and research purposes under the standard academic disclaimer:
  > *"The data and CAPE Ratio on this spreadsheet were developed by Robert J. Shiller using various public sources. Neither Robert J. Shiller nor any affiliates or consultants, are registered investment advisers and do not guarantee the accuracy or completeness of the CAPE Ratio here, or any data or methodology either included therein or upon which it is based. Individual investment decisions are best made with the help of a professional investment adviser."*
  Users are expected to cite Robert J. Shiller, *Irrational Exuberance*, Princeton University Press.
* **Course Repository License:** Shared for educational and academic evaluation purposes.

### Have any third parties imposed IP-based or other restrictions on the data associated with the instances?
S&P Dow Jones Indices LLC holds proprietary rights to the S&P 500 index trademark and real-time calculation methodology, while historical monthly composite time series published for academic research are widely treated as public historical information.

### Do any export controls or other regulatory restrictions apply to the dataset?
No export controls or regulatory restrictions apply.

---

## 7. Maintenance

### Who will be supporting/hosting/maintaining the dataset?
* **Upstream Primary Dataset:** Maintained and hosted by **Professor Robert J. Shiller** and the Yale University Department of Economics via `https://shillerdata.com/`.
* **Preprocessed Project Version:** Maintained by the team during the project duration.

### How can the owner/curator/manager of the dataset be contacted?
* Robert J. Shiller: Yale University, Department of Economics, New Haven, CT (`robert.shiller@yale.edu`).
* Project Team Members: Via GitHub ([https://github.com/Prokaee/Datapipelines_Projekt](https://github.com/Prokaee/Datapipelines_Projekt)) or university email.

### Is there an erratum?
* Upstream Primary Dataset: There is no separate erratum file; revisions, corrections, and note additions are incorporated directly into updated releases of `ie_data.xls`.
* Preprocessed Project Version: Corrections and modifications to the preprocessing pipeline are tracked through Git commit logs in the GitHub repository.

### Will the dataset be updated (e.g., to correct errors, add new instances)?
* **Upstream Data:** Robert Shiller updates `ie_data.xls` approximately once per month as new monthly closing prices, BLS CPI estimates, and quarterly S&P earnings releases are published.
* **Course Project Dataset:** The file `data/shiller_clean.csv` might change during project work. Any changes will be described in the updated preprocessing notebook.

### If the dataset relates to people, are there applicable limits on data retention?
Not applicable (no personal data).

### Will older versions of the dataset continue to be supported/hosted/maintained?
Older snapshots are archived in Git history within the project repository.

### If others want to extend/augment/build on/contribute to the dataset, is there a mechanism for them to do so?
Yes. Third parties and collaborators may fork the GitHub repository and perform enhancements or fixes.
