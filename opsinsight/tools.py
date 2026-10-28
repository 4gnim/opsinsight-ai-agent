from opsinsight.database import get_connection


def get_sales_summary() -> dict:
    """Return an overall summary of sales transactions."""
    connection = get_connection()

    try:
        result = connection.execute(
            """
            SELECT
                COUNT(*) AS transaction_count,
                COALESCE(SUM(quantity), 0) AS units_sold,
                COALESCE(
                    SUM(quantity * unit_price),
                    0
                ) AS total_revenue,
                MIN(sale_date) AS first_sale_date,
                MAX(sale_date) AS last_sale_date
            FROM sales
            """
        ).fetchone()

        return dict(result)

    finally:
        connection.close()


def get_top_products(limit: int = 5) -> list[dict]:
    """Return the best-selling products by units sold."""
    if not 1 <= limit <= 10:
        raise ValueError("Limit must be between 1 and 10.")

    connection = get_connection()

    try:
        results = connection.execute(
            """
            SELECT
                p.product_id,
                p.product_name,
                SUM(s.quantity) AS units_sold,
                SUM(s.quantity * s.unit_price) AS revenue
            FROM products AS p
            JOIN sales AS s
                ON p.product_id = s.product_id
            GROUP BY
                p.product_id,
                p.product_name
            ORDER BY
                units_sold DESC,
                revenue DESC,
                p.product_name ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        return [dict(row) for row in results]

    finally:
        connection.close()


def get_low_stock_products() -> list[dict]:
    """Return products whose stock is at or below minimum."""
    connection = get_connection()

    try:
        results = connection.execute(
            """
            SELECT
                product_id,
                product_name,
                stock_qty,
                min_stock,
                min_stock - stock_qty AS stock_gap
            FROM products
            WHERE stock_qty <= min_stock
            ORDER BY
                stock_gap DESC,
                product_name ASC
            """
        ).fetchall()

        return [dict(row) for row in results]

    finally:
        connection.close()