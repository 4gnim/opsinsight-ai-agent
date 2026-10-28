import json

from langchain_core.tools import tool

from opsinsight.tools import (get_low_stock_products, get_sales_summary, get_top_products)


@tool
def sales_summary() -> str:
    """Get the overall sales summary, including transaction count,
    total units sold, revenue, and sales date range.

    Use this when the user asks about sales performance or revenue.
    This tool does not provide targets, profit, historical comparisons,
    or evidence that sales performance is good or bad.
    """
    result = get_sales_summary()

    result["evaluation_limits"] = {
        "sales_target_available": False,
        "historical_comparison_available": False,
        "profit_data_available": False,
        "note": (
            "Revenue and units sold describe sales activity. "
            "They are insufficient on their own to classify "
            "performance as good or bad."
        ),
    }

    return json.dumps(result, ensure_ascii=False)


@tool
def top_selling_products(limit: int = 5) -> str:
    """Find products with the highest number of units sold.
    Use this when the user asks about best-selling or top-selling products.
    The limit must be between 1 and 10.
    """
    result = get_top_products(limit=limit)
    return json.dumps(result, ensure_ascii=False)


@tool
def low_stock_products() -> str:
    """Find products whose current stock is at or below their minimum stock threshold. Use this when the user asks about low stock, inventory risks, or which products may need replenishment.
    """
    result = get_low_stock_products()
    return json.dumps(result, ensure_ascii=False)


AVAILABLE_TOOLS = [
    sales_summary,
    top_selling_products,
    low_stock_products,
]