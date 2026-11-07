from FastAPI import APIRouter
from app.storage import tasks

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.get("/")
def get_tasks():
    return tasks