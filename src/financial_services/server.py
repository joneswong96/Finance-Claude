"""MCP server entry point for the financial-services plugin."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from financial_services.tools.calculators import compound_interest, convert_currency, loan_amortization
from financial_services.tools.portfolio import assess_portfolio
from financial_services.tools.stock import analyze_stock, generate_financial_report
from financial_services.tools.valuation import calculate_dcf, calculate_financial_ratios

mcp = FastMCP("financial-analysis")


@mcp.tool()
def tool_analyze_stock(ticker: str) -> dict[str, Any]:
    """Fetch real-time stock data and return a structured analysis including price, valuation metrics, financials, and analyst commentary.

    Args:
        ticker: Stock ticker symbol (e.g. "AAPL", "MSFT", "GOOGL").
    """
    return analyze_stock(ticker)


@mcp.tool()
def tool_calculate_dcf(
    cash_flows: list[float],
    discount_rate: float,
    terminal_growth_rate: float = 0.02,
    shares_outstanding: float | None = None,
) -> dict[str, Any]:
    """Perform a Discounted Cash Flow (DCF) valuation given projected cash flows.

    Args:
        cash_flows: List of projected free cash flows for each future period.
        discount_rate: WACC as a decimal (e.g. 0.10 for 10%).
        terminal_growth_rate: Perpetuity growth rate for terminal value (e.g. 0.02 for 2%).
        shares_outstanding: Optional shares count to compute per-share intrinsic value.
    """
    return calculate_dcf(cash_flows, discount_rate, terminal_growth_rate, shares_outstanding)


@mcp.tool()
def tool_assess_portfolio(
    holdings: list[dict[str, Any]],
    fetch_live_prices: bool = True,
) -> dict[str, Any]:
    """Assess a stock portfolio: compute market value, allocation %, unrealized P&L, and risk level.

    Args:
        holdings: List of dicts with keys: ticker (str), shares (float), avg_cost (float).
                  Optionally include current_price (float) to skip live price fetch.
        fetch_live_prices: Set False to use only provided current_price values.
    """
    return assess_portfolio(holdings, fetch_live_prices=fetch_live_prices)


@mcp.tool()
def tool_calculate_financial_ratios(
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
    """Compute liquidity, leverage, profitability, and efficiency ratios from financial statement inputs.

    Provide whichever inputs you have — only ratios that can be computed from the given data are returned.
    All monetary inputs must use the same currency and period.
    """
    return calculate_financial_ratios(
        current_assets=current_assets,
        current_liabilities=current_liabilities,
        total_assets=total_assets,
        total_liabilities=total_liabilities,
        shareholders_equity=shareholders_equity,
        net_income=net_income,
        revenue=revenue,
        gross_profit=gross_profit,
        ebitda=ebitda,
        interest_expense=interest_expense,
        inventory=inventory,
        accounts_receivable=accounts_receivable,
        cost_of_goods_sold=cost_of_goods_sold,
        operating_income=operating_income,
    )


@mcp.tool()
def tool_generate_financial_report(
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
    """Generate a structured financial analysis report including ratios, narrative, and an overall assessment.

    All monetary inputs should use the same currency unit (typically USD millions).
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
def tool_convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
) -> dict[str, Any]:
    """Convert an amount between currencies using reference exchange rates.

    Supported currencies: USD, EUR, GBP, JPY, CAD, AUD, CHF, CNY, INR, MXN, BRL, SGD, HKD, SEK, NOK.
    Note: rates are static reference values — use a live FX feed for production.

    Args:
        amount: Monetary amount to convert.
        from_currency: ISO 4217 source currency code (e.g. "USD").
        to_currency: ISO 4217 target currency code (e.g. "EUR").
    """
    return convert_currency(amount, from_currency, to_currency)


@mcp.tool()
def tool_compound_interest(
    principal: float,
    annual_rate: float,
    years: float,
    compounds_per_year: int = 12,
    additional_contribution: float = 0.0,
) -> dict[str, Any]:
    """Calculate future value of an investment with compound interest and optional recurring contributions.

    Args:
        principal: Initial investment amount.
        annual_rate: Annual interest rate as a decimal (e.g. 0.07 for 7%).
        years: Investment horizon in years.
        compounds_per_year: Compounding frequency per year (12=monthly, 4=quarterly, 1=annually, 365=daily).
        additional_contribution: Amount added each compounding period (e.g. monthly if compounds_per_year=12).
    """
    return compound_interest(principal, annual_rate, years, compounds_per_year, additional_contribution)


@mcp.tool()
def tool_loan_amortization(
    principal: float,
    annual_rate: float,
    term_months: int,
    extra_monthly_payment: float = 0.0,
) -> dict[str, Any]:
    """Calculate monthly loan payment and full amortization schedule.

    Args:
        principal: Loan amount.
        annual_rate: Annual interest rate as a decimal (e.g. 0.065 for 6.5%).
        term_months: Loan term in months (e.g. 360 for a 30-year mortgage).
        extra_monthly_payment: Additional monthly payment toward principal to pay off loan faster.
    """
    return loan_amortization(principal, annual_rate, term_months, extra_monthly_payment)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
