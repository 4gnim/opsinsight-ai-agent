import logging

from fastapi import FastAPI, HTTPException

from opsinsight.agent import ask_agent
from opsinsight.report import build_sales_report
from opsinsight.schemas import AskRequest, AskResponse

logger = logging.getLogger(__name__)


app = FastAPI(
    title="OpsInsight AI Agent",
    description="AI agent for sales and inventory analysis.",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Check whether the API process is running."""
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    """Ask the AI Agent a question about business data."""
    try:
        answer = ask_agent(request.question)
        return AskResponse(answer=answer)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.exception("Agent request failed.")
        raise HTTPException(
            status_code=500,
            detail="The agent could not complete the request.",
        ) from exc


@app.get("/report")
def get_report() -> dict:
    """Return a factual business report from the database."""
    return build_sales_report()