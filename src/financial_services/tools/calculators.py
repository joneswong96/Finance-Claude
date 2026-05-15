"""Financial calculators: compound_interest, loan_amortization, convert_currency."""

from __future__ import annotations

import math
from typing import Any


# ---------------------------------------------------------------------------
# Compound Interest / Future Value
# ---------------------------------------------------------------------------

def compound_interest(
    principal: float,
    annual_rate: float,
    years: float,
    compounds_per_year: int = 12,
    additional_contribution: float = 0.0,
    contribution_timing: str = "end",
) -> dict[str, Any]:
    """Calculate compound interest and future value.

    Parameters
    ----------
    principal:
        Initial investment / present value (must be >= 0).
    annual_rate:
        Annual nominal interest rate as a decimal (e.g. 0.07 for 7%).
    years:
        Investment horizon in years (must be > 0).
    compounds_per_year:
        Number of compounding periods per year.
        Common values: 1 (annual), 2 (semi-annual), 4 (quarterly),
        12 (monthly), 52 (weekly), 365 (daily).
    additional_contribution:
        Optional periodic contribution made every compounding period
        (e.g. monthly if compounds_per_year=12).
    contribution_timing:
        ``"end"`` for contributions at period end (ordinary annuity) or
        ``"beginning"`` for contributions at period start (annuity due).

    Returns
    -------
    dict
        Future value, total contributions, total interest earned, effective
        annual rate, and a year-by-year growth summary.
    """
    if principal < 0:
        return {"error": "principal must be >= 0."}
    if annual_rate < 0:
        return {"error": "annual_rate must be >= 0."}
    if years <= 0:
        return {"error": "years must be > 0."}
    if compounds_per_year <= 0:
        return {"error": "compounds_per_year must be a positive integer."}

    n = compounds_per_year
    r_per_period = annual_rate / n
    total_periods = int(years * n)

    # Effective Annual Rate (EAR)
    if annual_rate == 0:
        ear = 0.0
    else:
        ear = (1 + r_per_period) ** n - 1

    # Future value of lump-sum principal
    fv_principal = principal * (1 + r_per_period) ** total_periods

    # Future value of periodic contributions (annuity)
    fv_contributions = 0.0
    if additional_contribution != 0 and r_per_period != 0:
        fv_annuity = additional_contribution * (((1 + r_per_period) ** total_periods - 1) / r_per_period)
        if contribution_timing.lower().startswith("b"):
            fv_annuity *= (1 + r_per_period)
        fv_contributions = fv_annuity
    elif additional_contribution != 0:
        # Zero interest — simple accumulation
        fv_contributions = additional_contribution * total_periods

    future_value = fv_principal + fv_contributions
    total_contributions = principal + additional_contribution * total_periods
    total_interest = future_value - total_contributions

    # Year-by-year summary
    yearly_summary: list[dict[str, float]] = []
    for yr in range(1, int(math.ceil(years)) + 1):
        periods_at_yr = min(yr * n, total_periods)
        fv_p = principal * (1 + r_per_period) ** periods_at_yr
        if additional_contribution != 0 and r_per_period != 0:
            fv_c = additional_contribution * (((1 + r_per_period) ** periods_at_yr - 1) / r_per_period)
            if contribution_timing.lower().startswith("b"):
                fv_c *= (1 + r_per_period)
        elif additional_contribution != 0:
            fv_c = additional_contribution * periods_at_yr
        else:
            fv_c = 0.0
        fv_yr = fv_p + fv_c
        contribs_yr = principal + additional_contribution * periods_at_yr
        yearly_summary.append(
            {
                "year": yr,
                "balance": round(fv_yr, 2),
                "total_contributions": round(contribs_yr, 2),
                "interest_earned": round(fv_yr - contribs_yr, 2),
            }
        )

    return {
        "inputs": {
            "principal": principal,
            "annual_rate": f"{annual_rate * 100:.4f}%",
            "years": years,
            "compounds_per_year": compounds_per_year,
            "additional_contribution_per_period": additional_contribution,
            "contribution_timing": contribution_timing,
        },
        "results": {
            "future_value": round(future_value, 2),
            "total_contributions": round(total_contributions, 2),
            "total_interest_earned": round(total_interest, 2),
            "effective_annual_rate": f"{ear * 100:.4f}%",
            "return_on_investment": f"{(total_interest / total_contributions * 100):.2f}%" if total_contributions > 0 else "N/A",
        },
        "yearly_summary": yearly_summary,
        "note": (
            "Assumes constant rate and regular contributions. "
            "Actual returns will vary."
        ),
    }


# ---------------------------------------------------------------------------
# Loan Amortization
# ---------------------------------------------------------------------------

def loan_amortization(
    principal: float,
    annual_rate: float,
    term_months: int,
    extra_monthly_payment: float = 0.0,
    origination_fee: float = 0.0,
) -> dict[str, Any]:
    """Calculate monthly payment and full amortization schedule for a loan.

    Parameters
    ----------
    principal:
        Loan amount (must be > 0).
    annual_rate:
        Annual nominal interest rate as a decimal (e.g. 0.065 for 6.5%).
    term_months:
        Loan term in months (e.g. 360 for a 30-year mortgage).
    extra_monthly_payment:
        Optional additional principal payment made each month.  This reduces
        the total interest paid and shortens the loan term.
    origination_fee:
        One-time upfront fee (added to the cost calculation for APR estimation).

    Returns
    -------
    dict
        Monthly payment, total interest, APR estimate, and a full amortization
        schedule (one row per month).
    """
    if principal <= 0:
        return {"error": "principal must be > 0."}
    if annual_rate < 0:
        return {"error": "annual_rate must be >= 0."}
    if term_months <= 0:
        return {"error": "term_months must be a positive integer."}

    monthly_rate = annual_rate / 12

    # Standard monthly payment (PMT formula)
    if monthly_rate == 0:
        monthly_payment = principal / term_months
    else:
        monthly_payment = (
            principal
            * monthly_rate
            * (1 + monthly_rate) ** term_months
            / ((1 + monthly_rate) ** term_months - 1)
        )

    # Build amortization schedule
    schedule: list[dict[str, Any]] = []
    balance = principal
    total_interest_paid = 0.0
    total_principal_paid = 0.0
    actual_months = 0

    for month in range(1, term_months + 1):
        if balance <= 0:
            break
        interest_payment = balance * monthly_rate
        principal_payment = min(monthly_payment - interest_payment + extra_monthly_payment, balance)
        if principal_payment < 0:
            principal_payment = 0.0

        # Final payment may be slightly less
        actual_payment = interest_payment + principal_payment
        balance -= principal_payment

        if balance < 0.01:
            balance = 0.0

        total_interest_paid += interest_payment
        total_principal_paid += principal_payment
        actual_months += 1

        schedule.append(
            {
                "month": month,
                "payment": round(actual_payment, 2),
                "principal": round(principal_payment, 2),
                "interest": round(interest_payment, 2),
                "cumulative_principal": round(total_principal_paid, 2),
                "cumulative_interest": round(total_interest_paid, 2),
                "remaining_balance": round(max(balance, 0), 2),
            }
        )

        if balance == 0:
            break

    total_paid = total_principal_paid + total_interest_paid + origination_fee

    # APR approximation (Newton-Raphson for monthly rate that prices in fee)
    apr_monthly = monthly_rate
    if origination_fee > 0 and actual_months > 0:
        net_proceeds = principal - origination_fee
        # Iterative solver
        for _ in range(50):
            if apr_monthly == 0:
                break
            pmt = monthly_payment
            pv = pmt * (1 - (1 + apr_monthly) ** -actual_months) / apr_monthly
            dpv = pmt * (
                (actual_months * (1 + apr_monthly) ** (-actual_months - 1)) / apr_monthly
                - (1 - (1 + apr_monthly) ** -actual_months) / apr_monthly**2
            )
            delta = (pv - net_proceeds) / dpv
            apr_monthly -= delta
            if abs(delta) < 1e-10:
                break
    apr = apr_monthly * 12

    # Savings from extra payment
    time_saved_months = term_months - actual_months
    standard_total_interest = (monthly_payment * term_months) - principal if monthly_rate != 0 else 0
    interest_savings = max(0.0, standard_total_interest - total_interest_paid)

    result: dict[str, Any] = {
        "inputs": {
            "principal": principal,
            "annual_rate": f"{annual_rate * 100:.4f}%",
            "term_months": term_months,
            "term_years": round(term_months / 12, 1),
            "extra_monthly_payment": extra_monthly_payment,
            "origination_fee": origination_fee,
        },
        "results": {
            "monthly_payment": round(monthly_payment, 2),
            "total_monthly_payment_with_extra": round(monthly_payment + extra_monthly_payment, 2),
            "total_interest_paid": round(total_interest_paid, 2),
            "total_amount_paid": round(total_paid, 2),
            "effective_loan_cost": f"{total_interest_paid / principal * 100:.2f}% of principal",
            "apr_estimate": f"{apr * 100:.4f}%" if origination_fee > 0 else f"{annual_rate * 100:.4f}% (no fees)",
            "actual_payoff_months": actual_months,
            "actual_payoff_years": round(actual_months / 12, 1),
        },
        "amortization_schedule": schedule,
    }

    if extra_monthly_payment > 0:
        result["extra_payment_benefit"] = {
            "months_saved": time_saved_months,
            "interest_savings": round(interest_savings, 2),
        }

    return result


# ---------------------------------------------------------------------------
# Currency Conversion
# ---------------------------------------------------------------------------

# Static exchange rates relative to USD (updated for demo purposes — not live)
_USD_RATES: dict[str, float] = {
    "USD": 1.0000,
    "EUR": 0.9210,   # 1 USD = 0.921 EUR
    "GBP": 0.7890,   # 1 USD = 0.789 GBP
    "JPY": 149.50,   # 1 USD = 149.5 JPY
    "CAD": 1.3650,   # 1 USD = 1.365 CAD
    "AUD": 1.5430,   # 1 USD = 1.543 AUD
    "CHF": 0.8950,   # 1 USD = 0.895 CHF
    "CNY": 7.2400,   # 1 USD = 7.24 CNY
    "INR": 83.20,    # 1 USD = 83.2 INR
    "MXN": 17.15,    # 1 USD = 17.15 MXN
    "SGD": 1.3450,   # 1 USD = 1.345 SGD
    "HKD": 7.8200,   # 1 USD = 7.82 HKD
    "NZD": 1.6280,   # 1 USD = 1.628 NZD
    "SEK": 10.550,   # 1 USD = 10.55 SEK
    "NOK": 10.620,   # 1 USD = 10.62 NOK
    "DKK": 6.8800,   # 1 USD = 6.88 DKK
    "ZAR": 18.900,   # 1 USD = 18.9 ZAR
    "BRL": 4.9800,   # 1 USD = 4.98 BRL
    "KRW": 1325.0,   # 1 USD = 1325 KRW
}

_CURRENCY_NAMES: dict[str, str] = {
    "USD": "US Dollar",
    "EUR": "Euro",
    "GBP": "British Pound Sterling",
    "JPY": "Japanese Yen",
    "CAD": "Canadian Dollar",
    "AUD": "Australian Dollar",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Renminbi (Yuan)",
    "INR": "Indian Rupee",
    "MXN": "Mexican Peso",
    "SGD": "Singapore Dollar",
    "HKD": "Hong Kong Dollar",
    "NZD": "New Zealand Dollar",
    "SEK": "Swedish Krona",
    "NOK": "Norwegian Krone",
    "DKK": "Danish Krone",
    "ZAR": "South African Rand",
    "BRL": "Brazilian Real",
    "KRW": "South Korean Won",
}


def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
    show_all_rates: bool = False,
) -> dict[str, Any]:
    """Convert an amount between currencies using static reference rates.

    ⚠️ STATIC RATES — hardcoded as of late 2024. Do NOT use for trading,
    FX analysis, or any context where accuracy matters. For live rates use
    TradingView MCP (``quote_get``) or a real-time FX API via ``fetch``.

    Supported currencies: USD, EUR, GBP, JPY, CAD, AUD, CHF, CNY, INR, MXN,
    SGD, HKD, NZD, SEK, NOK, DKK, ZAR, BRL, KRW.

    Parameters
    ----------
    amount:
        Amount to convert (must be >= 0).
    from_currency:
        Source currency code (ISO 4217, e.g. "USD").
    to_currency:
        Target currency code (ISO 4217, e.g. "EUR").
    show_all_rates:
        If True, also returns conversion of ``amount`` from ``from_currency``
        into all other supported currencies.

    Returns
    -------
    dict
        Converted amount, exchange rate used, and optional cross-rates table.
    """
    if amount < 0:
        return {"error": "amount must be >= 0."}

    src = from_currency.strip().upper()
    dst = to_currency.strip().upper()

    if src not in _USD_RATES:
        return {
            "error": f"Unsupported currency: {src}.",
            "supported_currencies": sorted(_USD_RATES.keys()),
        }
    if dst not in _USD_RATES:
        return {
            "error": f"Unsupported currency: {dst}.",
            "supported_currencies": sorted(_USD_RATES.keys()),
        }

    # Convert via USD as the base
    amount_in_usd = amount / _USD_RATES[src]
    converted = amount_in_usd * _USD_RATES[dst]
    exchange_rate = _USD_RATES[dst] / _USD_RATES[src]  # direct quote: 1 src = X dst

    result: dict[str, Any] = {
        "from": {
            "currency": src,
            "currency_name": _CURRENCY_NAMES.get(src, src),
            "amount": amount,
        },
        "to": {
            "currency": dst,
            "currency_name": _CURRENCY_NAMES.get(dst, dst),
            "amount": round(converted, 4),
        },
        "exchange_rate": {
            "rate": round(exchange_rate, 6),
            "description": f"1 {src} = {exchange_rate:.6f} {dst}",
            "inverse": round(1 / exchange_rate, 6),
            "inverse_description": f"1 {dst} = {1/exchange_rate:.6f} {src}",
        },
        "disclaimer": (
            "These are static reference rates for demonstration purposes only. "
            "They do not reflect live market rates. Use a real-time FX feed for "
            "production applications."
        ),
    }

    if show_all_rates:
        all_rates: list[dict[str, Any]] = []
        for ccy, usd_rate in sorted(_USD_RATES.items()):
            if ccy == src:
                continue
            r = usd_rate / _USD_RATES[src]
            converted_amt = amount_in_usd * usd_rate
            all_rates.append(
                {
                    "currency": ccy,
                    "currency_name": _CURRENCY_NAMES.get(ccy, ccy),
                    "rate": round(r, 6),
                    "converted_amount": round(converted_amt, 4),
                }
            )
        result["all_conversions"] = all_rates

    return result
