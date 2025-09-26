from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import auth, posts
from api.setup.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await create_db_and_tables()
    yield
    # Shutdown (if needed)


# Create FastAPI application instance with lifespan
app = FastAPI(
    title="FastAPI Application",
    description="A FastAPI application with proper structure and absolute imports",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(posts.router, prefix="/api/v1/posts", tags=["posts"])
app.include_router(auth.router, prefix="/auth", tags=["authentication"])


# Health check endpoint
@app.get("/")
async def root():
    return {"message": "FastAPI application is running!"}


@app.get("/healthz")
async def health_check():
    return {"status": "healthy"}
