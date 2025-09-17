import uvicorn
from fastapi import FastAPI
from .api.routes import router
from .config import settings
from .utils.logger import get_logger

logger = get_logger(__name__)
app = FastAPI(title="aide.ai Agent Daemon")
app.include_router(router)

def run():
    uvicorn.run("src.ai_agent.main:app", host="127.0.0.1", port=settings.PORT, reload=False)

if __name__ == "__main__":
    run()