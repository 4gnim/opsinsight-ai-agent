from opsinsight.tools import (
    get_low_stock_products,
    get_sales_summary,
    get_top_products,
)


def test_sales_summary():
    result = get_sales_summary()

    assert result["transaction_count"] == 30
    assert result["units_sold"] == 102
    assert result["total_revenue"] == 24_300_000


def test_top_products():
    result = get_top_products(limit=3)

    assert len(result) == 3
    assert result[0]["product_name"] == "HDMI Cable"
    assert result[0]["units_sold"] == 30
    assert result[1]["product_name"] == "Wireless Mouse"
    assert result[1]["units_sold"] == 15
    assert result[2]["product_name"] == "Laptop Stand"
    assert result[2]["units_sold"] == 12


def test_low_stock_products():
    result = get_low_stock_products()

    product_names = {
        product["product_name"] for product in result
    }

    assert product_names == {
        "Mechanical Keyboard",
        "USB-C Hub",
        "Webcam HD",
        "Monitor 24 Inch",
    }


def test_top_products_rejects_invalid_limit():
    try:
        get_top_products(limit=0)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for limit=0")


def test_top_products_revenue_is_correct():
    result = get_top_products(limit=5)

    products_by_name = {
        product["product_name"]: product
        for product in result
    }

    assert products_by_name["Laptop Stand"]["revenue"] == 2_160_000
    assert products_by_name["Headset"]["revenue"] == 2_750_000
    assert products_by_name["Laptop Bag"]["revenue"] == 2_250_000