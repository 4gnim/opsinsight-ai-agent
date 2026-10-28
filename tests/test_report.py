from opsinsight.report import build_sales_report


def test_sales_report_contains_verified_data():
    report = build_sales_report()

    assert report["summary"]["total_revenue"] == 24_300_000
    assert report["summary"]["units_sold"] == 102

    assert report["top_products"][0]["product_name"] == "HDMI Cable"
    assert report["top_products"][0]["revenue"] == 1_950_000

    assert len(report["low_stock_products"]) == 4

    assert report["evaluation_limits"]["sales_target_available"] is False
    assert report["evaluation_limits"]["historical_comparison_available"] is False



def test_sales_report_includes_metadata():
    from opsinsight.report import build_sales_report

    report = build_sales_report()

    assert report["metadata"]["source"] == "SQLite database"
    assert report["metadata"]["report_type"] == "sales_and_inventory"
    assert report["metadata"]["currency"] == "IDR"


def test_sales_report_does_not_claim_performance_evaluation():
    from opsinsight.report import build_sales_report

    report = build_sales_report()
    limits = report["evaluation_limits"]

    assert limits["sales_target_available"] is False
    assert limits["historical_comparison_available"] is False
    assert limits["profit_data_available"] is False
