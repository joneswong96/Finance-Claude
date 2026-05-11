"""Valuation tools: calculate_dcf and calculate_financial_ratios."""

from __future__ import annotations

from typing import Any


def calculate_dcf(
    cash_flows: list[float],
    discount_rate: float,
    terminal_growth_rate: float,
    growth_rate: float = 0.0,
    shares_outstanding: float | None = None,
    net_debt: float = 0.0,
) -> dict[str, Any]:
    """Perform a Discounted Cash Flow (DCF) valuation.

    Parameters
    ----------
    cash_flows:
        List of projected free cash flows for each forecast period (e.g. years 1-5).
        If *growth_rate* is non-zero and this list has only one element, the single
        value is used as Year-1 FCF and subsequent years are grown at *growth_rate*.
    discount_rate:
        Weighted-average cost of capital (WACC) as a decimal (e.g. 0.10 for 10%).
    terminal_growth_rate:
        Long-term perpetuity growth rate for terminal value (e.g. 0.025 for 2.5%).
        Must be strictly less than *discount_rate*.
    growth_rate:
        Optional year-over-year growth rate applied to *cash_flows* if you want the
        model to auto-expand a single seed FCF into a multi-year projection.
        Ignored when *cash_flows* already has multiple entries.
    shares_outstanding:
        Optional number of shares outstanding.  When provided, equity value per
        share is also returned.
    net_debt:
        Net debt (total debt minus cash).  Subtracted from enterprise value to
        derive equity value.  Can be negative if the company is net-cash.
    """

    if discount_rate <= 0:
        return {"error": "discount_rate must be positive."}
    if terminal_growth_rate >= discount_rate:
        return {
            "error": (
                f"terminal_growth_rate ({terminal_growth_rate}) must be strictly less than "
                f"discount_rate ({discount_rate}) to avoid an infinite or negative terminal value."
            )
        }
    if not cash_flows:
        return {"error": "cash_flows list must not be empty."}

    # Auto-expand seed FCF if growth_rate is provided and only one cash flow given
    if len(cash_flows) == 1 and growth_rate != 0.0:
        seed = cash_flows[0]
        expanded: list[float] = [seed]
        for _ in range(4):  # default 5-year projection
            expanded.append(expanded[-1] * (1 + growth_rate))
        cash_flows = expanded

    n = len(cash_flows)
    pv_details: list[dict[str, float]] = []
    total_pv_fcf = 0.0

    for i, fcf in enumerate(cash_flows, start=1):
        pv = fcf / (1 + discount_rate) ** i
        total_pv_fcf += pv
        pv_details.append(
            {
                "year": i,
                "free_cash_flow": round(fcf, 2),
                "present_value": round(pv, 2),
            }
        )

    # Gordon Growth Model terminal value at end of forecast horizon
    final_fcf = cash_flows[-1]
    terminal_fcf = final_fcf * (1 + terminal_growth_rate)
    terminal_value = terminal_fcf / (discount_rate - terminal_growth_rate)
    pv_terminal_value = terminal_value / (1 + discount_rate) ** n

    enterprise_value = total_pv_fcf + pv_terminal_value
    equity_value = enterprise_value - net_debt

    terminal_value_pct = (pv_terminal_value / enterprise_value * 100) if enterprise_value != 0 else 0.0

    result: dict[str, Any] = {
        "inputs": {
            "forecast_years": n,
            "discount_rate": f"{discount_rate * 100:.2f}%",
            "terminal_growth_rate": f"{terminal_growth_rate * 100:.2f}%",
            "net_debt": net_debt,
        },
        "cash_flow_projections": pv_details,
        "pv_of_forecast_cash_flows": round(total_pv_fcf, 2),
        "terminal_value": round(terminal_value, 2),
        "pv_of_terminal_value": round(pv_terminal_value, 2),
        "terminal_value_pct_of_ev": f"{terminal_value_pct:.1f}%",
        "enterprise_value": round(enterprise_value, 2),
        "net_debt": net_debt,
        "equity_value": round(equity_value, 2),
    }

    if shares_outstanding and shares_outstanding > 0:
        intrinsic_per_share = equity_value / shares_outstanding
        result["shares_outstanding"] = shares_outstanding
        result["intrinsic_value_per_share"] = round(intrinsic_per_share, 2)

    # Commentary
    notes: list[str] = []
    if terminal_value_pct > 80:
        notes.append(
            f"Terminal value represents {terminal_value_pct:.0f}% of enterprise value — "
            "the valuation is highly sensitive to the terminal growth rate assumption."
        )
    elif terminal_value_pct > 60:
        notes.append(
            f"Terminal value represents {terminal_value_pct:.0f}% of enterprise value, "
            "which is typical for DCF models."
        )

    if equity_value < 0:
        notes.append(
            "Equity value is negative, implying net debt exceeds enterprise value. "
            "This may indicate financial distress or a highly leveraged position."
        )

    spread = discount_rate - terminal_growth_rate
    if spread < 0.03:
        notes.append(
            f"The spread between discount rate and terminal growth rate is only "
            f"{spread*100:.1f}bps — small changes in assumptions produce large swings in value."
        )

    result["notes"] = notes
    return result


def calculate_financial_ratios(
    # Income statement
    revenue: float | None = None,
    gross_profit: float | None = None,
    operating_income: float | None = None,
    ebitda: float | None = None,
    net_income: float | None = None,
    interest_expense: float | None = None,
    income_tax_expense: float | None = None,
    depreciation_amortization: float | None = None,
    # Balance sheet
    total_assets: float | None = None,
    current_assets: float | None = None,
    cash_and_equivalents: float | None = None,
    inventory: float | None = None,
    accounts_receivable: float | None = None,
    total_liabilities: float | None = None,
    current_liabilities: float | None = None,
    total_debt: float | None = None,
    shareholders_equity: float | None = None,
    # Cash flow
    operating_cash_flow: float | None = None,
    capital_expenditures: float | None = None,
    # Market data
    market_cap: float | None = None,
    share_price: float | None = None,
    shares_outstanding: float | None = None,
    earnings_per_share: float | None = None,
) -> dict[str, Any]:
    """Compute a comprehensive set of financial ratios from income statement and balance sheet data.

    All monetary inputs must be in the same unit (e.g., all in USD millions).

    Parameters
    ----------
    revenue:
        Total revenue / net sales.
    gross_profit:
        Revenue minus cost of goods sold.
    operating_income:
        EBIT (earnings before interest and taxes).
    ebitda:
        Earnings before interest, taxes, depreciation, amortization.
    net_income:
        Bottom-line net profit.
    interest_expense:
        Interest paid on debt.
    income_tax_expense:
        Income taxes paid.
    depreciation_amortization:
        D&A expense for the period.
    total_assets:
        Total assets from balance sheet.
    current_assets:
        Assets convertible to cash within 12 months.
    cash_and_equivalents:
        Cash and short-term investments.
    inventory:
        Inventory value.
    accounts_receivable:
        Amounts owed by customers.
    total_liabilities:
        All liabilities.
    current_liabilities:
        Liabilities due within 12 months.
    total_debt:
        Short-term + long-term debt.
    shareholders_equity:
        Book value of equity (derived if not provided).
    operating_cash_flow:
        Cash from operations.
    capital_expenditures:
        Capex (provide as positive number).
    market_cap:
        Market capitalisation.
    share_price:
        Current share price.
    shares_outstanding:
        Total shares outstanding.
    earnings_per_share:
        EPS (derived if not provided).
    """

    def _safe_div(numerator: float | None, denominator: float | None) -> float | None:
        if numerator is None or denominator is None or denominator == 0:
            return None
        return numerator / denominator

    def _pct(v: float | None) -> str | None:
        return f"{v * 100:.2f}%" if v is not None else None

    def _r2(v: float | None) -> float | None:
        return round(v, 4) if v is not None else None

    # Derive equity if not provided
    equity = shareholders_equity
    if equity is None and total_assets is not None and total_liabilities is not None:
        equity = total_assets - total_liabilities

    # Derive free cash flow
    fcf: float | None = None
    if operating_cash_flow is not None and capital_expenditures is not None:
        fcf = operating_cash_flow - abs(capital_expenditures)

    # Derive net debt
    net_debt: float | None = None
    if total_debt is not None and cash_and_equivalents is not None:
        net_debt = total_debt - cash_and_equivalents
    elif total_debt is not None:
        net_debt = total_debt

    # ---- Liquidity ratios ----
    liquidity: dict[str, Any] = {}

    current_ratio = _safe_div(current_assets, current_liabilities)
    if current_ratio is not None:
        liquidity["current_ratio"] = _r2(current_ratio)
        if current_ratio >= 2.0:
            liquidity["current_ratio_note"] = "Strong — ample short-term assets to cover liabilities."
        elif current_ratio >= 1.0:
            liquidity["current_ratio_note"] = "Adequate — can meet near-term obligations."
        else:
            liquidity["current_ratio_note"] = "Below 1.0 — potential short-term liquidity risk."

    quick_assets: float | None = None
    if current_assets is not None and inventory is not None:
        quick_assets = current_assets - inventory
    elif current_assets is not None:
        quick_assets = current_assets

    quick_ratio = _safe_div(quick_assets, current_liabilities)
    if quick_ratio is not None:
        liquidity["quick_ratio"] = _r2(quick_ratio)
        if quick_ratio >= 1.0:
            liquidity["quick_ratio_note"] = "Good quick liquidity without relying on inventory."
        else:
            liquidity["quick_ratio_note"] = "Quick ratio below 1.0 may indicate reliance on inventory."

    cash_ratio = _safe_div(cash_and_equivalents, current_liabilities)
    if cash_ratio is not None:
        liquidity["cash_ratio"] = _r2(cash_ratio)

    # ---- Leverage / solvency ratios ----
    leverage: dict[str, Any] = {}

    dte = _safe_div(total_debt, equity)
    if dte is not None:
        leverage["debt_to_equity"] = _r2(dte)
        if dte < 0.5:
            leverage["debt_to_equity_note"] = "Conservative leverage."
        elif dte < 1.5:
            leverage["debt_to_equity_note"] = "Moderate leverage."
        else:
            leverage["debt_to_equity_note"] = "High leverage — elevated financial risk."

    total_dte = _safe_div(total_liabilities, equity)
    if total_dte is not None:
        leverage["total_liabilities_to_equity"] = _r2(total_dte)

    debt_to_assets = _safe_div(total_debt, total_assets)
    if debt_to_assets is not None:
        leverage["debt_to_assets"] = _r2(debt_to_assets)

    ebit = operating_income
    if ebit is None and ebitda is not None and depreciation_amortization is not None:
        ebit = ebitda - depreciation_amortization

    interest_coverage = _safe_div(ebit, interest_expense)
    if interest_coverage is not None:
        leverage["interest_coverage"] = _r2(interest_coverage)
        if interest_coverage >= 5:
            leverage["interest_coverage_note"] = "Comfortable ability to service interest payments."
        elif interest_coverage >= 2:
            leverage["interest_coverage_note"] = "Adequate interest coverage."
        else:
            leverage["interest_coverage_note"] = "Low interest coverage — debt service is a concern."

    if net_debt is not None and ebitda is not None and ebitda != 0:
        leverage["net_debt_to_ebitda"] = _r2(net_debt / ebitda)

    # ---- Profitability ratios ----
    profitability: dict[str, Any] = {}

    gross_margin = _safe_div(gross_profit, revenue)
    if gross_margin is not None:
        profitability["gross_margin"] = _pct(gross_margin)

    operating_margin = _safe_div(operating_income or ebit, revenue)
    if operating_margin is not None:
        profitability["operating_margin"] = _pct(operating_margin)

    ebitda_margin = _safe_div(ebitda, revenue)
    if ebitda_margin is not None:
        profitability["ebitda_margin"] = _pct(ebitda_margin)

    net_margin = _safe_div(net_income, revenue)
    if net_margin is not None:
        profitability["net_profit_margin"] = _pct(net_margin)
        if net_margin and net_margin > 0.20:
            profitability["net_margin_note"] = "Exceptional profitability."
        elif net_margin and net_margin > 0.10:
            profitability["net_margin_note"] = "Strong profitability."
        elif net_margin and net_margin > 0:
            profitability["net_margin_note"] = "Moderate profitability."
        else:
            profitability["net_margin_note"] = "Company is unprofitable."

    roe = _safe_div(net_income, equity)
    if roe is not None:
        profitability["roe"] = _pct(roe)
        if roe and roe > 0.20:
            profitability["roe_note"] = "Excellent return on equity."
        elif roe and roe > 0.10:
            profitability["roe_note"] = "Good return on equity."

    roa = _safe_div(net_income, total_assets)
    if roa is not None:
        profitability["roa"] = _pct(roa)

    roic_numerator = (net_income or 0) + (interest_expense or 0) * (1 - 0.25)
    invested_capital = (equity or 0) + (total_debt or 0) - (cash_and_equivalents or 0)
    if equity is not None and total_debt is not None and invested_capital != 0 and net_income is not None:
        roic = roic_numerator / invested_capital
        profitability["roic"] = _pct(roic)

    fcf_margin = _safe_div(fcf, revenue)
    if fcf_margin is not None:
        profitability["fcf_margin"] = _pct(fcf_margin)

    # ---- Efficiency ratios ----
    efficiency: dict[str, Any] = {}

    asset_turnover = _safe_div(revenue, total_assets)
    if asset_turnover is not None:
        efficiency["asset_turnover"] = _r2(asset_turnover)

    if accounts_receivable is not None and revenue is not None and revenue != 0:
        ar_turnover = revenue / accounts_receivable
        efficiency["accounts_receivable_turnover"] = _r2(ar_turnover)
        dso = 365 / ar_turnover
        efficiency["days_sales_outstanding"] = _r2(dso)

    if inventory is not None:
        cogs = (revenue or 0) - (gross_profit or 0) if revenue and gross_profit else None
        inv_turnover = _safe_div(cogs, inventory)
        if inv_turnover is not None:
            efficiency["inventory_turnover"] = _r2(inv_turnover)
            efficiency["days_inventory_outstanding"] = _r2(365 / inv_turnover)

    equity_multiplier = _safe_div(total_assets, equity)
    if equity_multiplier is not None:
        efficiency["equity_multiplier"] = _r2(equity_multiplier)

    # ---- Valuation ratios (if market data is provided) ----
    valuation: dict[str, Any] = {}

    price = share_price
    eps = earnings_per_share
    if eps is None and net_income is not None and shares_outstanding is not None and shares_outstanding != 0:
        eps = net_income / shares_outstanding

    if price is None and market_cap is not None and shares_outstanding is not None and shares_outstanding != 0:
        price = market_cap / shares_outstanding

    pe = _safe_div(price, eps)
    if pe is not None:
        valuation["pe_ratio"] = _r2(pe)

    if market_cap is not None:
        if revenue is not None and revenue != 0:
            valuation["price_to_sales"] = _r2(market_cap / revenue)
        if equity is not None and equity != 0:
            valuation["price_to_book"] = _r2(market_cap / equity)
        if fcf is not None and fcf != 0:
            valuation["price_to_fcf"] = _r2(market_cap / fcf)
        enterprise_value = market_cap + (net_debt or 0)
        if ebitda is not None and ebitda != 0:
            valuation["ev_to_ebitda"] = _r2(enterprise_value / ebitda)
        if revenue is not None and revenue != 0:
            valuation["ev_to_revenue"] = _r2(enterprise_value / revenue)
        valuation["enterprise_value"] = round(enterprise_value, 2)

    # ---- DuPont decomposition ----
    dupont: dict[str, Any] = {}
    if net_margin is not None and asset_turnover is not None and equity_multiplier is not None:
        dupont["net_profit_margin"] = _pct(net_margin)
        dupont["asset_turnover"] = _r2(asset_turnover)
        dupont["equity_multiplier"] = _r2(equity_multiplier)
        dupont["roe_dupont"] = _pct(net_margin * asset_turnover * equity_multiplier)
        dupont["note"] = "ROE = Net Margin × Asset Turnover × Equity Multiplier"

    result: dict[str, Any] = {}
    if liquidity:
        result["liquidity_ratios"] = liquidity
    if leverage:
        result["leverage_ratios"] = leverage
    if profitability:
        result["profitability_ratios"] = profitability
    if efficiency:
        result["efficiency_ratios"] = efficiency
    if valuation:
        result["valuation_ratios"] = valuation
    if dupont:
        result["dupont_analysis"] = dupont

    if not result:
        return {"error": "Insufficient data provided — please supply at least some income statement or balance sheet figures."}

    result["note"] = "All ratios calculated from provided inputs. Ensure all monetary values are in the same unit."
    return result
