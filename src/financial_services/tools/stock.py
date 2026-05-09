"""Stock analysis tools: analyze_stock and generate_financial_report."""

from __future__ import annotations

from typing import Any


def analyze_stock(ticker: str) -> dict[str, Any]:
    """Fetch real-time stock data via yfinance and return a structured analysis.

    Parameters
    ----------
    ticker:
        The stock ticker symbol (e.g. "AAPL", "MSFT", "GOOGL").

    Returns
    -------
    dict
        A dictionary containing price data, valuation metrics, and commentary.
    """
    try:
        import yfinance as yf
    except ImportError:
        return {"error": "yfinance is not installed. Run: pip install yfinance"}

    ticker_upper = ticker.strip().upper()
    stock = yf.Ticker(ticker_upper)

    try:
        info = stock.info
    except Exception as exc:
        return {"error": f"Failed to fetch data for {ticker_upper}: {exc}"}

    if not info or info.get("regularMarketPrice") is None and info.get("currentPrice") is None:
        return {"error": f"No data found for ticker '{ticker_upper}'. Check the symbol."}

    # ---- Core price / market data ----
    current_price = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose")
    prev_close = info.get("previousClose") or info.get("regularMarketPreviousClose")
    open_price = info.get("open") or info.get("regularMarketOpen")
    day_high = info.get("dayHigh") or info.get("regularMarketDayHigh")
    day_low = info.get("dayLow") or info.get("regularMarketDayLow")
    week_52_high = info.get("fiftyTwoWeekHigh")
    week_52_low = info.get("fiftyTwoWeekLow")
    volume = info.get("volume") or info.get("regularMarketVolume")
    avg_volume = info.get("averageVolume")

    # ---- Valuation metrics ----
    market_cap = info.get("marketCap")
    pe_ratio = info.get("trailingPE") or info.get("forwardPE")
    forward_pe = info.get("forwardPE")
    trailing_pe = info.get("trailingPE")
    eps = info.get("trailingEps")
    forward_eps = info.get("forwardEps")
    price_to_book = info.get("priceToBook")
    price_to_sales = info.get("priceToSalesTrailing12Months")
    ev_to_ebitda = info.get("enterpriseToEbitda")
    peg_ratio = info.get("pegRatio")

    # ---- Financials ----
    revenue = info.get("totalRevenue")
    gross_margins = info.get("grossMargins")
    operating_margins = info.get("operatingMargins")
    profit_margins = info.get("profitMargins")
    roe = info.get("returnOnEquity")
    roa = info.get("returnOnAssets")
    debt_to_equity = info.get("debtToEquity")
    current_ratio = info.get("currentRatio")
    dividend_yield = info.get("dividendYield")
    beta = info.get("beta")

    # ---- Growth / analyst data ----
    target_mean_price = info.get("targetMeanPrice")
    recommendation = info.get("recommendationKey", "").upper()
    earnings_growth = info.get("earningsGrowth")
    revenue_growth = info.get("revenueGrowth")

    # ---- Derived valuation commentary ----
    commentary_lines: list[str] = []

    if trailing_pe is not None:
        if trailing_pe < 0:
            commentary_lines.append("Company is currently unprofitable (negative trailing P/E).")
        elif trailing_pe < 15:
            commentary_lines.append(f"Trailing P/E of {trailing_pe:.1f}x is below the market average, suggesting potential undervaluation.")
        elif trailing_pe < 25:
            commentary_lines.append(f"Trailing P/E of {trailing_pe:.1f}x is roughly in line with the broader market.")
        else:
            commentary_lines.append(f"Trailing P/E of {trailing_pe:.1f}x is elevated; the market is pricing in significant growth.")

    if peg_ratio is not None and peg_ratio > 0:
        if peg_ratio < 1:
            commentary_lines.append(f"PEG ratio of {peg_ratio:.2f} suggests the stock may be undervalued relative to its growth rate.")
        elif peg_ratio < 2:
            commentary_lines.append(f"PEG ratio of {peg_ratio:.2f} is reasonable for a growth company.")
        else:
            commentary_lines.append(f"PEG ratio of {peg_ratio:.2f} indicates the stock may be pricey relative to growth.")

    if week_52_high and current_price:
        pct_from_high = (current_price - week_52_high) / week_52_high * 100
        commentary_lines.append(
            f"Current price is {abs(pct_from_high):.1f}% {'below' if pct_from_high < 0 else 'above'} its 52-week high."
        )

    if beta is not None:
        if beta < 0.8:
            commentary_lines.append(f"Beta of {beta:.2f} indicates lower volatility than the market (defensive stock).")
        elif beta < 1.2:
            commentary_lines.append(f"Beta of {beta:.2f} indicates market-like volatility.")
        else:
            commentary_lines.append(f"Beta of {beta:.2f} indicates higher volatility than the broader market.")

    if profit_margins is not None:
        pct = profit_margins * 100
        if pct < 5:
            commentary_lines.append(f"Net profit margin of {pct:.1f}% is thin.")
        elif pct < 15:
            commentary_lines.append(f"Net profit margin of {pct:.1f}% is moderate.")
        else:
            commentary_lines.append(f"Net profit margin of {pct:.1f}% is strong.")

    if recommendation:
        commentary_lines.append(f"Analyst consensus: {recommendation}.")
    if target_mean_price and current_price:
        upside = (target_mean_price - current_price) / current_price * 100
        commentary_lines.append(
            f"Mean analyst price target of ${target_mean_price:.2f} implies "
            f"{'upside' if upside >= 0 else 'downside'} of {abs(upside):.1f}%."
        )

    def _fmt_large(n: float | None, unit: str = "") -> str | None:
        if n is None:
            return None
        if abs(n) >= 1e12:
            return f"${n/1e12:.2f}T{unit}"
        if abs(n) >= 1e9:
            return f"${n/1e9:.2f}B{unit}"
        if abs(n) >= 1e6:
            return f"${n/1e6:.2f}M{unit}"
        return f"${n:,.0f}{unit}"

    def _pct(v: float | None) -> str | None:
        return f"{v*100:.2f}%" if v is not None else None

    return {
        "ticker": ticker_upper,
        "company_name": info.get("longName") or info.get("shortName", ticker_upper),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "exchange": info.get("exchange"),
        "currency": info.get("currency", "USD"),
        "price": {
            "current": current_price,
            "previous_close": prev_close,
            "open": open_price,
            "day_high": day_high,
            "day_low": day_low,
            "52_week_high": week_52_high,
            "52_week_low": week_52_low,
            "volume": volume,
            "avg_volume": avg_volume,
        },
        "valuation": {
            "market_cap": _fmt_large(market_cap),
            "market_cap_raw": market_cap,
            "trailing_pe": trailing_pe,
            "forward_pe": forward_pe,
            "eps_trailing": eps,
            "eps_forward": forward_eps,
            "price_to_book": price_to_book,
            "price_to_sales": price_to_sales,
            "ev_to_ebitda": ev_to_ebitda,
            "peg_ratio": peg_ratio,
        },
        "financials": {
            "revenue": _fmt_large(revenue),
            "gross_margin": _pct(gross_margins),
            "operating_margin": _pct(operating_margins),
            "net_profit_margin": _pct(profit_margins),
            "roe": _pct(roe),
            "roa": _pct(roa),
            "debt_to_equity": debt_to_equity,
            "current_ratio": current_ratio,
            "dividend_yield": _pct(dividend_yield),
            "beta": beta,
        },
        "growth": {
            "earnings_growth_yoy": _pct(earnings_growth),
            "revenue_growth_yoy": _pct(revenue_growth),
        },
        "analyst": {
            "recommendation": recommendation or None,
            "target_mean_price": target_mean_price,
            "target_high_price": info.get("targetHighPrice"),
            "target_low_price": info.get("targetLowPrice"),
            "number_of_analyst_opinions": info.get("numberOfAnalystOpinions"),
        },
        "valuation_commentary": commentary_lines,
    }


def generate_financial_report(
    company_name: str,
    ticker: str | None = None,
    revenue: float | None = None,
    net_income: float | None = None,
    total_assets: float | None = None,
    total_liabilities: float | None = None,
    shareholders_equity: float | None = None,
    current_assets: float | None = None,
    current_liabilities: float | None = None,
    ebitda: float | None = None,
    free_cash_flow: float | None = None,
    revenue_growth_rate: float | None = None,
    industry: str | None = None,
    fiscal_year: int | None = None,
) -> dict[str, Any]:
    """Generate a structured financial analysis report for a company.

    All monetary inputs are assumed to be in the same currency (typically USD millions).

    Parameters
    ----------
    company_name:
        Full legal or common name of the company.
    ticker:
        Optional stock ticker symbol for reference.
    revenue:
        Total revenue / net sales for the period.
    net_income:
        Net income (profit) for the period.
    total_assets:
        Total assets from the balance sheet.
    total_liabilities:
        Total liabilities from the balance sheet.
    shareholders_equity:
        Total shareholders' equity (can be derived if not provided).
    current_assets:
        Current assets (liquid within 12 months).
    current_liabilities:
        Current liabilities (due within 12 months).
    ebitda:
        Earnings before interest, taxes, depreciation, and amortization.
    free_cash_flow:
        Operating cash flow minus capital expenditures.
    revenue_growth_rate:
        Year-over-year revenue growth as a decimal (e.g. 0.15 for 15%).
    industry:
        Industry or sector for context.
    fiscal_year:
        The fiscal year being analyzed.
    """

    report: dict[str, Any] = {
        "report_title": f"Financial Analysis Report: {company_name}",
        "company": company_name,
        "ticker": ticker,
        "industry": industry,
        "fiscal_year": fiscal_year,
        "currency_note": "All monetary values in the same unit as provided (typically USD millions).",
    }

    # ---- Derived equity ----
    equity = shareholders_equity
    if equity is None and total_assets is not None and total_liabilities is not None:
        equity = total_assets - total_liabilities

    # ---- Ratio calculations ----
    ratios: dict[str, Any] = {}

    if net_income is not None and revenue is not None and revenue != 0:
        ratios["net_profit_margin"] = f"{net_income / revenue * 100:.2f}%"

    if ebitda is not None and revenue is not None and revenue != 0:
        ratios["ebitda_margin"] = f"{ebitda / revenue * 100:.2f}%"

    if current_assets is not None and current_liabilities is not None and current_liabilities != 0:
        cr = current_assets / current_liabilities
        ratios["current_ratio"] = round(cr, 2)
        if cr >= 2.0:
            ratios["liquidity_assessment"] = "Strong liquidity position."
        elif cr >= 1.0:
            ratios["liquidity_assessment"] = "Adequate liquidity."
        else:
            ratios["liquidity_assessment"] = "Potential liquidity concern — current liabilities exceed current assets."

    if total_liabilities is not None and equity is not None and equity != 0:
        dte = total_liabilities / equity
        ratios["debt_to_equity"] = round(dte, 2)
        if dte < 0.5:
            ratios["leverage_assessment"] = "Conservative leverage, financially resilient."
        elif dte < 1.5:
            ratios["leverage_assessment"] = "Moderate leverage, typical for many industries."
        else:
            ratios["leverage_assessment"] = "High leverage; closely monitor debt service capacity."

    if net_income is not None and equity is not None and equity != 0:
        roe = net_income / equity
        ratios["roe"] = f"{roe * 100:.2f}%"
        if roe > 0.20:
            ratios["roe_assessment"] = "Excellent return on equity — management is highly effective at generating profit from equity."
        elif roe > 0.10:
            ratios["roe_assessment"] = "Good return on equity."
        elif roe > 0:
            ratios["roe_assessment"] = "Below-average return on equity."
        else:
            ratios["roe_assessment"] = "Negative ROE indicates the company is destroying shareholder value."

    if net_income is not None and total_assets is not None and total_assets != 0:
        roa = net_income / total_assets
        ratios["roa"] = f"{roa * 100:.2f}%"

    if revenue is not None and total_assets is not None and total_assets != 0:
        ratios["asset_turnover"] = round(revenue / total_assets, 2)

    report["key_ratios"] = ratios

    # ---- Summary metrics ----
    summary: dict[str, Any] = {}
    if revenue is not None:
        summary["revenue"] = revenue
    if net_income is not None:
        summary["net_income"] = net_income
    if ebitda is not None:
        summary["ebitda"] = ebitda
    if free_cash_flow is not None:
        summary["free_cash_flow"] = free_cash_flow
    if total_assets is not None:
        summary["total_assets"] = total_assets
    if equity is not None:
        summary["shareholders_equity"] = equity
    if revenue_growth_rate is not None:
        summary["revenue_growth_yoy"] = f"{revenue_growth_rate * 100:.1f}%"
    report["financial_summary"] = summary

    # ---- Narrative sections ----
    strengths: list[str] = []
    concerns: list[str] = []
    highlights: list[str] = []

    if revenue_growth_rate is not None:
        if revenue_growth_rate > 0.20:
            strengths.append(f"High revenue growth of {revenue_growth_rate*100:.1f}% YoY indicates strong demand.")
        elif revenue_growth_rate > 0.05:
            highlights.append(f"Solid revenue growth of {revenue_growth_rate*100:.1f}% YoY.")
        elif revenue_growth_rate < 0:
            concerns.append(f"Revenue declined {abs(revenue_growth_rate)*100:.1f}% YoY — top-line pressure warrants monitoring.")

    if net_income is not None and revenue is not None and revenue != 0:
        margin = net_income / revenue * 100
        if margin > 20:
            strengths.append(f"Exceptional net profit margin of {margin:.1f}%.")
        elif margin > 10:
            highlights.append(f"Healthy net profit margin of {margin:.1f}%.")
        elif margin < 0:
            concerns.append(f"Negative net profit margin ({margin:.1f}%) — company is unprofitable.")

    if free_cash_flow is not None:
        if free_cash_flow > 0:
            strengths.append(f"Positive free cash flow of {free_cash_flow:,.0f} provides financial flexibility.")
        else:
            concerns.append(f"Negative free cash flow ({free_cash_flow:,.0f}) indicates cash burn.")

    cr_val = ratios.get("current_ratio")
    if isinstance(cr_val, (int, float)):
        if cr_val < 1.0:
            concerns.append("Current ratio below 1.0 raises short-term liquidity questions.")

    dte_val = ratios.get("debt_to_equity")
    if isinstance(dte_val, (int, float)):
        if dte_val > 2.0:
            concerns.append(f"High debt-to-equity ratio of {dte_val:.2f}x warrants attention.")

    report["analysis"] = {
        "strengths": strengths,
        "highlights": highlights,
        "concerns": concerns,
    }

    # ---- Overall assessment ----
    score = len(strengths) * 2 + len(highlights) - len(concerns) * 2
    if score >= 4:
        overall = "Strong"
    elif score >= 1:
        overall = "Positive"
    elif score == 0:
        overall = "Neutral"
    elif score >= -2:
        overall = "Cautious"
    else:
        overall = "Weak"

    report["overall_assessment"] = overall
    report["note"] = (
        "This report is generated from the provided inputs only and should not be used "
        "as the sole basis for investment decisions. Always consult a qualified financial advisor."
    )
    return report
