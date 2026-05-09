"""Valuation tools: calculate_dcf and calculate_financial_ratios."""

from __future__ import annotations

from typing import Any


def calculate_dcf(
    cash_flows: list[float],
    discount_rate: float,
    terminal_growth_rate: float = 0.02,
    shares_outstanding: float | None = None,
) -> dict[str, Any]:
    """Discounted Cash Flow (DCF) valuation.

    Parameters
    ----------
    cash_flows:
        Projected free cash flows for each future period (e.g. [100, 115, 132, ...]).
        At least one value required. All values in the same currency unit.
    discount_rate:
        Weighted average cost of capital (WACC) as a decimal (e.g. 0.10 for 10%).
    terminal_growth_rate:
        Perpetuity growth rate for terminal value (e.g. 0.02 for 2%).
    shares_outstanding:
        Optional number of shares outstanding to compute per-share intrinsic value.
    """
    if not cash_flows:
        return {"error": "cash_flows must contain at least one value."}
    if discount_rate <= terminal_growth_rate:
        return {"error": "discount_rate must be greater than terminal_growth_rate."}
    if discount_rate <= 0:
        return {"error": "discount_rate must be positive."}

    # Present value of explicit forecast period
    pv_cash_flows: list[dict[str, float]] = []
    total_pv = 0.0
    for i, cf in enumerate(cash_flows, start=1):
        pv = cf / (1 + discount_rate) ** i
        pv_cash_flows.append({"period": i, "cash_flow": round(cf, 2), "present_value": round(pv, 2)})
        total_pv += pv

    # Terminal value using Gordon Growth Model applied to the last cash flow
    last_cf = cash_flows[-1]
    terminal_value = last_cf * (1 + terminal_growth_rate) / (discount_rate - terminal_growth_rate)
    n = len(cash_flows)
    pv_terminal = terminal_value / (1 + discount_rate) ** n

    total_intrinsic_value = total_pv + pv_terminal

    result: dict[str, Any] = {
        "inputs": {
            "cash_flows": cash_flows,
            "discount_rate_pct": f"{discount_rate * 100:.2f}%",
            "terminal_growth_rate_pct": f"{terminal_growth_rate * 100:.2f}%",
            "forecast_periods": n,
        },
        "pv_of_forecast_cash_flows": round(total_pv, 2),
        "terminal_value": round(terminal_value, 2),
        "pv_of_terminal_value": round(pv_terminal, 2),
        "intrinsic_value": round(total_intrinsic_value, 2),
        "terminal_value_pct_of_total": f"{pv_terminal / total_intrinsic_value * 100:.1f}%",
        "period_breakdown": pv_cash_flows,
    }

    if shares_outstanding is not None and shares_outstanding > 0:
        result["intrinsic_value_per_share"] = round(total_intrinsic_value / shares_outstanding, 2)
        result["shares_outstanding"] = shares_outstanding

    return result


def calculate_financial_ratios(
    current_assets: float | None = None,
    current_liabilities: float | None = None,
    total_assets: float | None = None,
    total_liabilities: float | None = None,
    shareholders_equity: float | None = None,
    net_income: float | None = None,
    revenue: float | None = None,
    gross_profit: float | None = None,
    ebitda: float | None = None,
    interest_expense: float | None = None,
    inventory: float | None = None,
    accounts_receivable: float | None = None,
    cost_of_goods_sold: float | None = None,
    operating_income: float | None = None,
) -> dict[str, Any]:
    """Compute a comprehensive set of financial ratios from balance sheet / income statement inputs.

    Parameters
    ----------
    current_assets:
        Assets expected to be converted to cash within 12 months.
    current_liabilities:
        Obligations due within 12 months.
    total_assets:
        Sum of all assets on the balance sheet.
    total_liabilities:
        Sum of all liabilities on the balance sheet.
    shareholders_equity:
        Book value of equity (assets minus liabilities). Computed if not provided.
    net_income:
        Bottom-line profit for the period.
    revenue:
        Total net sales / revenue.
    gross_profit:
        Revenue minus cost of goods sold.
    ebitda:
        Earnings before interest, taxes, depreciation, and amortization.
    interest_expense:
        Interest expense for the period (used for interest coverage ratio).
    inventory:
        Inventory balance (used for inventory turnover and quick ratio).
    accounts_receivable:
        Accounts receivable balance (used for receivables turnover).
    cost_of_goods_sold:
        Cost of goods sold (used for inventory turnover).
    operating_income:
        Operating profit (EBIT) for the period.
    """
    ratios: dict[str, Any] = {}
    assessments: dict[str, str] = {}

    equity = shareholders_equity
    if equity is None and total_assets is not None and total_liabilities is not None:
        equity = total_assets - total_liabilities

    # ---- Liquidity ratios ----
    if current_assets is not None and current_liabilities is not None and current_liabilities != 0:
        cr = current_assets / current_liabilities
        ratios["current_ratio"] = round(cr, 3)
        assessments["current_ratio"] = (
            "Strong" if cr >= 2 else "Adequate" if cr >= 1 else "Weak — current liabilities exceed current assets"
        )

        # Quick ratio (exclude inventory)
        quick_assets = current_assets - (inventory or 0)
        qr = quick_assets / current_liabilities
        ratios["quick_ratio"] = round(qr, 3)
        assessments["quick_ratio"] = "Good" if qr >= 1 else "Below 1.0 — limited liquid coverage"

    # ---- Leverage ratios ----
    if total_liabilities is not None and equity is not None and equity != 0:
        dte = total_liabilities / equity
        ratios["debt_to_equity"] = round(dte, 3)
        assessments["debt_to_equity"] = (
            "Conservative" if dte < 0.5 else "Moderate" if dte < 1.5 else "High leverage"
        )

    if total_liabilities is not None and total_assets is not None and total_assets != 0:
        ratios["debt_ratio"] = round(total_liabilities / total_assets, 3)

    if ebitda is not None and interest_expense is not None and interest_expense != 0:
        icr = ebitda / interest_expense
        ratios["interest_coverage_ratio"] = round(icr, 2)
        assessments["interest_coverage"] = (
            "Very strong" if icr >= 5 else "Adequate" if icr >= 2 else "Concerning — limited ability to cover interest"
        )

    # ---- Profitability ratios ----
    if revenue is not None and revenue != 0:
        if gross_profit is not None:
            gm = gross_profit / revenue
            ratios["gross_margin"] = f"{gm * 100:.2f}%"
        if operating_income is not None:
            om = operating_income / revenue
            ratios["operating_margin"] = f"{om * 100:.2f}%"
        if net_income is not None:
            npm = net_income / revenue
            ratios["net_profit_margin"] = f"{npm * 100:.2f}%"
            assessments["profitability"] = (
                "Excellent (>20%)" if npm > 0.20
                else "Good (10–20%)" if npm > 0.10
                else "Below average (<10%)" if npm > 0
                else "Unprofitable"
            )
        if ebitda is not None:
            ratios["ebitda_margin"] = f"{ebitda / revenue * 100:.2f}%"

    if net_income is not None and equity is not None and equity != 0:
        roe = net_income / equity
        ratios["return_on_equity"] = f"{roe * 100:.2f}%"
        assessments["roe"] = (
            "Excellent (>20%)" if roe > 0.20 else "Good (10–20%)" if roe > 0.10 else "Below average"
        )

    if net_income is not None and total_assets is not None and total_assets != 0:
        ratios["return_on_assets"] = f"{net_income / total_assets * 100:.2f}%"

    if operating_income is not None and total_assets is not None and total_assets != 0:
        ratios["return_on_invested_capital_proxy"] = f"{operating_income / total_assets * 100:.2f}%"

    # ---- Efficiency ratios ----
    if revenue is not None and total_assets is not None and total_assets != 0:
        ratios["asset_turnover"] = round(revenue / total_assets, 3)

    if cost_of_goods_sold is not None and inventory is not None and inventory != 0:
        inv_turn = cost_of_goods_sold / inventory
        ratios["inventory_turnover"] = round(inv_turn, 2)
        ratios["days_inventory_outstanding"] = round(365 / inv_turn, 1)

    if revenue is not None and accounts_receivable is not None and accounts_receivable != 0:
        rec_turn = revenue / accounts_receivable
        ratios["receivables_turnover"] = round(rec_turn, 2)
        ratios["days_sales_outstanding"] = round(365 / rec_turn, 1)

    return {
        "ratios": ratios,
        "assessments": assessments,
        "note": "Ratios are only as reliable as the inputs provided. Ensure all figures use the same currency and period.",
    }
