
import os

import pandas as pd
import requests
import streamlit as st


API_BASE_URL = os.getenv(
    "OPSINSIGHT_API_URL",
    "http://127.0.0.1:8000",
).rstrip("/")

st.set_page_config(
    page_title="OpsInsight AI Agent",
    page_icon="📊",
    layout="wide",
)

st.title("OpsInsight AI Agent")
st.caption("AI-powered Sales & Inventory Analysis")

st.sidebar.header("Pengaturan")
st.sidebar.write("Backend: FastAPI")
st.sidebar.write("Data: SQLite")
st.sidebar.write("AI Agent: LangGraph + Ollama")
st.sidebar.caption(f"API: {API_BASE_URL}")


def fetch_report() -> dict:
    """Fetch the factual report from FastAPI."""
    response = requests.get(
        f"{API_BASE_URL}/report",
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def ask_api(question: str) -> str:
    """Send a question to the OpsInsight agent."""
    response = requests.post(
        f"{API_BASE_URL}/ask",
        json={"question": question},
        timeout=120,
    )
    response.raise_for_status()

    result = response.json()
    answer = result.get("answer")

    if not isinstance(answer, str) or not answer.strip():
        raise ValueError("API returned an empty answer.")

    return answer


# -------------------------
# Business report
# -------------------------
st.header("Business Overview")

if st.button("Refresh Report"):
    st.rerun()

try:
    report = fetch_report()
    summary = report["summary"]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Revenue",
        f"Rp{summary['total_revenue']:,.0f}",
    )
    col2.metric(
    "Units Sold",
    f"{summary['units_sold']:,}",
    )
    col3.metric(
        "Transactions",
        f"{summary['transaction_count']:,}",
    )

    st.caption(
        f"Data source: {report['metadata']['source']} | "
        f"Currency: {report['metadata']['currency']}"
    )

    period_col1, period_col2 = st.columns(2)

    period_col1.write(
        f"**First sale:** {summary['first_sale_date']}"
    )
    period_col2.write(
        f"**Last sale:** {summary['last_sale_date']}"
    )

    st.subheader("Top-Selling Products")

    top_products = report["top_products"]

    if top_products:
        top_df = pd.DataFrame(top_products)
        st.dataframe(
            top_df,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No sales data available.")

    st.subheader("Low-Stock Products")

    low_stock = report["low_stock_products"]

    if low_stock:
        stock_df = pd.DataFrame(low_stock)
        st.dataframe(
            stock_df,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.success("No products are at or below minimum stock.")

    st.info(report["evaluation_limits"]["note"])

except requests.RequestException:
    st.error(
        "Could not retrieve the report. "
        "Make sure the FastAPI server is running."
    )
except (KeyError, TypeError, ValueError) as exc:
    st.error(f"The report response is invalid: {exc}")


# -------------------------
# AI chat
# -------------------------
st.divider()
st.header("Ask OpsInsight")
st.caption(
    "AI-generated answers may contain errors. "
    "Verify important figures against the business report above."
)
st.write(
    "Ask questions about sales, top-selling products, "
    "and inventory. Answers depend on the available database."
)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(
    "Example: Produk apa yang paling banyak terjual?"
)

if question:
    st.session_state.chat_history.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing business data..."):
            try:
                answer = ask_api(question)
                st.markdown(answer)

                st.session_state.chat_history.append(
                    {"role": "assistant", "content": answer}
                )

            except requests.Timeout:
                st.error(
                    "The request timed out. "
                    "The model may need more time to respond."
                )
            except requests.RequestException:
                st.error(
                    "Could not connect to the AI agent. "
                    "Check the API server and try again."
                )
            except ValueError as exc:
                st.error(str(exc))
