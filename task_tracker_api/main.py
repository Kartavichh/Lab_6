from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from routers.tasks import router as tasks_router
from config import settings
from dependencies import limiter  # ← импортируем отсюда

app = FastAPI(title="Task Tracker API (Secure)", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем limiter к приложению
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda req, exc: JSONResponse(
    status_code=429, content={"detail": "Превышен лимит запросов. Попробуйте позже."}
))

app.include_router(tasks_router)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    if request.url.path not in ("/docs", "/redoc", "/openapi.json"):
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

@app.get("/", tags=["System"])
def root(): 
    return {"service": "Task Tracker API", "status": "running", "security": "active"}