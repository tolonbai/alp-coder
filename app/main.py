from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.agent import agent


app = FastAPI(
    title="AI DevOps Agent API",
    version="0.1.0",
    description="Local AI agent for controlled Kubernetes operations",
)


class AgentRequest(BaseModel):
    message: str


class AgentResponse(BaseModel):
    result: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "aidevops-agent"
    }


@app.post("/api/v1/agent", response_model=AgentResponse)
def run_agent(request: AgentRequest):
    try:
        result = agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": request.message
                }
            ]
        })

        return AgentResponse(
            result=result["messages"][-1].content
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )