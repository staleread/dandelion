from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def hello_router():
    return "Hello, router"
