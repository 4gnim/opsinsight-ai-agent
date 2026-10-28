import logging
from fastapi.testclient import TestClient

from opsinsight.api import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_report_endpoint_returns_verified_summary():
    response = client.get("/report")

    assert response.status_code == 200

    data = response.json()

    assert data["summary"]["transaction_count"] == 30
    assert data["summary"]["units_sold"] == 102
    assert data["summary"]["total_revenue"] == 24_300_000


def test_report_endpoint_contains_top_products():
    response = client.get("/report")

    assert response.status_code == 200

    data = response.json()
    top_products = data["top_products"]

    assert len(top_products) == 3
    assert top_products[0]["product_name"] == "HDMI Cable"
    assert top_products[0]["units_sold"] == 30
    assert top_products[0]["revenue"] == 1_950_000


def test_report_endpoint_contains_low_stock_products():
    response = client.get("/report")

    assert response.status_code == 200

    data = response.json()

    product_names = {
        product["product_name"]
        for product in data["low_stock_products"]
    }

    assert product_names == {
        "Mechanical Keyboard",
        "USB-C Hub",
        "Webcam HD",
        "Monitor 24 Inch",
    }


def test_report_endpoint_discloses_evaluation_limits():
    response = client.get("/report")

    assert response.status_code == 200

    limits = response.json()["evaluation_limits"]

    assert limits["sales_target_available"] is False
    assert limits["historical_comparison_available"] is False
    assert limits["profit_data_available"] is False


def test_ask_rejects_empty_question():
    response = client.post(
        "/ask",
        json={"question": ""},
    )

    assert response.status_code == 422


def test_ask_rejects_question_over_1000_characters():
    response = client.post(
        "/ask",
        json={"question": "a" * 1001},
    )

    assert response.status_code == 422


def test_ask_rejects_whitespace_only_question():
    response = client.post(
        "/ask",
        json={"question": "   "},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Question must not be empty."


def test_ask_returns_answer(monkeypatch):
    def fake_ask_agent(question: str) -> str:
        return "Total pendapatan adalah Rp24.300.000."

    monkeypatch.setattr(
        "opsinsight.api.ask_agent",
        fake_ask_agent,
    )

    response = client.post(
        "/ask",
        json={"question": "Berapa total pendapatan?"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "Total pendapatan adalah Rp24.300.000."
    }


def test_ask_returns_generic_error_on_agent_failure(monkeypatch):
    def fake_ask_agent(question: str) -> str:
        raise RuntimeError("Internal model error")

    monkeypatch.setattr(
        "opsinsight.api.ask_agent",
        fake_ask_agent,
    )

    response = client.post(
        "/ask",
        json={"question": "Berapa total pendapatan?"},
    )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "The agent could not complete the request."
    }



def test_ask_logs_internal_error(monkeypatch, caplog):
    def fake_ask_agent(question: str) -> str:
        raise RuntimeError("Internal model error")

    monkeypatch.setattr("opsinsight.api.ask_agent", fake_ask_agent)

    with caplog.at_level(logging.ERROR, logger="opsinsight.api"):
        response = client.post(
            "/ask",
            json={"question": "Berapa total pendapatan?"},
        )

    assert response.status_code == 500
    assert "Agent request failed." in caplog.text
    assert "Internal model error" in caplog.text


def test_report_summary_matches_frontend_contract():
    response = client.get("/report")

    assert response.status_code == 200

    summary = response.json()["summary"]

    # Fields consumed by the Streamlit dashboard
    assert "total_revenue" in summary
    assert "units_sold" in summary
    assert "transaction_count" in summary

    # Verify the seeded dataset values
    assert summary["total_revenue"] == 24_300_000
    assert summary["units_sold"] == 102
    assert summary["transaction_count"] == 30