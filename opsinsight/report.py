
from opsinsight.tools import (
    get_low_stock_products,
    get_sales_summary,
    get_top_products,
)


def build_sales_report() -> dict:
    """Build a factual sales report directly from the database tools."""
    summary = get_sales_summary()
    top_products = get_top_products(limit=3)
    low_stock = get_low_stock_products()

    return {
        "metadata": {
            "source": "SQLite database",
            "report_type": "sales_and_inventory",
            "currency": "IDR",
        },
        "summary": summary,
        "top_products": top_products,
        "low_stock_products": low_stock,
        "evaluation_limits": {
            "sales_target_available": False,
            "historical_comparison_available": False,
            "profit_data_available": False,
            "note": (
                "Revenue and units sold describe sales activity. "
                "They are insufficient on their own to classify "
                "performance as good or bad."
            ),
        },
    }
