"""Portfolio analysis tool: assess_portfolio."""

from __future__ import annotations

from typing import Any


def assess_portfolio(
    holdings: list[dict[str, Any]],
    risk_free_rate: float = 0.05,
    fetch_live_prices: bool = True,
) -> dict[str, Any]:
    """Assess a portfolio of stock holdings.

    Parameters
    ----------
    holdings:
        List of holding dicts, each with keys:
          - ``ticker``  (str)  : stock ticker symbol
          - ``shares``  (float): number of shares held
          - ``avg_cost`` (float): average cost basis per share
        Optionally, a holding may include:
          - ``current_price`` (float): override live price lookup
    risk_free_rate:
        Annual risk-free rate as a decimal, used for Sharpe-style commentary.
        Defaults to 5% (approximate current T-bill rate).
    fetch_live_prices:
        Whether to attempt fetching live prices via yfinance.
        Set to False to use only the ``current_price`` overrides in holdings.

    Returns
    -------
    dict
        Portfolio value, per-holding breakdown (allocation %, unrealised P&L),
        overall cost basis, and a qualitative risk assessment.
    """

    if not holdings:
        return {"error": "holdings list must not be empty."}

    # Normalise input keys (allow both camelCase and snake_case)
    normalised: list[dict[str, Any]] = []
    for h in holdings:
        ticker = str(h.get("ticker", h.get("symbol", ""))).strip().upper()
        shares = float(h.get("shares", h.get("quantity", 0)))
        avg_cost = float(h.get("avg_cost", h.get("average_cost", h.get("cost_basis", 0))))
        current_price_override = h.get("current_price", h.get("price"))
        if not ticker:
            return {"error": f"A holding entry is missing a ticker symbol: {h}"}
        if shares <= 0:
            return {"error": f"Shares must be positive for ticker {ticker}."}
        normalised.append(
            {
                "ticker": ticker,
                "shares": shares,
                "avg_cost": avg_cost,
                "current_price_override": current_price_override,
            }
        )

    # Fetch live prices via yfinance where not overridden
    tickers_needing_price = [
        h["ticker"] for h in normalised if h["current_price_override"] is None and fetch_live_prices
    ]

    live_prices: dict[str, float] = {}
    price_errors: dict[str, str] = {}

    if tickers_needing_price:
        try:
            import yfinance as yf

            for ticker in tickers_needing_price:
                try:
                    t = yf.Ticker(ticker)
                    info = t.info
                    price = (
                        info.get("currentPrice")
                        or info.get("regularMarketPrice")
                        or info.get("previousClose")
                    )
                    if price:
                        live_prices[ticker] = float(price)
                    else:
                        price_errors[ticker] = "Price not available from yfinance"
                except Exception as exc:
                    price_errors[ticker] = str(exc)
        except ImportError:
            for ticker in tickers_needing_price:
                price_errors[ticker] = "yfinance not installed — provide current_price in holdings"

    # Build per-holding metrics
    holding_details: list[dict[str, Any]] = []
    total_market_value = 0.0
    total_cost_basis = 0.0

    for h in normalised:
        ticker = h["ticker"]
        shares = h["shares"]
        avg_cost = h["avg_cost"]

        current_price: float | None = h["current_price_override"]
        if current_price is None:
            current_price = live_prices.get(ticker)

        cost_basis = shares * avg_cost
        total_cost_basis += cost_basis

        if current_price is not None:
            market_value = shares * current_price
            unrealised_pnl = market_value - cost_basis
            unrealised_pnl_pct = (unrealised_pnl / cost_basis * 100) if cost_basis != 0 else 0.0
            total_market_value += market_value
        else:
            market_value = cost_basis  # fall back to cost for weight calculation
            unrealised_pnl = None
            unrealised_pnl_pct = None
            total_market_value += market_value

        holding_details.append(
            {
                "ticker": ticker,
                "shares": shares,
                "avg_cost_per_share": avg_cost,
                "current_price": current_price,
                "market_value": round(market_value, 2) if market_value is not None else None,
                "cost_basis": round(cost_basis, 2),
                "unrealised_pnl": round(unrealised_pnl, 2) if unrealised_pnl is not None else None,
                "unrealised_pnl_pct": (
                    f"{unrealised_pnl_pct:+.2f}%" if unrealised_pnl_pct is not None else None
                ),
                "price_error": price_errors.get(ticker),
            }
        )

    # Compute allocation weights now that we have total_market_value
    for detail in holding_details:
        mv = detail["market_value"] or 0.0
        detail["allocation_pct"] = (
            f"{mv / total_market_value * 100:.2f}%" if total_market_value > 0 else "N/A"
        )

    # ---- Portfolio-level metrics ----
    total_unrealised_pnl = sum(
        d["unrealised_pnl"] for d in holding_details if d["unrealised_pnl"] is not None
    )
    total_unrealised_pnl_pct = (
        (total_unrealised_pnl / total_cost_basis * 100) if total_cost_basis != 0 else 0.0
    )

    # Concentration risk: top holding weight
    weights = [
        (d["market_value"] or 0.0) / total_market_value
        for d in holding_details
        if total_market_value > 0
    ]
    weights.sort(reverse=True)
    top_holding_weight = weights[0] if weights else 0.0
    num_holdings = len(holding_details)

    # Herfindahl-Hirschman Index (HHI) for concentration
    hhi = sum(w**2 for w in weights)

    # Risk level assessment
    if num_holdings == 1 or top_holding_weight > 0.60:
        risk_level = "HIGH"
        risk_reason = "Portfolio is highly concentrated — a single position dominates."
    elif num_holdings <= 3 or top_holding_weight > 0.40 or hhi > 0.35:
        risk_level = "ELEVATED"
        risk_reason = "Limited diversification increases idiosyncratic risk."
    elif num_holdings <= 8 or hhi > 0.20:
        risk_level = "MODERATE"
        risk_reason = "Moderate diversification; adding more uncorrelated assets would reduce risk."
    else:
        risk_level = "LOW-MODERATE"
        risk_reason = "Reasonably diversified portfolio."

    # Sort holdings by market value descending for readability
    holding_details.sort(key=lambda d: d["market_value"] or 0.0, reverse=True)

    result: dict[str, Any] = {
        "summary": {
            "total_market_value": round(total_market_value, 2),
            "total_cost_basis": round(total_cost_basis, 2),
            "total_unrealised_pnl": round(total_unrealised_pnl, 2),
            "total_unrealised_pnl_pct": f"{total_unrealised_pnl_pct:+.2f}%",
            "number_of_holdings": num_holdings,
            "risk_level": risk_level,
            "risk_assessment": risk_reason,
            "concentration_hhi": round(hhi, 4),
            "top_holding_weight": f"{top_holding_weight * 100:.1f}%",
        },
        "holdings": holding_details,
    }

    if price_errors:
        result["price_fetch_errors"] = price_errors
        result["note"] = (
            "Some live prices could not be fetched. Those positions use cost basis for market value. "
            "Provide 'current_price' in the holding dict to override."
        )

    # ---- Diversification tips ----
    tips: list[str] = []
    if num_holdings < 10:
        tips.append(
            f"Consider expanding from {num_holdings} to at least 15-20 positions to reduce concentration risk."
        )
    if top_holding_weight > 0.25:
        top_ticker = holding_details[0]["ticker"] if holding_details else "top position"
        tips.append(
            f"{top_ticker} represents {top_holding_weight*100:.1f}% of the portfolio. "
            "Trimming large individual positions can improve risk-adjusted returns."
        )
    if tips:
        result["diversification_tips"] = tips

    return result
