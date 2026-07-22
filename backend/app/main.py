print("LOADING MY STUDY PLANNER MAIN.PY")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.routes import auth, subjects, tasks, schedule

# Initialize FastAPI app
app = FastAPI(
    title="Study Planner API",
    description="AI-powered study planning system",
    version="1.0.0"
)

# CORS middleware - allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(subjects.router)
app.include_router(tasks.router)
app.include_router(schedule.router)

# Startup event
@app.on_event("startup")
def startup():
    """Create all database tables on startup"""
    init_db()
    print("✅ Database tables initialized")


# Health check
@app.get("/")
def root():
    return {"message": "Study Planner API is running! 📚"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)