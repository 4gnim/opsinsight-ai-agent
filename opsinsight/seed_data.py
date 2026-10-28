from opsinsight.database import (
    get_connection,
    initialize_database,
)


PRODUCTS = [
    (1, "SKU001", "Wireless Mouse", "Aksesoris", 85000, 12, 10),
    (2, "SKU002", "Mechanical Keyboard", "Aksesoris", 350000, 4, 8),
    (3, "SKU003", "USB-C Hub", "Aksesoris", 220000, 3, 6),
    (4, "SKU004", "Headset", "Audio", 275000, 18, 5),
    (5, "SKU005", "Webcam HD", "Video", 300000, 2, 5),
    (6, "SKU006", "Laptop Stand", "Aksesoris", 180000, 16, 6),
    (7, "SKU007", "SSD 1TB", "Storage", 950000, 7, 4),
    (8, "SKU008", "Monitor 24 Inch", "Display", 1650000, 2, 3),
    (9, "SKU009", "Laptop Bag", "Aksesoris", 250000, 9, 5),
    (10, "SKU010", "HDMI Cable", "Kabel", 65000, 25, 10),
]


SALES = [
    (1, "2026-10-01", 1, 4, 85000, "Online"),
    (2, "2026-10-01", 2, 2, 350000, "Retail"),
    (3, "2026-10-02", 3, 3, 220000, "Marketplace"),
    (4, "2026-10-02", 4, 2, 275000, "Online"),
    (5, "2026-10-03", 5, 1, 300000, "Retail"),
    (6, "2026-10-03", 6, 4, 180000, "Marketplace"),
    (7, "2026-10-04", 7, 1, 930000, "Online"),
    (8, "2026-10-04", 8, 1, 1650000, "Retail"),
    (9, "2026-10-05", 1, 5, 85000, "Marketplace"),
    (10, "2026-10-05", 9, 2, 250000, "Online"),
    (11, "2026-10-06", 10, 8, 65000, "Retail"),
    (12, "2026-10-07", 2, 3, 345000, "Marketplace"),
    (13, "2026-10-07", 3, 2, 220000, "Online"),
    (14, "2026-10-08", 4, 5, 275000, "Retail"),
    (15, "2026-10-09", 5, 2, 295000, "Marketplace"),
    (16, "2026-10-10", 6, 3, 180000, "Online"),
    (17, "2026-10-11", 7, 2, 950000, "Retail"),
    (18, "2026-10-12", 8, 1, 1600000, "Online"),
    (19, "2026-10-13", 9, 4, 250000, "Marketplace"),
    (20, "2026-10-14", 10, 12, 65000, "Online"),
    (21, "2026-10-15", 1, 6, 85000, "Retail"),
    (22, "2026-10-16", 2, 1, 350000, "Online"),
    (23, "2026-10-17", 3, 4, 215000, "Marketplace"),
    (24, "2026-10-18", 4, 3, 275000, "Online"),
    (25, "2026-10-19", 5, 1, 300000, "Retail"),
    (26, "2026-10-20", 6, 5, 180000, "Marketplace"),
    (27, "2026-10-20", 7, 1, 950000, "Online"),
    (28, "2026-10-21", 8, 1, 1650000, "Retail"),
    (29, "2026-10-22", 9, 3, 250000, "Online"),
    (30, "2026-10-23", 10, 10, 65000, "Marketplace"),
]


def seed_database() -> None:
    """Insert the synthetic products and sales into SQLite."""
    initialize_database()
    connection = get_connection()

    try:
        with connection:
            connection.executemany(
                """
                INSERT OR IGNORE INTO products (
                    product_id,
                    sku,
                    product_name,
                    category,
                    unit_price,
                    stock_qty,
                    min_stock
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                PRODUCTS,
            )

            connection.executemany(
                """
                INSERT OR IGNORE INTO sales (
                    sale_id,
                    sale_date,
                    product_id,
                    quantity,
                    unit_price,
                    channel
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                SALES,
            )

        product_count = connection.execute(
            "SELECT COUNT(*) AS total FROM products"
        ).fetchone()["total"]

        sales_count = connection.execute(
            "SELECT COUNT(*) AS total FROM sales"
        ).fetchone()["total"]

    finally:
        connection.close()

    print("Synthetic dataset loaded successfully.")
    print(f"Products: {product_count}")
    print(f"Sales transactions: {sales_count}")


if __name__ == "__main__":
    seed_database()