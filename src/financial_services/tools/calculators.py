"""Financial calculators: compound_interest, loan_amortization, convert_currency."""

from __future__ import annotations

import math
from typing import Any

# Static exchange rates vs USD (as of training data — for demo purposes only)
_USD_RATES: dict[str, float] = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 149.50,
    "CAD": 1.36,
    "AUD": 1.53,
    "CHF": 0.90,
    "CNY": 7.24,
    "INR": 83.10,
    "MXN": 17.15,
    "BRL": 4.97,
    "SGD": 1.34,
    "HKD": 7.82,
    "SEK": 10.42,
    "NOK": 10.55,
}


def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
) -> dict[str, Any]:
    """Convert an amount between currencies using static reference rates.

    Parameters
    ----------
    amount:
        The monetary amount to convert.
    from_currency:
        ISO 4217 currency code of the source currency (e.g. "USD").
    to_currency:
        ISO 4217 currency code of the target currency (e.g. "EUR").
    """
    src = from_currency.strip().upper()
    dst = to_currency.strip().upper()

    if src not in _USD_RATES:
        return {"error": f"Unsupported currency: {src}. Supported: {sorted(_USD_RATES)}"}
    if dst not in _USD_RATES:
        return {"error": f"Unsupported currency: {dst}. Supported: {sorted(_USD_RATES)}"}

    # Convert to USD then to target
    amount_usd = amount / _USD_RATES[src]
    converted = amount_usd * _USD_RATES[dst]
    rate = _USD_RATES[dst] / _USD_RATES[src]

    return {
        "from": {"amount": round(amount, 4), "currency": src},
        "to": {"amount": round(converted, 4), "currency": dst},
        "exchange_rate": round(rate, 6),
        "inverse_rate": round(1 / rate, 6),
        "disclaimer": "Rates are static reference values for demonstration only. Use a live FX feed for production.",
    }


def compound_interest(
    principal: float,
    annual_rate: float,
    years: float,
    compounds_per_year: int = 12,
    additional_contribution: float = 0.0,
) -> dict[str, Any]:
    """Calculate future value with compound interest.

    Parameters
    ----------
    principal:
        Initial investment / deposit amount.
    annual_rate:
        Annual interest rate as a decimal (e.g. 0.07 for 7%).
    years:
        Investment horizon in years.
    compounds_per_year:
        Number of compounding periods per year (12 = monthly, 4 = quarterly, 1 = annually, 365 = daily).
    additional_contribution:
        Regular contribution added each compounding period (e.g. monthly contribution if compounds_per_year=12).
    """
    if principal < 0:
        return {"error": "principal cannot be negative."}
    if annual_rate < 0:
        return {"error": "annual_rate cannot be negative."}
    if years <= 0:
        return {"error": "years must be positive."}
    if compounds_per_year <= 0:
        return {"error": "compounds_per_year must be a positive integer."}

    n = compounds_per_year
    r = annual_rate / n
    total_periods = int(years * n)

    # Future value of lump sum
    fv_lump = principal * (1 + r) ** total_periods

    # Future value of recurring contributions (annuity due / ordinary annuity)
    if additional_contribution > 0 and r > 0:
        fv_contributions = additional_contribution * (((1 + r) ** total_periods - 1) / r)
    elif additional_contribution > 0:
        fv_contributions = additional_contribution * total_periods
    else:
        fv_contributions = 0.0

    future_value = fv_lump + fv_contributions
    total_contributed = principal + additional_contribution * total_periods
    total_interest_earned = future_value - total_contributed

    # Effective annual rate
    ear = (1 + r) ** n - 1

    return {
        "inputs": {
            "principal": principal,
            "annual_rate_pct": f"{annual_rate * 100:.3f}%",
            "years": years,
            "compounds_per_year": n,
            "additional_contribution_per_period": additional_contribution,
        },
        "future_value": round(future_value, 2),
        "total_contributed": round(total_contributed, 2),
        "total_interest_earned": round(total_interest_earned, 2),
        "effective_annual_rate": f"{ear * 100:.4f}%",
        "total_return_pct": f"{(future_value / total_contributed - 1) * 100:.2f}%" if total_contributed > 0 else "N/A",
    }


def loan_amortization(
    principal: float,
    annual_rate: float,
    term_months: int,
    extra_monthly_payment: float = 0.0,
) -> dict[str, Any]:
    """Calculate monthly payment and amortization schedule for a loan.

    Parameters
    ----------
    principal:
        Loan amount (original balance).
    annual_rate:
        Annual interest rate as a decimal (e.g. 0.065 for 6.5%).
    term_months:
        Loan term in months (e.g. 360 for a 30-year mortgage).
    extra_monthly_payment:
        Optional additional amount paid each month toward principal.
    """
    if principal <= 0:
        return {"error": "principal must be positive."}
    if annual_rate < 0:
        return {"error": "annual_rate cannot be negative."}
    if term_months <= 0:
        return {"error": "term_months must be positive."}

    monthly_rate = annual_rate / 12

    # Standard monthly payment (fixed-rate amortization formula)
    if monthly_rate > 0:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** term_months) / (
            (1 + monthly_rate) ** term_months - 1
        )
    else:
        monthly_payment = principal / term_months

    total_monthly = monthly_payment + extra_monthly_payment

    # Build amortization schedule
    schedule: list[dict[str, float]] = []
    balance = principal
    total_interest_paid = 0.0
    actual_months = 0

    for month in range(1, term_months + 1):
        if balance <= 0:
            break

        interest = balance * monthly_rate
        principal_payment = min(total_monthly - interest, balance)
        if principal_payment < 0:
            principal_payment = 0.0

        balance -= principal_payment
        balance = max(balance, 0.0)
        total_interest_paid += interest
        actual_months = month

        schedule.append({
            "month": month,
            "payment": round(total_monthly if balance > 0 else (interest + principal_payment), 2),
            "principal": round(principal_payment, 2),
            "interest": round(interest, 2),
            "balance": round(balance, 2),
        })

        if balance == 0:
            break

    total_paid = sum(p["payment"] for p in schedule)
    months_saved = term_months - actual_months

    return {
        "inputs": {
            "loan_amount": principal,
            "annual_rate_pct": f"{annual_rate * 100:.3f}%",
            "term_months": term_months,
            "extra_monthly_payment": extra_monthly_payment,
        },
        "monthly_payment": round(monthly_payment, 2),
        "total_monthly_with_extra": round(total_monthly, 2),
        "total_paid": round(total_paid, 2),
        "total_interest_paid": round(total_interest_paid, 2),
        "actual_payoff_months": actual_months,
        "months_saved_by_extra_payment": months_saved,
        "amortization_schedule": schedule,
    }
