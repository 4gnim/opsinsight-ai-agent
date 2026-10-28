from pathlib import Path
import sqlite3


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "opsinsight.db"


def get_connection() -> sqlite3.Connection:
    """Create a connection to the local SQLite database."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database() -> None:
    """Create the tables and indexes required by the application."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = get_connection()

    try:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                sku TEXT NOT NULL UNIQUE,
                product_name TEXT NOT NULL,
                category TEXT NOT NULL,
                unit_price INTEGER NOT NULL
                    CHECK (unit_price >= 0),
                stock_qty INTEGER NOT NULL
                    CHECK (stock_qty >= 0),
                min_stock INTEGER NOT NULL
                    CHECK (min_stock >= 0)
            );

            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY,
                sale_date TEXT NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL
                    CHECK (quantity > 0),
                unit_price INTEGER NOT NULL
                    CHECK (unit_price >= 0),
                channel TEXT NOT NULL
                    CHECK (
                        channel IN (
                            'Online',
                            'Retail',
                            'Marketplace'
                        )
                    ),
                FOREIGN KEY (product_id)
                    REFERENCES products(product_id)
            );

            CREATE INDEX IF NOT EXISTS idx_sales_date
                ON sales(sale_date);

            CREATE INDEX IF NOT EXISTS idx_sales_product_id
                ON sales(product_id);
            """
        )

        connection.commit()

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()

    connection = get_connection()

    try:
        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
            """
        ).fetchall()
    finally:
        connection.close()

    print(f"Database initialized: {DB_PATH}")
    print("Tables:", ", ".join(row["name"] for row in tables))