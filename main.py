from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from agents.market_analysis import MarketAnalysisAgent
from agents.risk_scoring import RiskScoringAgent
from agents.project_tracking import ProjectTrackingAgent
from agents.reporting import ReportingAgent
from api.routes import router as api_router
import uvicorn
import os

app = FastAPI(title="AI-Powered Project Risk Management System",
              description="Real-time project risk detection and mitigation system",
              version="1.0.0")

# Initialize agents
market_agent = MarketAnalysisAgent()
risk_agent = RiskScoringAgent()
project_agent = ProjectTrackingAgent()
reporting_agent = ReportingAgent()

# Include API routes
app.include_router(api_router, prefix="/api")

# Serve static files for frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def serve_frontend():
    """Serve the frontend dashboard"""
    with open("frontend/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.on_event("startup")
async def startup_event():
    """Initialize application state on startup"""
    print("Starting up risk management system...")
    # Initialize any required resources here

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    print("Shutting down risk management system...")

if __name__ == "__main__":
    # Create frontend directory if it doesn't exist
    os.makedirs("frontend", exist_ok=True)
    
    # Run the application
    uvicorn.run(app, host="0.0.0.0", port=8000)
