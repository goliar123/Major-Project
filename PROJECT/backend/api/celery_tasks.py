import sys
import os
from pathlib import Path

# Add project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from celery import Celery
from config.settings import settings
from dataset.schema import MultiAgentTrace
from core.engine import attribution_engine
from dataset.loader import dataset_loader

celery_app = Celery(
    "attribution_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)

@celery_app.task(name="tasks.attribute_trace_async")
def attribute_trace_async(trace_dict: dict) -> dict:
    """Asynchronously processes a trace attribution job."""
    steps_data = trace_dict.get("steps", [])
    trace = MultiAgentTrace(
        trace_id=trace_dict.get("trace_id", "async-trace"),
        title=trace_dict.get("title"),
        environment_name=trace_dict.get("environment_name", "AutoGen"),
        task_goal=trace_dict.get("task_goal", ""),
        steps=steps_data
    )
    verdict = attribution_engine.attribute_trace(trace)
    return verdict.model_dump()
