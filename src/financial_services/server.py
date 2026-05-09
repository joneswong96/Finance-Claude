"""MCP server entry point for the financial-services plugin."""

from __future__ import annotations

import sys
from typing import Any

from mcp.server.fastmcp import FastMCP

from financial_services.tools.stock import analyze_stock, generate_financial_report
from financial_services.tools.valuation import calculate_dcf, calculate_financial_ratios
from financial_services.tools.portfolio import assess_portfolio
from financial_services.tools.calculators import (
    compound_interest,
    loan_amortization,
    convert_currency,
)

# ---------------------------------------------------------------------------
# Server instantiation
# ---------------------------------------------------------------------------

mcp = FastMCP(
    "financial-analysis",
    instructions=(
        "A financial analysis assistant providing tools for stock analysis, "
        "DCF valuation, portfolio assessment, financial ratio calculation, "
        "report generation, currency conversion, compound interest, and loan "
        "amortization. All stock data is fetched live via yfinance unless "
        "a current_price override is supplied."
    ),
)

# ---------------------------------------------------------------------------
# Tool registrations
# ---------------------------------------------------------------------------


@mcp.tool()
def analyze_stock_tool(ticker: str) -> dict[str, Any]:
    """Analyze a stock by ticker symbol.

    Fetches live data from Yahoo Finance and returns P/E ratio, EPS,
    52-week high/low, market cap, valuation metrics, analyst consensus,
    and a qualitative valuation commentary.

    Args:
        ticker: Stock ticker symbol (e.g. "AAPL", "MSFT", "GOOGL").

    Returns:
        Structured dict with price, valuation, financials, growth, analyst
        data, and commentary sections.
    """
    return analyze_stock(ticker)


@mcp.tool()
def calculate_dcf_tool(
    cash_flows: list[float],
    discount_rate: float,
    terminal_growth_rate: float,
    growth_rate: float = 0.0,
    shares_outstanding: float | None = None,
    net_debt: float = 0.0,
) -> dict[str, Any]:
    """Perform a Discounted Cash Flow (DCF) valuation.

    Args:
        cash_flows: Projected free cash flows for each forecast year (e.g. [100, 110, 121]).
            Provide a single-element list with growth_rate to auto-project 5 years.
        discount_rate: WACC as a decimal (e.g. 0.10 for 10%).
        terminal_growth_rate: Perpetuity growth rate (e.g. 0.025 for 2.5%).
            Must be less than discount_rate.
        growth_rate: Optional YoY FCF growth rate to auto-expand a single seed FCF.
        shares_outstanding: Optional shares count for per-share intrinsic value.
        net_debt: Net debt (debt minus cash) to subtract from enterprise value.

    Returns:
        DCF results: present values, terminal value, enterprise value, equity value,
        optional intrinsic value per share, and sensitivity notes.
    """
    return calculate_dcf(
        cash_flows=cash_flows,
        discount_rate=discount_rate,
        terminal_growth_rate=terminal_growth_rate,
        growth_rate=growth_rate,
        shares_outstanding=shares_outstanding,
        net_debt=net_debt,
    )


@mcp.tool()
def assess_portfolio_tool(
    holdings: list[dict[str, Any]],
    risk_free_rate: float = 0.05,
    fetch_live_prices: bool = True,
) -> dict[str, Any]:
    """Assess a stock portfolio's value, allocation, unrealised P&L, and risk.

    Args:
        holdings: List of holding dicts. Each must have:
            - ticker (str): stock symbol
            - shares (float): number of shares
            - avg_cost (float): average cost basis per share
            Optional:
            - current_price (float): override live price lookup
        risk_free_rate: Annual risk-free rate as a decimal (default 0.05 = 5%).
        fetch_live_prices: Fetch live prices via yfinance (default True).

    Returns:
        Portfolio summary (total value, P&L, risk level) and per-holding breakdown
        with allocation percentages and unrealised gains/losses.
    """
    return assess_portfolio(
        holdings=holdings,
        risk_free_rate=risk_free_rate,
        fetch_live_prices=fetch_live_prices,
    )


@mcp.tool()
def calculate_financial_ratios_tool(
    revenue: float | None = None,
    gross_profit: float | None = None,
    operating_income: float | None = None,
    ebitda: float | None = None,
    net_income: float | None = None,
    interest_expense: float | None = None,
    income_tax_expense: float | None = None,
    depreciation_amortization: float | None = None,
    total_assets: float | None = None,
    current_assets: float | None = None,
    cash_and_equivalents: float | None = None,
    inventory: float | None = None,
    accounts_receivable: float | None = None,
    total_liabilities: float | None = None,
    current_liabilities: float | None = None,
    total_debt: float | None = None,
    shareholders_equity: float | None = None,
    operating_cash_flow: float | None = None,
    capital_expenditures: float | None = None,
    market_cap: float | None = None,
    share_price: float | None = None,
    shares_outstanding: float | None = None,
    earnings_per_share: float | None = None,
) -> dict[str, Any]:
    """Compute comprehensive financial ratios from income statement and balance sheet data.

    Calculates liquidity ratios (current, quick, cash), leverage ratios
    (debt-to-equity, interest coverage, net debt/EBITDA), profitability ratios
    (gross/operating/net margins, ROE, ROA, ROIC), efficiency ratios (asset
    turnover, DSO, inventory turnover), valuation ratios (P/E, EV/EBITDA,
    P/B, P/FCF), and DuPont decomposition.

    Args:
        revenue: Total revenue / net sales.
        gross_profit: Revenue minus cost of goods sold.
        operating_income: EBIT (earnings before interest and taxes).
        ebitda: Earnings before interest, taxes, depreciation, amortization.
        net_income: Bottom-line net profit.
        interest_expense: Interest paid on debt.
        income_tax_expense: Income taxes paid.
        depreciation_amortization: D&A expense for the period.
        total_assets: Total assets from balance sheet.
        current_assets: Assets convertible to cash within 12 months.
        cash_and_equivalents: Cash and short-term investments.
        inventory: Inventory value.
        accounts_receivable: Amounts owed by customers.
        total_liabilities: All liabilities.
        current_liabilities: Liabilities due within 12 months.
        total_debt: Short-term + long-term debt.
        shareholders_equity: Book value of equity (derived if not provided).
        operating_cash_flow: Cash from operations.
        capital_expenditures: Capex (provide as positive number).
        market_cap: Market capitalisation.
        share_price: Current share price.
        shares_outstanding: Total shares outstanding.
        earnings_per_share: EPS (derived if not provided).

    Returns:
        Dict with sections: liquidity_ratios, leverage_ratios, profitability_ratios,
        efficiency_ratios, valuation_ratios, dupont_analysis.
    """
    return calculate_financial_ratios(
        revenue=revenue,
        gross_profit=gross_profit,
        operating_income=operating_income,
        ebitda=ebitda,
        net_income=net_income,
        interest_expense=interest_expense,
        income_tax_expense=income_tax_expense,
        depreciation_amortization=depreciation_amortization,
        total_assets=total_assets,
        current_assets=current_assets,
        cash_and_equivalents=cash_and_equivalents,
        inventory=inventory,
        accounts_receivable=accounts_receivable,
        total_liabilities=total_liabilities,
        current_liabilities=current_liabilities,
        total_debt=total_debt,
        shareholders_equity=shareholders_equity,
        operating_cash_flow=operating_cash_flow,
        capital_expenditures=capital_expenditures,
        market_cap=market_cap,
        share_price=share_price,
        shares_outstanding=shares_outstanding,
        earnings_per_share=earnings_per_share,
    )


@mcp.tool()
def generate_financial_report_tool(
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

    Args:
        company_name: Full company name.
        ticker: Optional ticker symbol for reference.
        revenue: Total revenue for the period.
        net_income: Net income (profit) for the period.
        total_assets: Total assets from the balance sheet.
        total_liabilities: Total liabilities.
        shareholders_equity: Total shareholders' equity.
        current_assets: Current assets.
        current_liabilities: Current liabilities.
        ebitda: EBITDA for the period.
        free_cash_flow: Free cash flow (operating CF minus capex).
        revenue_growth_rate: YoY revenue growth as a decimal (e.g. 0.12 = 12%).
        industry: Industry or sector for context.
        fiscal_year: The fiscal year being analyzed.

    Returns:
        Structured report with key ratios, financial summary, strengths,
        highlights, concerns, and overall assessment (Strong/Positive/Neutral/Cautious/Weak).
    """
    return generate_financial_report(
        company_name=company_name,
        ticker=ticker,
        revenue=revenue,
        net_income=net_income,
        total_assets=total_assets,
        total_liabilities=total_liabilities,
        shareholders_equity=shareholders_equity,
        current_assets=current_assets,
        current_liabilities=current_liabilities,
        ebitda=ebitda,
        free_cash_flow=free_cash_flow,
        revenue_growth_rate=revenue_growth_rate,
        industry=industry,
        fiscal_year=fiscal_year,
    )


@mcp.tool()
def convert_currency_tool(
    amount: float,
    from_currency: str,
    to_currency: str,
    show_all_rates: bool = False,
) -> dict[str, Any]:
    """Convert an amount between currencies using static reference rates.

    Supported currencies: USD, EUR, GBP, JPY, CAD, AUD, CHF, CNY, INR, MXN,
    SGD, HKD, NZD, SEK, NOK, DKK, ZAR, BRL, KRW.

    Args:
        amount: Amount to convert (>= 0).
        from_currency: Source currency ISO 4217 code (e.g. "USD").
        to_currency: Target currency ISO 4217 code (e.g. "EUR").
        show_all_rates: If True, also convert to all other supported currencies.

    Returns:
        Converted amount, exchange rate, inverse rate, and optionally a full
        cross-rates table.

    Note:
        These are static reference rates for demonstration. Use a live FX feed
        for production applications.
    """
    return convert_currency(
        amount=amount,
        from_currency=from_currency,
        to_currency=to_currency,
        show_all_rates=show_all_rates,
    )


@mcp.tool()
def compound_interest_tool(
    principal: float,
    annual_rate: float,
    years: float,
    compounds_per_year: int = 12,
    additional_contribution: float = 0.0,
    contribution_timing: str = "end",
) -> dict[str, Any]:
    """Calculate compound interest and future value of an investment.

    Args:
        principal: Initial investment / present value (>= 0).
        annual_rate: Annual nominal interest rate as a decimal (e.g. 0.07 = 7%).
        years: Investment horizon in years (> 0).
        compounds_per_year: Compounding frequency: 1=annual, 4=quarterly,
            12=monthly (default), 52=weekly, 365=daily.
        additional_contribution: Periodic contribution per compounding period
            (e.g. monthly amount if compounds_per_year=12).
        contribution_timing: "end" (ordinary annuity) or "beginning" (annuity due).

    Returns:
        Future value, total contributions, total interest earned, effective
        annual rate (EAR), and year-by-year growth summary.
    """
    return compound_interest(
        principal=principal,
        annual_rate=annual_rate,
        years=years,
        compounds_per_year=compounds_per_year,
        additional_contribution=additional_contribution,
        contribution_timing=contribution_timing,
    )


@mcp.tool()
def loan_amortization_tool(
    principal: float,
    annual_rate: float,
    term_months: int,
    extra_monthly_payment: float = 0.0,
    origination_fee: float = 0.0,
) -> dict[str, Any]:
    """Calculate monthly payment and full amortization schedule for a loan.

    Args:
        principal: Loan amount (> 0).
        annual_rate: Annual nominal interest rate as a decimal (e.g. 0.065 = 6.5%).
        term_months: Loan term in months (e.g. 360 for a 30-year mortgage).
        extra_monthly_payment: Additional principal payment each month to
            reduce total interest and shorten the loan term.
        origination_fee: One-time upfront fee for APR estimation.

    Returns:
        Monthly payment, total interest paid, APR estimate, actual payoff
        timeline, and a full month-by-month amortization schedule.
    """
    return loan_amortization(
        principal=principal,
        annual_rate=annual_rate,
        term_months=term_months,
        extra_monthly_payment=extra_monthly_payment,
        origination_fee=origination_fee,
    )


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Run the MCP server (stdio transport)."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
