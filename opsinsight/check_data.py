from opsinsight.database import get_connection


def main() -> None:
    connection = get_connection()

    try:
        products = connection.execute(
            """
            SELECT product_id, product_name, stock_qty, min_stock
            FROM products
            ORDER BY product_id
            """
        ).fetchall()

        print("=== PRODUCT INVENTORY ===")

        for product in products:
            print(
                f"{product['product_name']}: "
                f"stock={product['stock_qty']}, "
                f"minimum={product['min_stock']}"
            )

        result = connection.execute(
            """
            SELECT
                COUNT(*) AS transaction_count,
                SUM(quantity) AS units_sold,
                SUM(quantity * unit_price) AS total_revenue
            FROM sales
            """
        ).fetchone()

        print("\n=== SALES SUMMARY ===")
        print(f"Transactions: {result['transaction_count']}")
        print(f"Units sold: {result['units_sold']}")
        print(f"Total revenue: Rp{result['total_revenue']:,}")

    finally:
        connection.close()


if __name__ == "__main__":
    main()