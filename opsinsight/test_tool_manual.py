from opsinsight.tools import (
    get_low_stock_products,
    get_sales_summary,
    get_top_products,
)


def main() -> None:
    summary = get_sales_summary()

    print("=== SALES SUMMARY ===")
    print(f"Transactions: {summary['transaction_count']}")
    print(f"Units sold: {summary['units_sold']}")
    print(f"Revenue: Rp{summary['total_revenue']:,}")
    print(
        f"Period: {summary['first_sale_date']} "
        f"to {summary['last_sale_date']}"
    )

    print("\n=== TOP 5 PRODUCTS ===")

    for product in get_top_products(limit=5):
        print(
            f"{product['product_name']}: "
            f"{product['units_sold']} units, "
            f"revenue Rp{product['revenue']:,}"
        )

    print("\n=== LOW STOCK PRODUCTS ===")

    for product in get_low_stock_products():
        print(
            f"{product['product_name']}: "
            f"stock {product['stock_qty']}, "
            f"minimum {product['min_stock']}, "
            f"gap {product['stock_gap']}"
        )


if __name__ == "__main__":
    main()