# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from pathlib import Path
# from .routes import sequence

# app = FastAPI(
#     title="Krane API",
#     description="DNA/RNA Sequence Analysis API",
#     version="0.1.0"
# )

# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Mount static files
# static_path = Path(__file__).parent / "static"
# app.mount("/static", StaticFiles(directory=static_path), name="static")

# # Include routers
# app.include_router(sequence.router)
# app.include_router(sequence.router, prefix="/api/sequence")

# @app.get("/")
# async def root():
#     return {
#         "message": "Welcome to Krane API",
#         "docs": "/docs",
#         "redoc": "/redoc"
#     }

# def start_server():
#     """Entry point for the web server when installed as a package."""
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# if __name__ == "__main__":
#     start_server()

# src/krane/web/app.py
from fastapi import FastAPI, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from .routes import sequence
from .schemas.sequence import HealthResponse

app = FastAPI(
    title="Krane API",
    description="DNA/RNA Sequence Analysis API",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Configure templates
# templates = Jinja2Templates(directory=Path(__file__).parent / "web" / "templates")
# Configure templates - Fix the path resolution
template_path = Path(__file__).parent / "templates"  # Remove duplicate 'web'
templates = Jinja2Templates(directory=str(template_path))

# Include routers
app.include_router(sequence.router)
app.include_router(sequence.router, prefix="/api/sequence")

@app.get("/")
async def root():
    return {
        "message": "Welcome to Krane API",
        "docs": "/docs",
        "redoc": "/redoc",
        "help": "/help",
        "demo": "/demo"
    }

@app.get("/healthz", 
         response_model=HealthResponse,
         status_code=status.HTTP_200_OK,
         summary="Health Check",
         description="Returns the health status of the API")
async def health_check():
    """
    Perform a health check on the API.
    
    Returns:
        HealthResponse: Object containing the health status
    """
    return HealthResponse(status="online")

@app.get("/help",
         summary="API Help",
         description="Returns the help page")
async def help(request: Request):
    """
    Render the help page.
    """
    return templates.TemplateResponse(
        "help.html",
        {"request": request, "title": "API Help"}
    )

@app.get("/demo",
         summary="API Demo",
         description="Returns the demo page")
async def demo(request: Request):
    """
    Render the demo page.
    """
    return templates.TemplateResponse(
        "demo.html",
        {"request": request, "title": "API Demo"}
    )

def start_server():
    """Entry point for the web server when installed as a package."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_server()