from fastapi import FastAPI

app = FastAPI(
    title="AI-Powered Code Review Tool Backend",
    description="Backend API for automated code review, security, and quality suggestions.",
    version="0.1.0"
)

@app.get("/health", tags=["Health Check"])
async def health_check():
    """Perform a health check on the API."""
    return {"status": "healthy", "message": "AI Code Review API is running!"}

# To run this application:
# 1. Save the code as main.py
# 2. Install FastAPI and Uvicorn: pip install "fastapi[all]"
# 3. Run from your terminal: uvicorn main:app --reload --host 0.0.0.0 --port 8000
