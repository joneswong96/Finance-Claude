"""
TRAW (Traws Pharma) Quantitative & Statistical Analysis
Date: 2026-05-10
Analyst: Quant-Analyst Agent

All assumptions explicitly flagged with [ASSUMPTION] tags.
"""

import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

print("=" * 72)
print("TRAWS PHARMA (NASDAQ: TRAW) — QUANTITATIVE ANALYSIS")
print("Analysis Date: 2026-05-10")
print("=" * 72)

# ─────────────────────────────────────────────────────────────────────────────
# RAW DATA INPUTS
# ─────────────────────────────────────────────────────────────────────────────
price          = 2.09          # current price post-May 8
market_cap     = 31.7e6        # $31.7M
shares_out     = 15.15e6       # shares outstanding
price_52w_high = 3.27
price_52w_low  = 0.97
avg_vol        = 207_000       # average daily volume
spike_vol      = 69_250_000    # May 8 volume
cash           = 13.8e6        # post-PIPE cash estimate
monthly_burn   = 1.5e6
pipe_price     = 1.673         # $/share PIPE April 2026

# ─────────────────────────────────────────────────────────────────────────────
# MODULE 1: VALUATION METRICS
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "─" * 72)
print("MODULE 1: VALUATION METRICS")
print("─" * 72)

cash_per_share = cash / shares_out
p_cash_ratio   = price / cash_per_share

# Enterprise Value: EV = Mkt Cap - Cash + Debt
# [ASSUMPTION] Debt = $0 (negative stockholders' equity may reflect accumulated
#              losses / accumulated deficit, not necessarily interest-bearing debt;
#              exact debt figure NOT provided in data package — flag as gap)
assumed_debt = 0.0
ev = market_cap - cash + assumed_debt
ev_per_share = ev / shares_out

print(f"\n  Current Price:         ${price:.2f}")
print(f"  Market Cap:            ${market_cap/1e6:.1f}M")
print(f"  Cash (post-PIPE est.): ${cash/1e6:.1f}M")
print(f"  Cash per Share:        ${cash_per_share:.3f}")
print(f"  P/Cash Ratio:          {p_cash_ratio:.2f}x")
print(f"  [ASSUMPTION] Debt = $0 (not specified; flag as data gap)")
print(f"  Enterprise Value:      ${ev/1e6:.2f}M")
print(f"  EV per Share:          ${ev_per_share:.3f}")
print(f"  Premium to Cash/Share: {((price - cash_per_share)/cash_per_share)*100:.1f}%")
print(f"  Price / 52w High:      {price/price_52w_high:.2%}  (drawdown from high)")
print(f"  Price / 52w Low:       {price/price_52w_low:.2%}  (premium to low)")
print(f"  PIPE Discount to Mkt:  {((price - pipe_price)/price)*100:.1f}% above PIPE price")

print("\n  INTERPRETATION:")
print(f"  At {p_cash_ratio:.2f}x Price/Cash, the stock trades at a significant premium")
print(f"  to its treasury. The ~${ev/1e6:.1f}M of EV above cash represents the market's")
print(f"  option value on ratutrelvir and any hantavirus pipeline. For a pre-revenue")
print(f"  biotech, this is a pure pipeline/optionality valuation.")
print(f"  DATA GAP: Exact debt/liabilities schedule required for precise EV.")

# ─────────────────────────────────────────────────────────────────────────────
# MODULE 2: BURN RATE & DILUTION RISK
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "─" * 72)
print("MODULE 2: BURN RATE ANALYSIS & DILUTION RISK")
print("─" * 72)

runway_months = cash / monthly_burn
runway_date_offset_months = runway_months  # from now (2026-05-10)

# Shares needed at various dilution prices to raise enough cash to extend runway
extension_target_months = 12  # another year of runway
cash_needed = monthly_burn * extension_target_months

# [ASSUMPTION] Warrant terms: data package mentions "$50M additional" PIPE capacity.
# We model warrants at 1.1x PIPE price (typical biotech structure) and also at PIPE price.
# Exact warrant strike NOT provided — flagged as a critical data gap.
warrant_strike_assumed = pipe_price * 1.10   # [ASSUMPTION] 10% premium to PIPE
warrant_coverage_assumed = 1.0               # [ASSUMPTION] 1:1 warrant coverage ratio

# If $50M in additional warrants are exercised:
assumed_warrant_raise = 50e6
shares_from_warrants = assumed_warrant_raise / warrant_strike_assumed
dilution_from_warrants_pct = shares_from_warrants / shares_out * 100

# Survival dilution: what price + how many new shares needed to survive 12 more months
survival_price_levels = [1.00, 1.50, 1.673, 2.00, 2.09]
print(f"\n  Current Cash:          ${cash/1e6:.1f}M")
print(f"  Monthly Burn Rate:     ${monthly_burn/1e6:.2f}M/month")
print(f"  Implied Runway:        {runway_months:.1f} months (to ~Q1 2027)")
print(f"  Cash to Extend 12mo:   ${cash_needed/1e6:.1f}M needed")

print(f"\n  [ASSUMPTION] Warrant strike = ${warrant_strike_assumed:.3f} (10% above PIPE price of ${pipe_price})")
print(f"  [ASSUMPTION] $50M additional PIPE capacity in warrants (from data package)")
print(f"  [DATA GAP]  Exact warrant strike, quantity, and expiry NOT provided")

print(f"\n  Warrant Dilution Scenario ($50M raise at ${warrant_strike_assumed:.3f}):")
print(f"    New Shares Issued:   {shares_from_warrants/1e6:.2f}M")
print(f"    Dilution to Existing:{dilution_from_warrants_pct:.1f}%")
print(f"    Pro-Forma Shares:    {(shares_out + shares_from_warrants)/1e6:.2f}M")
print(f"    Pro-Forma Mkt Cap*:  ${((shares_out + shares_from_warrants) * price)/1e6:.1f}M (*at current price)")

print(f"\n  Survival Fundraise Table (to raise ${cash_needed/1e6:.0f}M for 12 months):")
print(f"  {'Offer Price':>14} | {'New Shares (M)':>14} | {'Dilution %':>10} | {'Pro-Forma Shares (M)':>20}")
print(f"  {'-'*14}-+-{'-'*14}-+-{'-'*10}-+-{'-'*20}")
for p_offer in survival_price_levels:
    new_shares = cash_needed / p_offer
    dil_pct = new_shares / shares_out * 100
    pro_forma = (shares_out + new_shares) / 1e6
    print(f"  ${p_offer:>13.3f} | {new_shares/1e6:>13.2f}M | {dil_pct:>9.1f}% | {pro_forma:>19.2f}M")

print(f"\n  KEY RISK: At current ~$2.09 price, raising ${cash_needed/1e6:.0f}M requires")
print(f"  ~{cash_needed/price/1e6:.1f}M new shares — a {cash_needed/price/shares_out*100:.0f}% dilution event.")
print(f"  Biotech secondaries typically price at 10-20% discount to market,")
print(f"  implying effective dilution of {cash_needed/(price*0.85)/shares_out*100:.0f}–{cash_needed/(price*0.90)/shares_out*100:.0f}%.")

# ─────────────────────────────────────────────────────────────────────────────
# MODULE 3: VOLUME / MOMENTUM ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "─" * 72)
print("MODULE 3: VOLUME & MOMENTUM ANALYSIS")
print("─" * 72)

volume_ratio = spike_vol / avg_vol
# Days-to-cover spike volume relative to float
# [ASSUMPTION] Float ≈ shares outstanding (no insider lock-up data provided)
float_assumed = shares_out  # [ASSUMPTION]
spike_vol_as_pct_float = spike_vol / float_assumed * 100

# Turnover rate: fraction of float that traded on May 8
turnover_rate = spike_vol / float_assumed

# Typical post-catalyst biotech volume decay (half-life analysis)
# Model: volume decays exponentially with half-life = 2 trading days (empirical biotech norm)
# [ASSUMPTION] Exponential decay model for post-announcement volume
half_life_days = 2.0
days = np.arange(0, 15)
vol_decay = avg_vol + (spike_vol - avg_vol) * np.exp(-np.log(2) / half_life_days * days)

print(f"\n  May 8 Spike Volume:    {spike_vol/1e6:.2f}M shares")
print(f"  Avg Daily Volume:      {avg_vol/1e3:.0f}K shares")
print(f"  Volume Ratio:          {volume_ratio:.0f}x normal")
print(f"  Float Turnover (May8): {turnover_rate:.1f}x float in one session")
print(f"  [ASSUMPTION] Float = shares outstanding ({shares_out/1e6:.2f}M); actual float may differ")

print(f"\n  Nano-Cap Liquidity Analysis:")
print(f"  At $2.09 and 207K avg volume: daily $ liquidity = ${price * avg_vol / 1e3:.0f}K")
print(f"  Position size constraint (assuming max 10% of ADV):")
for pos_size_k in [50, 100, 250, 500, 1000]:
    days_to_build = (pos_size_k * 1000 / price) / (avg_vol * 0.10)
    print(f"    ${pos_size_k}K position → {days_to_build:.1f} trading days to build/unwind")

print(f"\n  VOLUME SPIKE STATISTICAL ANALYSIS:")
# Z-score of May 8 volume assuming log-normal distribution (standard for volumes)
# [ASSUMPTION] Log-normal volume with mean=log(avg_vol), std=0.8 (typical biotech nano-cap)
ln_vol_std_assumed = 0.8  # [ASSUMPTION]
ln_spike_z = (np.log(spike_vol) - np.log(avg_vol)) / ln_vol_std_assumed
print(f"  Log-volume Z-score:    {ln_spike_z:.1f}σ above mean")
print(f"  [ASSUMPTION] Log-vol std = {ln_vol_std_assumed} (typical nano-cap biotech)")
print(f"  Probability of ≥335x volume by chance: effectively 0% (>{ln_spike_z:.0f}σ event)")

print(f"\n  BREAKOUT vs. DEAD-CAT BOUNCE FRAMEWORK:")
print(f"  Genuine Breakout Indicators:")
print(f"    - Volume 335x normal: extreme, consistent with institutional/algorithmic discovery")
print(f"    - Post-catalyst price sustained >20% above pre-announcement (IF holding)")
print(f"    - Float turnover >4.5x in one session creates significant holder base rotation")
print(f"\n  Dead-Cat Bounce Indicators:")
print(f"    - 9-month cash runway: fundamental terminal risk NOT resolved by announcement")
print(f"    - No revenue pathway disclosed for hantavirus (preclinical/early stage implied)")
print(f"    - PIPE overhang at $1.673: sellers exist at 20% below current price")
print(f"    - Nano-cap: thin liquidity means small selling pressure can reprice sharply")
print(f"    - Pattern: FDA clinical hold (March) → PIPE at depressed price (April) →")
print(f"      hantavirus announcement (May) = textbook catalyst manufacturing sequence")

print(f"\n  VERDICT: Balance of evidence favors DEAD-CAT BOUNCE setup.")
print(f"  The volume spike reflects genuine discovery/speculation momentum but does NOT")
print(f"  resolve the structural cash cliff at Q1 2027. Without pipeline monetization,")
print(f"  a secondary offering is near-certain, which historically resets the price to")
print(f"  offer price ± 10% within 30-60 trading days for nano-cap biotechs.")

# ─────────────────────────────────────────────────────────────────────────────
# MODULE 4: PIPE OVERHANG ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "─" * 72)
print("MODULE 4: PIPE OVERHANG & WARRANT DILUTION")
print("─" * 72)

# PIPE mechanics
# [ASSUMPTION] PIPE raised approximately $X at $1.673/share.
# Data package does not specify the dollar amount of the April PIPE — only the price.
# We back-calculate from the post-PIPE cash estimate.
# Pre-PIPE cash: unknown. Post-PIPE cash: ~$13.8M.
# [ASSUMPTION] Pre-PIPE cash was ~$8-10M (6-7 months runway before PIPE at $1.5M/month)
pre_pipe_cash_assumed = 9.0e6  # [ASSUMPTION]
pipe_raise_amount = cash - pre_pipe_cash_assumed  # implied ~$4.8M
pipe_shares_issued = pipe_raise_amount / pipe_price

print(f"  PIPE Price (April 2026):  ${pipe_price:.3f}/share")
print(f"  Current Price:            ${price:.2f}/share")
print(f"  PIPE Discount to Market:  {(1 - pipe_price/price)*100:.1f}%")
print(f"  [ASSUMPTION] Pre-PIPE cash ~${pre_pipe_cash_assumed/1e6:.0f}M")
print(f"  [ASSUMPTION] Implied PIPE Raise: ~${pipe_raise_amount/1e6:.1f}M")
print(f"  [DATA GAP] Exact PIPE size (shares and $ amount) not provided")
print(f"  [ASSUMPTION] Implied PIPE shares issued: ~{pipe_shares_issued/1e6:.2f}M")

print(f"\n  PIPE Investor Profit/Loss at Various Prices:")
pipe_investor_basis = pipe_price
for test_price in [0.97, 1.50, 1.673, 2.09, 2.50, 3.00, 3.27]:
    pnl = (test_price - pipe_investor_basis) / pipe_investor_basis * 100
    status = "PROFIT" if pnl > 0 else "LOSS"
    print(f"    Price ${test_price:.3f}: PIPE investor {status} = {pnl:+.1f}%")

print(f"\n  PIPE Overhang Mechanics:")
print(f"  PIPE investors typically have registration rights (resale shelf within 30-90 days).")
print(f"  At current price of $2.09, PIPE investors are sitting on +{(price/pipe_price-1)*100:.0f}%.")
print(f"  This creates a STRONG incentive to sell into any strength above $1.673.")
print(f"  [DATA GAP] Exact lock-up period and registration rights terms unknown.")

print(f"\n  Warrant Dilution ($50M Additional Capacity):")
print(f"  [DATA GAP] Warrant strike price not specified in data package.")
print(f"  Scenario analysis at various warrant strikes:")
for w_strike_mult in [1.0, 1.1, 1.25, 1.5]:
    w_strike = pipe_price * w_strike_mult
    shares_from_w = 50e6 / w_strike
    total_dil = (shares_from_w / shares_out) * 100
    new_total = shares_out + shares_from_w
    theo_price = (market_cap + 50e6) / new_total  # naive dilution-adjusted price
    print(f"    Strike ${w_strike:.3f} ({w_strike_mult:.2f}x PIPE): {shares_from_w/1e6:.1f}M new shares, "
          f"{total_dil:.0f}% dilution, theo price ${theo_price:.2f}")

# ─────────────────────────────────────────────────────────────────────────────
# MODULE 5: RISK-ADJUSTED RETURN — EXPECTED VALUE ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "─" * 72)
print("MODULE 5: RISK-ADJUSTED EXPECTED VALUE ANALYSIS")
print("─" * 72)

# Three scenarios with probability weights
# Assumptions are explicitly grounded in the data
scenarios = {
    "Bull": {
        "probability": 0.15,
        "description": "Ratutrelvir Phase 3 initiated + hantavirus fast-track; partnership/licensing deal",
        "price_target": 6.00,
        "rationale": "Pipeline monetization removes cash cliff; 2-3x current EV on deal premium",
        "horizon_months": 12,
    },
    "Base": {
        "probability": 0.35,
        "description": "Ratutrelvir data mixed; secondary offering at ~$1.50; dilution reset",
        "price_target": 1.20,  # post-dilution reset with 50%+ dilution at discount
        "rationale": "Secondary at 15-20% discount to reset price ~$1.50-1.60; post-dilution NAV ~$1.20",
        "horizon_months": 9,
    },
    "Bear": {
        "probability": 0.50,
        "description": "Cash cliff reached without deal; forced PIPE/reverse merger; near-wipeout",
        "price_target": 0.30,
        "rationale": "Distressed financing or reverse merger; equity retention ~15% for existing holders",
        "horizon_months": 9,
    },
}
# [ASSUMPTION] Probabilities sum to 1.0 (0.15 + 0.35 + 0.50 = 1.00)
# [ASSUMPTION] Price targets based on analogous nano-cap biotech outcomes (no deal vs. deal)
# [ASSUMPTION] Bull case requires partnership — no evidence of active discussions provided

total_prob = sum(s["probability"] for s in scenarios.values())
assert abs(total_prob - 1.0) < 1e-9, "Probabilities must sum to 1.0"

entry_price = price
ev_calc = 0.0

print(f"\n  Entry Price: ${entry_price:.2f}")
print(f"\n  {'Scenario':>8} | {'Prob':>6} | {'Price Target':>12} | {'Return':>8} | {'EV Contribution':>16}")
print(f"  {'-'*8}-+-{'-'*6}-+-{'-'*12}-+-{'-'*8}-+-{'-'*16}")

for scenario_name, s in scenarios.items():
    ret = (s["price_target"] - entry_price) / entry_price
    ev_contribution = s["probability"] * s["price_target"]
    ev_calc += ev_contribution
    print(f"  {scenario_name:>8} | {s['probability']:>5.0%} | ${s['price_target']:>10.2f} | "
          f"{ret:>+7.1%} | ${ev_contribution:>14.3f}")

ev_return = (ev_calc - entry_price) / entry_price
print(f"\n  Expected Value (EV):    ${ev_calc:.3f}")
print(f"  EV Return vs Entry:     {ev_return:+.1%}")
print(f"  EV < Entry Price:       {'YES — negative EV' if ev_calc < entry_price else 'NO — positive EV'}")

# Probability-weighted volatility (standard deviation of outcomes)
scenario_prices = np.array([s["price_target"] for s in scenarios.values()])
scenario_probs  = np.array([s["probability"]  for s in scenarios.values()])
ev_variance = np.sum(scenario_probs * (scenario_prices - ev_calc)**2)
ev_std = np.sqrt(ev_variance)
ev_coeff_variation = ev_std / ev_calc

print(f"\n  Outcome Std Deviation:  ${ev_std:.3f}")
print(f"  Coefficient of Var:     {ev_coeff_variation:.2f} (higher = more dispersed outcomes)")

# Risk-adjusted metrics
# Sharpe-like ratio: (EV - risk-free) / std_dev
rf_rate_12m = 0.045  # [ASSUMPTION] 12m risk-free rate ~4.5%
rf_price_equiv = entry_price * (1 + rf_rate_12m)
sharpe_like = (ev_calc - rf_price_equiv) / ev_std
print(f"\n  [ASSUMPTION] Risk-free rate: {rf_rate_12m:.1%}")
print(f"  Risk-free price equiv:  ${rf_price_equiv:.3f}")
print(f"  Sharpe-like ratio:      {sharpe_like:.3f}  (scenario-weighted; <0 = risk-unadjusted negative)")

print(f"\n  SCENARIO ASSUMPTIONS:")
for name, s in scenarios.items():
    print(f"  [{name}] {s['description']}")
    print(f"         Rationale: {s['rationale']}")
    print(f"         Horizon: {s['horizon_months']} months")

# ─────────────────────────────────────────────────────────────────────────────
# MODULE 6: POSITION SIZING
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "─" * 72)
print("MODULE 6: POSITION SIZING")
print("─" * 72)

# Kelly Criterion
# Kelly fraction f* = (p*b - q) / b
# where p = prob win, q = prob loss = 1-p, b = odds ratio
# For multi-outcome: f* = sum(pi * (xi - r) / variance) — full Kelly
# Using simplified Kelly with bull (win) vs. bear+base (loss) framing

# We'll use full Kelly across the three outcomes
# f* = E[log(1 + f*R)] maximized numerically
from scipy.optimize import minimize_scalar

def neg_expected_log_return(f, prices, probs, entry):
    """Minimize negative expected log return (= maximize expected log wealth)."""
    log_returns = np.log(prices / entry)
    weighted = np.sum(probs * np.log(1 + f * log_returns))
    # Protect against log(0) if f causes total loss
    if np.any(1 + f * log_returns <= 0):
        return 1e6
    return -np.sum(probs * np.log(1 + f * log_returns))

result = minimize_scalar(
    neg_expected_log_return,
    bounds=(0.0, 1.0),
    method='bounded',
    args=(scenario_prices, scenario_probs, entry_price)
)
kelly_full = result.x

# Half-Kelly and quarter-Kelly for more conservative sizing
half_kelly  = kelly_full / 2
qtr_kelly   = kelly_full / 4

print(f"\n  Kelly Criterion Position Sizing:")
print(f"  Full Kelly:             {kelly_full*100:.2f}% of portfolio")
print(f"  Half Kelly (practical): {half_kelly*100:.2f}% of portfolio")
print(f"  Quarter Kelly (conservative): {qtr_kelly*100:.2f}% of portfolio")

# Practical constraints for nano-cap
print(f"\n  Practical Constraints (override Kelly if more restrictive):")
print(f"  1. LIQUIDITY CAP: At $207K avg daily vol, a 1% position in a $10M portfolio")
print(f"     = $100K ÷ ($2.09 × 207K × 10%) = {100_000 / (price * avg_vol * 0.10):.1f} days to build")
print(f"     → Liquidity constraint implies max ~$43K/day ($207K × 10% × $2.09 × share = $43K daily)")

daily_dollar_liq_cap = price * avg_vol * 0.10
print(f"     Daily $ liquidity cap (10% of ADV): ${daily_dollar_liq_cap:,.0f}")

# Max position by portfolio size given 20-day build constraint
max_build_days = 20
max_pos_by_liq = daily_dollar_liq_cap * max_build_days
print(f"     Max position in 20 days: ${max_pos_by_liq:,.0f}")

print(f"\n  2. SINGLE-STOCK RISK CAP: Standard nano-cap biotech risk budget = max 0.5%")
print(f"     of portfolio NAV for category (negative EV, terminal risk, <$50M market cap)")

print(f"\n  3. CONCENTRATION LIMIT: For stocks with bear-case near-zero,")
print(f"     max position = (max tolerable loss) / (1 - bear_case_price/entry)")
max_tolerable_loss_pct = 0.01  # 1% portfolio impact from bear case
bear_return = (0.30 - entry_price) / entry_price
implied_max_position_pct = max_tolerable_loss_pct / abs(bear_return)
print(f"     If max tolerable portfolio loss from this stock = 1%:")
print(f"     Bear return = {bear_return:.1%} → max position = {implied_max_position_pct*100:.2f}% of portfolio")

print(f"\n  RECOMMENDED MAXIMUM ALLOCATION:")
recommended_max = min(qtr_kelly, 0.005, implied_max_position_pct)
print(f"  min(Quarter-Kelly={qtr_kelly*100:.2f}%, 0.5% cap, {implied_max_position_pct*100:.2f}% loss limit)")
print(f"  = {recommended_max*100:.2f}% of portfolio NAV (hard cap)")
print(f"\n  For a $10M portfolio: max position = ${recommended_max * 10e6:,.0f}")
print(f"  For a $1M portfolio:  max position = ${recommended_max * 1e6:,.0f}")
print(f"\n  [ASSUMPTION] Portfolio = diversified multi-asset; this is the MAXIMUM,")
print(f"  not the recommended. Given negative EV, 0% (no position) is equally defensible.")

# ─────────────────────────────────────────────────────────────────────────────
# MODULE 7: QUANTITATIVE RED FLAGS
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "─" * 72)
print("MODULE 7: QUANTITATIVE RED FLAGS SCORECARD")
print("─" * 72)

red_flags = [
    ("CRITICAL", "Cash runway < 12 months",
     f"{runway_months:.1f} months (to Q1 2027); terminal risk if no raise"),
    ("CRITICAL", "Negative stockholders' equity",
     "Liabilities exceed book assets; equity holders are residual claimants on nothing"),
    ("CRITICAL", "EV analysis negative",
     f"Scenario-weighted EV = ${ev_calc:.2f} vs entry ${entry_price:.2f} ({ev_return:+.1%})"),
    ("HIGH",     "Extreme liquidity risk",
     f"Avg daily $ volume = ${price*avg_vol/1e3:.0f}K; institutional exit in bear case catastrophic"),
    ("HIGH",     "PIPE overhang at $1.673",
     f"PIPE investors at +{(price/pipe_price-1)*100:.0f}% gain; strong sell incentive above $1.673"),
    ("HIGH",     "Volume spike anomaly",
     f"335x normal volume (May 8) is statistically extreme; likely driven by retail/social media"),
    ("HIGH",     "FDA clinical hold on tivoxavir",
     "Regulatory setback not resolved; reduces pipeline optionality"),
    ("MEDIUM",   "P/Cash ratio elevated",
     f"{p_cash_ratio:.2f}x: trading at significant premium to treasury with no revenue"),
    ("MEDIUM",   "Warrant dilution risk",
     f"$50M additional capacity → potentially {dilution_from_warrants_pct:.0f}%+ dilution if exercised"),
    ("MEDIUM",   "Announcement pattern risk",
     "PIPE at low → hantavirus news → classic 'manufactured catalyst' sequence"),
    ("LOW",      "No revenue / pre-commercial",
     "Zero revenue offset: reduces valuation anchor; all value is option value"),
    ("LOW",      "Nano-cap size effect",
     "$31.7M market cap: high beta to micro-cap sentiment; illiquid in stress"),
]

critical_count = sum(1 for f in red_flags if f[0] == "CRITICAL")
high_count     = sum(1 for f in red_flags if f[0] == "HIGH")
medium_count   = sum(1 for f in red_flags if f[0] == "MEDIUM")
low_count      = sum(1 for f in red_flags if f[0] == "LOW")

for severity, flag, detail in red_flags:
    marker = {"CRITICAL": "[!!!]", "HIGH": "[!! ]", "MEDIUM": "[ ! ]", "LOW": "[   ]"}[severity]
    print(f"\n  {marker} {severity}: {flag}")
    print(f"        {detail}")

print(f"\n  RED FLAG SUMMARY: {critical_count} CRITICAL | {high_count} HIGH | {medium_count} MEDIUM | {low_count} LOW")

# ─────────────────────────────────────────────────────────────────────────────
# MONTE CARLO: Price path simulation (burn-to-zero risk)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "─" * 72)
print("MODULE 8: MONTE CARLO — CASH DEPLETION PROBABILITY")
print("─" * 72)

# [ASSUMPTION] Monthly burn is fixed at $1.5M with ±$0.2M std dev
# [ASSUMPTION] Cash raises occur probabilistically (based on scenario weights)
# [ASSUMPTION] No revenue inflows
n_simulations = 50_000
n_months      = 18  # simulate 18 months from now

burn_mean = 1.5e6
burn_std  = 0.20e6  # [ASSUMPTION] 13% CV on burn rate

np.random.seed(42)
monthly_burns = np.random.normal(burn_mean, burn_std, (n_simulations, n_months))
monthly_burns = np.maximum(monthly_burns, 0)  # no negative burn

# Simulate cash trajectory
cash_paths = np.zeros((n_simulations, n_months + 1))
cash_paths[:, 0] = cash

# Random fundraise event: prob 0.40 of raising $10M at month 6-9 (base/bull scenarios)
raise_prob      = 0.40   # [ASSUMPTION]
raise_amount    = 10.0e6 # [ASSUMPTION]
raise_timing    = np.random.choice(np.arange(4, 10), n_simulations)  # random month 4-9
raise_occurs    = np.random.random(n_simulations) < raise_prob

for t in range(n_months):
    cash_paths[:, t+1] = cash_paths[:, t] - monthly_burns[:, t]
    # Add fundraise if it occurs at this month
    raise_mask = raise_occurs & (raise_timing == t)
    cash_paths[raise_mask, t+1] += raise_amount
    # Cash can't go below 0 (company folds or raises emergency capital)
    cash_paths[:, t+1] = np.maximum(cash_paths[:, t+1], 0)

# Probability of cash depletion (reaching zero) at each month
depletion_by_month = np.mean(cash_paths == 0, axis=0)
# Cumulative probability of having hit zero by month t
ever_depleted = np.any(cash_paths[:, 1:] == 0, axis=1)
cumulative_depletion = np.mean(ever_depleted)

print(f"\n  Monte Carlo Parameters ({n_simulations:,} simulations, {n_months} months):")
print(f"  Starting Cash:    ${cash/1e6:.1f}M")
print(f"  Burn: N(${burn_mean/1e6:.1f}M, ${burn_std/1e6:.1f}M) per month [ASSUMPTION]")
print(f"  Fundraise: {raise_prob:.0%} prob of ${raise_amount/1e6:.0f}M raise in months 4-9 [ASSUMPTION]")

print(f"\n  Month-by-Month Cash Depletion Probability:")
for month in [3, 6, 9, 12, 15, 18]:
    p_depleted = depletion_by_month[month]
    avg_cash = np.mean(cash_paths[:, month])
    p5_cash  = np.percentile(cash_paths[:, month], 5)
    p95_cash = np.percentile(cash_paths[:, month], 95)
    print(f"  Month {month:2d}: P(depleted)={p_depleted:.1%}, "
          f"Mean cash=${avg_cash/1e6:.2f}M, P5=${p5_cash/1e6:.2f}M, P95=${p95_cash/1e6:.2f}M")

print(f"\n  Cumulative P(cash depletion within 18 months): {cumulative_depletion:.1%}")
print(f"  [ASSUMPTION] Fundraise prob, amount, and timing are illustrative estimates")

# ─────────────────────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 72)
print("EXECUTIVE SUMMARY")
print("=" * 72)

print(f"""
  COMPANY:  Traws Pharma (TRAW) — Nano-cap clinical-stage biotech
  DATE:     2026-05-10
  PRICE:    ${price:.2f}  |  MARKET CAP: ${market_cap/1e6:.1f}M  |  CASH: ${cash/1e6:.1f}M

  ┌─────────────────────────────────────────────────────────────────┐
  │  METRIC                          VALUE         SIGNAL           │
  ├─────────────────────────────────────────────────────────────────┤
  │  Cash per Share                  ${cash_per_share:.3f}        Neutral      │
  │  P/Cash Ratio                    {p_cash_ratio:.2f}x          RED          │
  │  Enterprise Value                ${ev/1e6:.2f}M          RED (option)  │
  │  Runway (months)                 {runway_months:.1f}           RED          │
  │  Scenario-Weighted EV            ${ev_calc:.2f}         RED (neg)    │
  │  Sharpe-like (scenario)          {sharpe_like:.3f}          RED (<0)     │
  │  Kelly fraction (full)           {kelly_full*100:.2f}%          CAUTION      │
  │  Max Recommended Allocation      {recommended_max*100:.2f}%          (hard cap)   │
  │  P(Cash Depletion, 18mo)         {cumulative_depletion:.0%}           RED          │
  │  Red Flags (CRITICAL/HIGH)       {critical_count}/{high_count}              RED          │
  └─────────────────────────────────────────────────────────────────┘

  OVERALL QUANTITATIVE VERDICT: HIGH SPECULATIVE RISK / NEGATIVE EXPECTED VALUE

  The numbers do not support initiating or adding to a position at $2.09 from
  a risk-adjusted perspective. The dominant outcome (50% prob) is near-total
  loss from cash depletion + distressed financing. The scenario-weighted EV of
  ${ev_calc:.2f} is {abs(ev_return)*100:.1f}% below the current entry price of ${entry_price:.2f}.

  The May 8 volume spike (335x normal) is statistically extreme but does NOT
  change the fundamental terminal risk. It creates a short-term trading
  opportunity for momentum players with STRICT stop-losses, but it is NOT
  a long-term investment signal.

  Maximum allocation for risk-budget-conscious portfolios: {recommended_max*100:.2f}% of NAV.
  For most institutional mandates: 0% (outside risk tolerance parameters).

  DATA GAPS REQUIRING RESOLUTION BEFORE REVISED ANALYSIS:
  1. Exact PIPE size (shares issued, total $ raised in April 2026)
  2. Warrant terms: strike price, quantity, expiry, and exercise conditions
  3. Full balance sheet: total debt / liabilities (negative equity composition)
  4. Hantavirus program details: stage, timeline, regulatory pathway
  5. Ratutrelvir Phase 3 initiation timeline and capital requirements
  6. Lock-up and registration rights terms for PIPE investors
""")
