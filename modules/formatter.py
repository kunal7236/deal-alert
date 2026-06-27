"""
modules/formatter.py

Telegram message formatter.

Responsibilities:
- Format deal notifications.
- No Telegram API calls.
- No business logic.
"""

from __future__ import annotations


def _format_price(price: int | float | None) -> str:
    """
    Format price with Indian currency symbol.
    """

    if price is None:
        return "N/A"

    return f"₹{price:,}"


def format_deal_message(
    deal: dict,
    matched_keyword: str,
) -> str:
    """
    Build Telegram notification message.
    """

    title = deal.get("title", "Unknown Product")
    image = deal.get("image", "")
    product_url = deal.get("productUrl", "#")

    current_price = _format_price(deal.get("currentPrice"))
    mrp = _format_price(deal.get("mrp"))

    discount = deal.get("discountPercentage")

    if discount is None:
        discount = "N/A"
    else:
        discount = f"{discount}%"

    return (
        f"🔥 <b>Keyword Match:</b> {matched_keyword}\n\n"
        f"<b>{title}</b>\n\n"
        f"💰 <b>Current Price:</b> {current_price}\n"
        f"🏷 <b>MRP:</b> {mrp}\n"
        f"📉 <b>Discount:</b> {discount}\n\n"
        f"🔗 <a href=\"{product_url}\">Buy Now</a>\n"
        f"<a href=\"{image}\">&#8203;</a>"
    )