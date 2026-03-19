from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import auth, book_copies, book_titles, borrow_slips, categories, readers, reports, users
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_routes = [
    auth.router,
    users.router,
    readers.router,
    categories.router,
    book_titles.router,
    book_copies.router,
    borrow_slips.router,
    reports.router,
]
for route in api_routes:
    app.include_router(route, prefix=settings.api_prefix)


@app.get("/")
def root():
    return {"message": "Library management API is running."}


@app.exception_handler(ValueError)
def handle_value_error(_, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
